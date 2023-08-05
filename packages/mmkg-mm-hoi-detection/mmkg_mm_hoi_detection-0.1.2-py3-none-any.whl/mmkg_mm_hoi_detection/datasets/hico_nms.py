# ------------------------------------------------------------------------
# Copyright (c) Hitachi, Ltd. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 [see LICENSE for details]
# ------------------------------------------------------------------------

import json
import os
from collections import defaultdict

import cv2
import numpy as np

from ..util.topk import top_k
from .hico_text_label import hico_text_label


class HICOnms():
    def __init__(self, preds, args):
        self.overlap_iou = 0.5
        self.max_hois = 15

        self.zero_shot_type = args.zero_shot_type

        self.use_nms_filter = args.use_nms_filter
        self.thres_nms = args.thres_nms
        self.nms_alpha = args.nms_alpha
        self.nms_beta = args.nms_beta

        self.use_score_thres = False
        self.thres_score = 1e-5

        self.use_soft_nms = False
        self.soft_nms_sigma = 0.5
        self.soft_nms_thres_score = 1e-11

        self.fp = defaultdict(list)
        self.tp = defaultdict(list)
        self.score = defaultdict(list)
        self.sum_gts = defaultdict(lambda: 0)
        self.gt_triplets = []

        self.preds = []
        self.hico_triplet_labels = list(hico_text_label.keys())
        self.hoi_obj_list = []
        for hoi_pair in self.hico_triplet_labels:
            self.hoi_obj_list.append(hoi_pair[1])

        for index, img_preds in enumerate(preds):
            img_preds = {k: v.to('cpu').numpy() for k, v in img_preds.items()}
            bboxes = [{'bbox': list(bbox)} for bbox in img_preds['boxes']]
            obj_scores = img_preds['obj_scores'] *  img_preds['obj_scores']
            hoi_scores = img_preds['hoi_scores'] + obj_scores[:, self.hoi_obj_list]

            hoi_labels = np.tile(np.arange(hoi_scores.shape[1]), (hoi_scores.shape[0], 1))
            subject_ids = np.tile(img_preds['sub_ids'], (hoi_scores.shape[1], 1)).T
            object_ids = np.tile(img_preds['obj_ids'], (hoi_scores.shape[1], 1)).T

            hoi_scores = hoi_scores.ravel()
            hoi_labels = hoi_labels.ravel()
            subject_ids = subject_ids.ravel()
            object_ids = object_ids.ravel()

            topk_hoi_scores = top_k(list(hoi_scores), self.max_hois)
            topk_indexes = np.array([np.where(hoi_scores == score)[0][0] for score in topk_hoi_scores])

            if len(subject_ids) > 0:
                hois = [{'subject_id': subject_id, 'object_id': object_id, 'category_id': category_id, 'score': score}
                        for
                        subject_id, object_id, category_id, score in
                        zip(subject_ids[topk_indexes], object_ids[topk_indexes], hoi_labels[topk_indexes], topk_hoi_scores)]
                hois = hois[:self.max_hois]
            else:
                hois = []
            self.preds.append({
                'filename': 'image_%03d'%(index),
                'predictions': bboxes,
                'hoi_prediction': hois
            })

        if self.use_nms_filter:
            print('eval use_nms_filter ...')
            self.preds = self.triplet_nms_filter(self.preds)

        print(len(self.preds))

    def get_nms_preds(self):
        return self.preds


    def triplet_nms_filter(self, preds):
        preds_filtered = []
        for img_preds in preds:
            pred_bboxes = img_preds['predictions']
            pred_hois = img_preds['hoi_prediction']
            all_triplets = {}
            for index, pred_hoi in enumerate(pred_hois):
                triplet = pred_hoi['category_id']

                if triplet not in all_triplets:
                    all_triplets[triplet] = {'subs': [], 'objs': [], 'scores': [], 'indexes': []}
                all_triplets[triplet]['subs'].append(pred_bboxes[pred_hoi['subject_id']]['bbox'])
                all_triplets[triplet]['objs'].append(pred_bboxes[pred_hoi['object_id']]['bbox'])
                all_triplets[triplet]['scores'].append(pred_hoi['score'])
                all_triplets[triplet]['indexes'].append(index)

            all_keep_inds = []
            for triplet, values in all_triplets.items():
                subs, objs, scores = values['subs'], values['objs'], values['scores']
                if self.use_soft_nms:
                    keep_inds = self.pairwise_soft_nms(np.array(subs), np.array(objs), np.array(scores))
                else:
                    keep_inds = self.pairwise_nms(np.array(subs), np.array(objs), np.array(scores))

                if self.use_score_thres:
                    sorted_scores = np.array(scores)[keep_inds]
                    keep_inds = np.array(keep_inds)[sorted_scores > self.thres_score]

                keep_inds = list(np.array(values['indexes'])[keep_inds])
                all_keep_inds.extend(keep_inds)

            preds_filtered.append({
                'filename': img_preds['filename'],
                'predictions': pred_bboxes,
                'hoi_prediction': list(np.array(img_preds['hoi_prediction'])[all_keep_inds])
            })

        return preds_filtered

    def pairwise_nms(self, subs, objs, scores):
        sx1, sy1, sx2, sy2 = subs[:, 0], subs[:, 1], subs[:, 2], subs[:, 3]
        ox1, oy1, ox2, oy2 = objs[:, 0], objs[:, 1], objs[:, 2], objs[:, 3]

        sub_areas = (sx2 - sx1 + 1) * (sy2 - sy1 + 1)
        obj_areas = (ox2 - ox1 + 1) * (oy2 - oy1 + 1)

        order = scores.argsort()[::-1]

        keep_inds = []
        while order.size > 0:
            i = order[0]
            keep_inds.append(i)

            sxx1 = np.maximum(sx1[i], sx1[order[1:]])
            syy1 = np.maximum(sy1[i], sy1[order[1:]])
            sxx2 = np.minimum(sx2[i], sx2[order[1:]])
            syy2 = np.minimum(sy2[i], sy2[order[1:]])

            sw = np.maximum(0.0, sxx2 - sxx1 + 1)
            sh = np.maximum(0.0, syy2 - syy1 + 1)
            sub_inter = sw * sh
            sub_union = sub_areas[i] + sub_areas[order[1:]] - sub_inter

            oxx1 = np.maximum(ox1[i], ox1[order[1:]])
            oyy1 = np.maximum(oy1[i], oy1[order[1:]])
            oxx2 = np.minimum(ox2[i], ox2[order[1:]])
            oyy2 = np.minimum(oy2[i], oy2[order[1:]])

            ow = np.maximum(0.0, oxx2 - oxx1 + 1)
            oh = np.maximum(0.0, oyy2 - oyy1 + 1)
            obj_inter = ow * oh
            obj_union = obj_areas[i] + obj_areas[order[1:]] - obj_inter

            ovr = np.power(sub_inter / sub_union, self.nms_alpha) * np.power(obj_inter / obj_union, self.nms_beta)
            inds = np.where(ovr <= self.thres_nms)[0]

            order = order[inds + 1]
        return keep_inds

    def pairwise_soft_nms(self, subs, objs, scores):
        assert subs.shape[0] == objs.shape[0]
        N = subs.shape[0]

        sx1, sy1, sx2, sy2 = subs[:, 0], subs[:, 1], subs[:, 2], subs[:, 3]
        ox1, oy1, ox2, oy2 = objs[:, 0], objs[:, 1], objs[:, 2], objs[:, 3]

        sub_areas = (sx2 - sx1 + 1) * (sy2 - sy1 + 1)
        obj_areas = (ox2 - ox1 + 1) * (oy2 - oy1 + 1)

        for i in range(N):
            tscore = scores[i]
            pos = i + 1
            if i != N - 1:
                maxpos = np.argmax(scores[pos:])
                maxscore = scores[pos:][maxpos]

                if tscore < maxscore:
                    subs[i], subs[maxpos.item() + i + 1] = subs[maxpos.item() + i + 1].copy(), subs[i].copy()
                    sub_areas[i], sub_areas[maxpos + i + 1] = sub_areas[maxpos + i + 1].copy(), sub_areas[i].copy()

                    objs[i], objs[maxpos.item() + i + 1] = objs[maxpos.item() + i + 1].copy(), objs[i].copy()
                    obj_areas[i], obj_areas[maxpos + i + 1] = obj_areas[maxpos + i + 1].copy(), obj_areas[i].copy()

                    scores[i], scores[maxpos.item() + i + 1] = scores[maxpos.item() + i + 1].copy(), scores[i].copy()

            # IoU calculate
            sxx1 = np.maximum(subs[i, 0], subs[pos:, 0])
            syy1 = np.maximum(subs[i, 1], subs[pos:, 1])
            sxx2 = np.minimum(subs[i, 2], subs[pos:, 2])
            syy2 = np.minimum(subs[i, 3], subs[pos:, 3])

            sw = np.maximum(0.0, sxx2 - sxx1 + 1)
            sh = np.maximum(0.0, syy2 - syy1 + 1)
            sub_inter = sw * sh
            sub_union = sub_areas[i] + sub_areas[pos:] - sub_inter
            sub_ovr = sub_inter / sub_union

            oxx1 = np.maximum(objs[i, 0], objs[pos:, 0])
            oyy1 = np.maximum(objs[i, 1], objs[pos:, 1])
            oxx2 = np.minimum(objs[i, 2], objs[pos:, 2])
            oyy2 = np.minimum(objs[i, 3], objs[pos:, 3])

            ow = np.maximum(0.0, oxx2 - oxx1 + 1)
            oh = np.maximum(0.0, oyy2 - oyy1 + 1)
            obj_inter = ow * oh
            obj_union = obj_areas[i] + obj_areas[pos:] - obj_inter
            obj_ovr = obj_inter / obj_union

            # Gaussian decay
            ## mode 1
            # weight = np.exp(-(sub_ovr * obj_ovr) / self.soft_nms_sigma)

            ## mode 2
            weight = np.exp(-sub_ovr / self.soft_nms_sigma) * np.exp(-obj_ovr / self.soft_nms_sigma)

            scores[pos:] = weight * scores[pos:]

        # select the boxes and keep the corresponding indexes
        keep_inds = np.where(scores > self.soft_nms_thres_score)[0]

        return keep_inds


    def bbox_clip(self, box, size):
        x1, y1, x2, y2 = box
        h, w = size
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(x2, w)
        y2 = min(y2, h)
        return [x1, y1, x2, y2]
