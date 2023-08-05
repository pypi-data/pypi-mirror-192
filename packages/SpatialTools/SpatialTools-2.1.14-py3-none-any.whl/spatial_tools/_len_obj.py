#!/share/nas2/genome/biosoft/Python//3.7.3/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2022/12/28 22:51
# @Author : jmzhang
# @Email : zhangjm@biomarker.com.cn

from matplotlib.axes._axes import _log as matplotlib_axes_logger
import matplotlib.pyplot as plt
from matplotlib import image
import _pickle as cPickle
from pathlib import Path
import seaborn as sns
import anndata as ad
import pickle, gzip
import pandas as pd
import scanpy as sc
import numpy as np
import warnings
import argparse
import logging
import anndata
import json
import math
import re


class LenObjet:
    def __init__(self, pic, barcodes_pos, low_pic=None):
        self._pic = image.imread(pic)

        if low_pic:
            self._low_pic = image.imread(low_pic)
            self._low_contain = True
            self.low_scalar = self._cal_zoom_rate(self._low_pic.shape[0], self._low_pic.shape[1])
        else:
            self._low_pic = None
            self._low_contain = False

        self.container = self._make_container(barcodes_pos)
        self.scalar = self._cal_zoom_rate(self._pic.shape[0], self._pic.shape[1])

        self._adata_type = None
        self._facet_pos_list = None

    def __str__(self):
        info = 'low pic: {}\nlevel: {}\nscalar: {}'. \
            format('True' if self._low_contain else 'False',
                   list(self.container.keys()), self.scalar)
        return info

    def _make_container(self, barcodes_pos):
        """{"level2": {obsm: "", point_size: ""}, "level3":{obsm: "", point_size: ""}}"""
        container_dict = {}

        if not isinstance(barcodes_pos, list):
            barcodes_pos = [barcodes_pos]

        for i in barcodes_pos:
            obsm = pd.read_csv(i, '\t', names=['barcode', '__x', '__y'])
            point_size = self._auto_cal_radius(obsm)
            level = str(obsm['barcode'][0]).split('_')[0]
            container_dict[level] = {'obsm': obsm, 'point_size': point_size}

        return container_dict

    @staticmethod
    def _get_adata_level(input_adata):
        return str(input_adata['barcode'][0]).split('_')[0]

    @property
    def pic(self):
        return plt.imshow(self._pic)

    @property
    def low_pic(self):
        if not self._low_contain:
            raise ValueError('no low pic in SpatialTools')
        else:
            return plt.imshow(self._low_pic)

    @staticmethod
    def _cal_zoom_rate(width, height):
        """from litt@biomarker.com.cn SpatialCluster_split"""
        std_width = 1000
        std_height = std_width / (46 * 31) * (46 * 36 * np.sqrt(3) / 2.0)
        if std_width / std_height > width / height:
            scale = width / std_width
        else:
            scale = height / std_height
        return scale

    @staticmethod
    def _auto_cal_radius(cluster_pos_df):
        """from litt@biomarker.com.cn SpatialCluster_split"""
        radius = 999999
        pref_pos = [0, 0]
        for index, item in cluster_pos_df.iterrows():
            if index != 0:
                curr_pos = [item['__y'], item['__x']]
                center_dist = np.sqrt((curr_pos[0] - pref_pos[0]) ** 2 + (curr_pos[1] - pref_pos[1]) ** 2)
                if center_dist < radius:
                    radius = center_dist
            pref_pos = [item['__y'], item['__x']]
            if index > 1000:
                break
        radius = round(radius * 0.618 / 2)
        if radius < 1:
            radius = 1

        return radius
