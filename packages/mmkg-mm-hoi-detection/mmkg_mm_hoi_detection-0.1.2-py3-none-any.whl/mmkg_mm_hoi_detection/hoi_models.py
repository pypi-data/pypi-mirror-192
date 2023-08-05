import argparse
import datetime
import json
import random
import time
from pathlib import Path
from PIL import Image
import numpy as np
import torch
from torch.utils.data import DataLoader, DistributedSampler
from torch import nn
from .util import misc as utils
from .models import build_model
import os
from .datasets import transforms as T
from .datasets.hico_nms import HICOnms
from .datasets.static_hico import HICO_INTERACTIONS
import itertools
import cv2
def cv2PIL(img_cv):
    return Image.fromarray(cv2.cvtColor(img_cv,cv2.COLOR_BGR2RGB))

def random_color():
    rdn = random.randint(1, 2222)
    b = int(rdn * 997) % 255
    g = int(rdn * 4447) % 255
    r = int(rdn * 6563) % 255
    return b, g, r

def get_args_parser():
    parser = argparse.ArgumentParser('Set transformer detector', add_help=False)
    parser.add_argument('--lr', default=1e-4, type=float)
    parser.add_argument('--lr_backbone', default=1e-5, type=float)
    parser.add_argument('--lr_clip', default=1e-5, type=float)
    parser.add_argument('--batch_size', default=2, type=int)
    parser.add_argument('--weight_decay', default=1e-4, type=float)
    parser.add_argument('--epochs', default=150, type=int)
    parser.add_argument('--lr_drop', default=100, type=int)
    parser.add_argument('--clip_max_norm', default=0.1, type=float,
                        help='gradient clipping max norm')

    # Model parameters
    parser.add_argument('--frozen_weights', type=str, default=None,
                        help="Path to the pretrained model. If set, only the mask head will be trained")
    # * Backbone
    parser.add_argument('--backbone', default='resnet50', type=str,
                        help="Name of the convolutional backbone to use")
    parser.add_argument('--dilation', action='store_true',
                        help="If true, we replace stride with dilation in the last convolutional block (DC5)")
    parser.add_argument('--position_embedding', default='sine', type=str, choices=('sine', 'learned'),
                        help="Type of positional embedding to use on top of the image features")

    # * Transformer
    parser.add_argument('--enc_layers', default=6, type=int,
                        help="Number of encoding layers in the transformer")
    parser.add_argument('--dec_layers', default=3, type=int,
                        help="Number of stage1 decoding layers in the transformer")
    parser.add_argument('--dim_feedforward', default=2048, type=int,
                        help="Intermediate size of the feedforward layers in the transformer blocks")
    parser.add_argument('--hidden_dim', default=256, type=int,
                        help="Size of the embeddings (dimension of the transformer)")
    parser.add_argument('--dropout', default=0.1, type=float,
                        help="Dropout applied in the transformer")
    parser.add_argument('--nheads', default=8, type=int,
                        help="Number of attention heads inside the transformer's attentions")
    parser.add_argument('--num_queries', default=64, type=int,
                        help="Number of query slots")
    parser.add_argument('--pre_norm', action='store_true')

    # * Segmentation
    parser.add_argument('--masks', action='store_true',
                        help="Train segmentation head if the flag is provided")

    # HOI
    parser.add_argument('--hoi', action='store_true',
                        help="Train for HOI if the flag is provided")
    parser.add_argument('--num_obj_classes', type=int, default=80,
                        help="Number of object classes")
    parser.add_argument('--num_verb_classes', type=int, default=117,
                        help="Number of verb classes")
    parser.add_argument('--pretrained', type=str, default='',
                        help='Pretrained model path')
    #path = './mmkg_mm_hoi_detection/pretrained/HICO_GEN_VLKT_S.pth'
    parser.add_argument('--subject_category_id', default=0, type=int)
    parser.add_argument('--verb_loss_type', type=str, default='focal',
                        help='Loss type for the verb classification')

    # Loss
    parser.add_argument('--no_aux_loss', dest='aux_loss', action='store_false',
                        help="Disables auxiliary decoding losses (loss at each layer)")
    parser.add_argument('--with_mimic', action='store_true',
                        help="Use clip feature mimic")
    # * Matcher
    parser.add_argument('--set_cost_class', default=1, type=float,
                        help="Class coefficient in the matching cost")
    parser.add_argument('--set_cost_bbox', default=2.5, type=float,
                        help="L1 box coefficient in the matching cost")
    parser.add_argument('--set_cost_giou', default=1, type=float,
                        help="giou box coefficient in the matching cost")
    parser.add_argument('--set_cost_obj_class', default=1, type=float,
                        help="Object class coefficient in the matching cost")
    parser.add_argument('--set_cost_verb_class', default=1, type=float,
                        help="Verb class coefficient in the matching cost")
    parser.add_argument('--set_cost_hoi', default=1, type=float,
                        help="Hoi class coefficient")

    # * Loss coefficients
    parser.add_argument('--mask_loss_coef', default=1, type=float)
    parser.add_argument('--dice_loss_coef', default=1, type=float)
    parser.add_argument('--bbox_loss_coef', default=2.5, type=float)
    parser.add_argument('--giou_loss_coef', default=1, type=float)
    parser.add_argument('--obj_loss_coef', default=1, type=float)
    parser.add_argument('--verb_loss_coef', default=2, type=float)
    parser.add_argument('--hoi_loss_coef', default=2, type=float)
    parser.add_argument('--mimic_loss_coef', default=20, type=float)
    parser.add_argument('--alpha', default=0.5, type=float, help='focal loss alpha')
    parser.add_argument('--eos_coef', default=0.1, type=float,
                        help="Relative classification weight of the no-object class")

    # dataset parameters
    parser.add_argument('--dataset_file', default='hico')
    parser.add_argument('--coco_path', type=str)
    parser.add_argument('--coco_panoptic_path', type=str)
    parser.add_argument('--remove_difficult', action='store_true')
    parser.add_argument('--hoi_path', type=str)

    parser.add_argument('--output_dir', default='',
                        help='path where to save, empty for no saving')
    parser.add_argument('--device', default='cuda',
                        help='device to use for training / testing')
    parser.add_argument('--seed', default=42, type=int)
    parser.add_argument('--resume', default='', help='resume from checkpoint')
    parser.add_argument('--start_epoch', default=0, type=int, metavar='N',
                        help='start epoch')
    parser.add_argument('--eval', action='store_true')
    parser.add_argument('--num_workers', default=2, type=int)

    # distributed training parameters
    parser.add_argument('--world_size', default=1, type=int,
                        help='number of distributed processes')
    parser.add_argument('--dist_url', default='env://', help='url used to set up distributed training')

    # hoi eval parameters
    parser.add_argument('--use_nms_filter', default='True',action='store_true', help='Use pair nms filter, default not use')
    parser.add_argument('--thres_nms', default=0.7, type=float)
    parser.add_argument('--nms_alpha', default=1, type=float)
    parser.add_argument('--nms_beta', default=0.5, type=float)
    parser.add_argument('--json_file', default='results.json', type=str)

    # clip
    parser.add_argument('--ft_clip_with_small_lr', action='store_true',
                        help='Use smaller learning rate to finetune clip weights')
    parser.add_argument('--with_clip_label', default='True',action='store_true', help='Use clip to classify HOI')
    parser.add_argument('--early_stop_mimic', action='store_true', help='stop mimic after step')
    parser.add_argument('--with_obj_clip_label',default='True', action='store_true', help='Use clip to classify object')
    parser.add_argument('--clip_model', default='ViT-B/32',
                        help='clip pretrained model path')
    parser.add_argument('--fix_clip', action='store_true', help='')
    parser.add_argument('--clip_embed_dim', default=512, type=int)

    # zero shot type
    parser.add_argument('--zero_shot_type', default='default',
                        help='default, rare_first, non_rare_first, unseen_object, unseen_verb')
    parser.add_argument('--del_unseen', action='store_true', help='')

    return parser


class MMHOIDetection(nn.Module):
    def __init__(self , pretrained=''):
        super().__init__()
        parser = argparse.ArgumentParser('GEN VLKT training and evaluation script', parents=[get_args_parser()])
        args = parser.parse_args()
        device = torch.device(args.device)
        self.device = device
        self.args=args
         # fix the seed for reproducibility
        seed = args.seed + utils.get_rank()
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        np.random.seed(seed)
        random.seed(seed)
        torch.backends.cudnn.deterministic = True

        model, criterion, postprocessors = build_model(args)
        model.to(device)
        #print('****************')
        #print(model)
        #print('****************')
        self.criterion = criterion
        self.postprocessors = postprocessors
        self.model_without_ddp = model
        self.model = model
        for name, p in model.named_parameters():
            if 'eval_visual_projection' in name:
                p.requires_grad = False
        #param_dicts = [
        #        {"params": [p for n, p in self.model_without_ddp.named_parameters() if
        #                    "backbone" not in n and 'visual_projection' not in n and p.requires_grad]},
        #        {
        #            "params": [p for n, p in self.model_without_ddp.named_parameters() if
        #                       "backbone" in n and p.requires_grad],
        #            "lr": args.lr_backbone,
        #        },
        #        {
        #            "params": [p for n, p in self.model_without_ddp.named_parameters() if
        #                       'visual_projection' in n and p.requires_grad],
        #            "lr": args.lr_clip,
        #        },
        #    ]
        #output_dir = Path(args.output_dir)
        if len(pretrained)>1:
            checkpoint = torch.load(pretrained, map_location='cpu')
            self.model_without_ddp.load_state_dict(checkpoint['model'])
            self.model.load_state_dict(checkpoint['model'])
        print('HOI Model Constructed.')
    
    @torch.no_grad()
    def inference(self, image, output_path=''):
        img = image.convert('RGB')
        w, h = img.size
        normalize = T.Compose([
        T.ToTensor(),
        T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
        _transform = T.Compose([
            T.RandomResize([800], max_size=1333),
            normalize,
        ])
        
        orig_size = torch.as_tensor([[int(h), int(w)]])
        samples,_ = _transform(img,None)
        self.model.eval()
        print('Read one image.')
        samples = samples.to(self.device)
        samples = samples.unsqueeze(0)
        outputs = self.model(samples, is_training=False)
        
        results = self.postprocessors['hoi'](outputs, orig_size)
        preds = []
        preds.extend(list(itertools.chain.from_iterable(utils.all_gather(results))))
        nms = HICOnms(preds,self.args)
        preds_nms = nms.get_nms_preds()
        img_preds = preds_nms[0]
        #import ipdb;ipdb.set_trace()
        img_result = self.viz_hoi_result(img,img_preds)
        if len(output_path) > 0:
            cv2.imwrite(output_path, img_result)
        
        return preds_nms,cv2PIL(img_result)

    def viz_hoi_result(self,img, hoi_list):
        img_result = img.copy()
        img_result = cv2.cvtColor(np.asarray(img_result), cv2.COLOR_RGB2BGR)
        boxes = hoi_list['predictions']
        font_scale = 0.6
        hois = hoi_list['hoi_prediction']
        hois.sort(key=lambda hoi: (hoi['subject_id'], hoi['object_id']))

        hp = {}
        for idx_box, hoi in enumerate(hois):
            color = random_color()
            sb = str(hoi['subject_id'])
            ob = str(hoi['object_id'])
            bid = sb+' '+ob
            if bid in hp:
                color = hp[bid]
            hp[bid]=color
            # action
            i_name, i_score = hoi['category_id'], hoi['score']
            i_name = HICO_INTERACTIONS[i_name]['action'] +' ' + HICO_INTERACTIONS[i_name]['object']
            cv2.putText(img_result, '%s:%.2f' % (i_name, i_score),
                        (10, 20 * idx_box+20 ), cv2.FONT_HERSHEY_COMPLEX, font_scale, color, 1,cv2.LINE_AA)
            # human
            x1, y1, x2, y2 = map(int,boxes[hoi['subject_id']]['bbox'])
            smx,smy = (x1+x2)/2,(y1+y2)/2

            h_name = 'person'
            cv2.rectangle(img_result, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img_result, '%s' % h_name, (x1, y2-5), cv2.FONT_HERSHEY_COMPLEX, font_scale, color, 1,cv2.LINE_AA)
            # object
            x1, y1, x2, y2 = map(int,boxes[hoi['object_id']]['bbox'])
            omx,omy = (x1+x2)/2,(y1+y2)/2
            o_name = HICO_INTERACTIONS[hoi['category_id']]['object']
            action = HICO_INTERACTIONS[hoi['category_id']]['action']
            cv2.rectangle(img_result, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img_result, '%s'%o_name, (x1, y2-5), cv2.FONT_HERSHEY_COMPLEX, font_scale, color, 1,cv2.LINE_AA)
            
            cv2.line(img_result, (int(smx),int(smy)),(int(omx),int(omy)),color,2)
            #cv2.putText(img_result, '%s:%.2f'%(action, i_score), (int((smx+omx)/2),int((smy+omy)/2)), cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)

        if img_result.shape[0] > 480:
            ratio = img_result.shape[0] / 480  
            img_result = cv2.resize(img_result, (int(img_result.shape[1] / ratio), int(img_result.shape[0] / ratio)))
        return img_result

if __name__ == '__main__':
    model = MMHOIDetection()
    res = model.inference('/data/wangzp/EoID-master/data/hico_20160224_det/images/train2015/HICO_train2015_00000001.jpg')
    print(res)
    