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


class Plotting:



    @staticmethod
    def _lighten_color(color, amount=0.5):
        """
        Lightens the given color by multiplying (1-luminosity) by the given amount.
        Input can be matplotlib color string, hex string, or RGB tuple.
        Examples:
        >> lighten_color('g', 0.3)
        >> lighten_color('#F034A3', 0.6)
        >> lighten_color((.3,.55,.1), 0.5)
        """
        import matplotlib.colors as mc
        import colorsys
        try:
            c = mc.cnames[color]
        except:
            c = color
        c = colorsys.rgb_to_hls(*mc.to_rgb(c))
        return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])

    def _facet_pos(self, length, ncol):
        nrow = math.ceil(length / ncol)
        facet_pos_list = []
        for i in range(nrow):
            for x in range(ncol):
                facet_pos_list.append((i, x))

        self._facet_pos_list = facet_pos_list

        return nrow, ncol

    @staticmethod
    def _change_para_dict(origin: dict, changed: dict):
        for k, v in changed.items():
            if k not in origin.keys():
                raise ValueError('wrong para_dict key value : {}'.format(k))

            origin[k] = v

        return origin

    def _discrete_scatter_plot(self, ax, para_dict: dict, color_dict):
        plot_para_dict = {'title': '', 'xlabel': 'S1000 spatial 1', 'ylabel': 'S1000 spatial 2',
                          'legend_scale': 1.2, 'legend_ncol': math.ceil(len(color_dict) / 17),
                          'legend_marker_size': None,
                          'show_ticks_and_labels': True}

        if para_dict:
            plot_para_dict = self._change_para_dict(plot_para_dict, para_dict)

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.99, box.height * 0.99])

        # ax.legend(
        #     loc='center left',
        #     markerscale=float(plot_para_dict['legend_scale']),
        #     bbox_to_anchor=(1, 0.5), ncol=int(plot_para_dict['legend_ncol']),
        #     fontsize=16, frameon=False, handletextpad=0.3)

        lgnd = plt.legend(
            loc='center left',
            markerscale=float(plot_para_dict['legend_scale']),
            bbox_to_anchor=(1, 0.5), ncol=int(plot_para_dict['legend_ncol']),
            fontsize=16, frameon=False, handletextpad=0.3)

        if plot_para_dict['legend_marker_size']:
            for _ in range(len(lgnd.legendHandles)):
                lgnd.legendHandles[_]._sizes = [plot_para_dict['legend_marker_size']]

        plt.title(plot_para_dict['title'])
        plt.xlabel(plot_para_dict['xlabel'])
        plt.ylabel(plot_para_dict['ylabel'])

        if not plot_para_dict['show_ticks_and_labels'] or plot_para_dict['show_ticks_and_labels'] == 'False':
            plt.xticks([])
            plt.yticks([])
            ax.xaxis.set_ticklabels([])
            ax.yaxis.set_ticklabels([])

    def _continuous_scatter_plot(self):
        pass

    def _crop_coord(self, plot_data, crop_coord: list, low_pic=False):
        x1, x2, y1, y2 = [int(_) for _ in crop_coord]
        pic = self._low_pic if low_pic else self._pic
        pic = pic[x1:x2, y1:y2, :]

        plot_data = plot_data.query('{} <= __x <= {} & {} <= __y <= {}'.format(y1, y2, x1, x2))
        plot_data2 = plot_data.copy()

        plot_data2['__y'] = plot_data2['__y'] - x1
        plot_data2['__x'] = plot_data2['__x'] - y1

        return pic, plot_data2

    def s1000_spatial_plot(self, adata: anndata,
                           color='seurat_clusters',
                           groups=None,
                           size=1,
                           size_auto=False,
                           alpha=1,
                           alpha_map_to_value=False,
                           cmap='viridis',
                           value_limits=None,
                           figsize=(10, 10),
                           crop_coord=None,
                           to_save=None,
                           darken=None,
                           return_fig=False,
                           return_table=False,
                           feature=None,
                           split=False,
                           ncol=2,
                           color_dict: dict = None,
                           hspace=None,
                           dpi=500,
                           wspace=None,
                           para_dict=None,
                           draw_pic=True,
                           low_pic=False,
                           interactive=False,
                           pic_only=False,
                           run_dash=False,
                           **kwargs):
        """
        - adata:
        - color:
        - para_dict:
            - discrete_scatter_plot:
                {'title': '', 'xlabel': 'S1000 spatial 1', 'ylabel': 'S1000 spatial 2',
                 'legend_scale': 1.2, 'legend_ncol': math.ceil(len(self.color_dict) / 17),
                 'show_ticks_and_labels': True}
                - title: 标题
                - xlabel: x轴标题
                - ylabel: y轴标题
                - legend_scale: 图例图形大小
                - legend_ncol: 图例列数，默认一列17个元素
                - show_ticks_and_labels: 是否展示刻度

            - continuous_scatter_plot
                {'xlabel': 'S1000 spatial 1', 'ylabel': 'S1000 spatial 2',
                 'show_ticks_and_labels': True, 'shrink': 0.4, 'pad': 0.05}

        """
        if color == 'class':
            raise 'please change columns of class'

        if low_pic:
            if not self._low_contain:
                raise ValueError('no low pic in SpatialTools')

        if isinstance(adata, sc.AnnData):
            adata = adata.copy()
            adata.obs.index.name = None
            adata.obs['barcode'] = adata.obs.index
            self._adata_type = 'AnnData'

            obsm = self.container[self._get_adata_level(adata.obs)]['obsm']
            point_size = self.container[self._get_adata_level(adata.obs)]['point_size']

            plot_data = obsm.merge(adata.obs, on='barcode')

        elif isinstance(adata, pd.DataFrame):
            adata = adata.copy()
            adata.index.name = None

            if 'barcode' not in adata.columns:
                adata['barcode'] = adata.index

            self._adata_type = 'DataFrame'

            obsm = self.container[self._get_adata_level(adata)]['obsm']
            point_size = self.container[self._get_adata_level(adata)]['point_size']

            plot_data = obsm.merge(adata, on='barcode')

        else:
            raise 'wrong adata, should be AnnData and DataFrame'

        if plot_data.shape[0] == 0:
            raise ValueError('barcodes of pic and matrix are inconsistent ...')

        if not feature:

            plot_data[color] = plot_data[color].astype(str)

            # 离散型散点图
            prob = list(plot_data[color].value_counts().index)

            if not color_dict:
                number_col = len(prob)
                if number_col <= 12:
                    selected_col = list(sns.color_palette("Paired", number_col))
                else:
                    selected_col = list(sns.color_palette(None, number_col))

                color_dict = dict(zip(prob, selected_col))

            if groups:

                for i in groups:
                    if i not in plot_data[color].unique():
                        raise 'groups not in column of color'

                plot_data = plot_data.query('{} in {}'.format(color, groups))
                plot_data[color] = plot_data[color].astype("category")
                plot_data[color] = plot_data[color].cat.set_categories(groups, ordered=True)
                prob = groups

            if darken:
                color_dict = {k: self._lighten_color(v, darken) for k, v in color_dict.items()}

            if not low_pic:
                plot_data['__x'] = np.round(plot_data['__x'] * self.scalar, 2)
                plot_data['__y'] = np.round(plot_data['__y'] * self.scalar, 2)

            else:
                plot_data['__x'] = np.round(plot_data['__x'] * self.low_scalar, 2)
                plot_data['__y'] = np.round(plot_data['__y'] * self.low_scalar, 2)

            if crop_coord:
                plot_pic, plot_data = self._crop_coord(plot_data=plot_data, low_pic=low_pic, crop_coord=crop_coord)
            else:
                plot_pic = self._low_pic if low_pic else self._pic

            size = point_size ** 2 if size == 1 else point_size ** 2 * size

            if size_auto:
                size = size * self.AUTO_SIZE_DISCRETE[self._get_adata_level(adata)]

            grouped = plot_data.groupby(color)

            # 执行交互
            if interactive or run_dash:
                fig = SpatialApp.interact_pic_discrete(plot_data_grouped=grouped,
                                                       pic=plot_pic,
                                                       color=color,
                                                       color_dict=dict(
                                                           zip(prob, sns.color_palette(None, len(prob)).as_hex())),
                                                       size=size,
                                                       alpha=alpha,
                                                       figsize=figsize,
                                                       pic_only=pic_only,
                                                       draw_pic=draw_pic,
                                                       to_save=to_save)

                return fig

            fig, ax = plt.subplots(constrained_layout=True, figsize=figsize)

            start = 0
            for key, group in grouped:

                if key in prob:
                    if split:
                        grid_dim = self._facet_pos(length=len(prob), ncol=ncol)
                        ax = plt.subplot2grid(grid_dim, self._facet_pos_list[start])
                        plt.tight_layout()
                        start += 1

                    group.plot(ax=ax, kind='scatter', x='__x', y='__y',
                               label=key,
                               c=color_dict[key],
                               s=size,
                               alpha=alpha)

                    self._discrete_scatter_plot(ax=ax,
                                                para_dict=para_dict,
                                                color_dict=color_dict)

                    if wspace:
                        plt.subplots_adjust(hspace=int(wspace))
                    if hspace:
                        plt.subplots_adjust(hspace=int(hspace))

                    if draw_pic:
                        plt.imshow(plot_pic)

            if not draw_pic:
                plt.gca().invert_yaxis()

            # plot_data = plot_data2

            # handles, labels = plt.gca().get_legend_handles_labels()
            # if self.levels:
            #     legend_order = [labels.index(i) for i in self.levels]
            # else:
            #     legend_order = [labels.index(i) for i in labels]
            #
            # ax.legend([handles[idx] for idx in legend_order], [labels[idx] for idx in legend_order])

        else:
            # 连续型散点图
            if not isinstance(feature, list):
                feature = [feature]

            if self._adata_type == 'AnnData':
                # in Anndata
                adata.var['symbol'] = adata.var.index
                prob = [i for i in feature if i in adata.obs.columns]

                if 'gene_ids' not in adata.var.columns:
                    adata.var['gene_ids'] = adata.var.index

                if 'symbol' not in adata.var.columns:
                    adata.var['symbol'] = adata.var.index

                symbol = list(adata.var.query('gene_ids in {} or symbol in {}'.format(feature, feature)).index)
                if not len(symbol) == 0:
                    gene_df = adata[:, symbol].to_df()
                    gene_df['barcode'] = gene_df.index
                    plot_data = plot_data.merge(gene_df, on='barcode')
                    prob += symbol

            else:
                prob = [i for i in feature if i in adata.columns]

            if len(prob) == 0:
                raise ValueError('wrong feature')

            size = point_size ** 2 if size == 1 else point_size ** 2 * size

            if size_auto:
                size = size * self.AUTO_SIZE_CONTINUOUS[self._get_adata_level(adata)]

            plot_para_dict = {'xlabel': 'S1000 spatial 1', 'ylabel': 'S1000 spatial 2',
                              'show_ticks_and_labels': True, 'shrink': 0.4, 'pad': 0.05}

            if para_dict:
                plot_para_dict = self._change_para_dict(plot_para_dict, para_dict)

            if not low_pic:
                plot_data['__x'] = plot_data['__x'] * self.scalar
                plot_data['__y'] = plot_data['__y'] * self.scalar

            else:
                plot_data['__x'] = plot_data['__x'] * self.low_scalar
                plot_data['__y'] = plot_data['__y'] * self.low_scalar

            if crop_coord:
                plot_pic, plot_data = self._crop_coord(plot_data=plot_data, low_pic=low_pic, crop_coord=crop_coord)
            else:
                plot_pic = self._low_pic if low_pic else self._pic

            if interactive or run_dash:
                fig = SpatialApp.interact_pic_continuous(plot_data=plot_data,
                                                         pic=plot_pic,
                                                         feature=prob[0],
                                                         size=size,
                                                         alpha=alpha,
                                                         cmap=cmap,
                                                         to_save=to_save,
                                                         pic_only=pic_only,
                                                         figsize=figsize,
                                                         draw_pic=draw_pic)

                return fig

            fig, ax = plt.subplots(constrained_layout=True, figsize=figsize)

            start = 0

            for feature in prob:
                if len(prob) > 1:
                    grid_dim = self._facet_pos(length=len(prob), ncol=ncol)
                    ax = plt.subplot2grid(grid_dim, self._facet_pos_list[start])
                    plt.tight_layout()
                    start += 1

                if alpha_map_to_value:
                    from sklearn.preprocessing import MinMaxScaler
                    scalar_alpha = MinMaxScaler(feature_range=(0, 1))
                    alpha = [i[0] for i in scalar_alpha.fit_transform(pd.DataFrame(np.array(plot_data[feature])))]

                if value_limits:
                    from sklearn.preprocessing import MinMaxScaler
                    scalar_value = MinMaxScaler(feature_range=value_limits)
                    value = [i[0] for i in scalar_value.fit_transform(pd.DataFrame(np.array(plot_data[feature])))]
                else:
                    value = plot_data[feature]

                plt.scatter(x=plot_data['__x'],
                            y=plot_data['__y'],
                            alpha=alpha,
                            s=size, cmap=cmap,
                            c=value)

                plt.title(feature)
                plt.xlabel(plot_para_dict['xlabel'])
                plt.ylabel(plot_para_dict['ylabel'])
                plt.colorbar(shrink=float(plot_para_dict['shrink']), pad=float(plot_para_dict['pad']))

                if draw_pic:
                    plt.imshow(plot_pic)
                else:
                    plt.gca().invert_yaxis()

                if not plot_para_dict['show_ticks_and_labels'] or plot_para_dict['show_ticks_and_labels'] == 'False':
                    plt.xticks([])
                    plt.yticks([])
                    ax.xaxis.set_ticklabels([])
                    ax.yaxis.set_ticklabels([])

                if wspace:
                    plt.subplots_adjust(hspace=float(wspace))
                if hspace:
                    plt.subplots_adjust(hspace=float(hspace))

        if to_save:
            self._plot_save(fig, to_save=to_save, dpi=dpi)

        if return_fig and return_table:
            return fig, plot_data

        if return_fig:
            return fig

        if return_table:
            return plot_data
    pass