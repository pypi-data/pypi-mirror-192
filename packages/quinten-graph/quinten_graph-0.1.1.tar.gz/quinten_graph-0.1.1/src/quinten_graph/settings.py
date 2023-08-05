"""
This sub-module contains settings and functions to easily set-up matplotlib and seaborn with quinten's chart and custom settings
The following functions are available:
    - set_style_pers
"""
import sys
sys.path.append('.')
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
# if running in repo use src.quinten_graph
from quinten_graph import config

class QuintenSettings(object):
    """_summary_

    Args:
            entity (str): finance, health, academy, holding. This determines to color palette used.

    Attributes:
        quinten_colors (list): list of colors used for the palette defined in config.py
        quinten_palette (matplotlib.colors.ListedColormap): custom palette built with quinten_colors
        linear_quinten_palette (matplotlib.colors.LinearSegmentedColormap): linear palette (to use with parameter "cmap" in sns.heatmap and potentially other graphs)
        dic_rc_params (dict): rc_params for matplotlib defined in config.py

    Methods:
        set_style_quinten : apply the parameters
    """
    def __init__(self, entity):
        """"""
        self.entity = entity
        self.quinten_colors = config.dic_quinten_colors[entity]
        self.quinten_palette = sns.color_palette(config.dic_quinten_colors[entity])
        self.linear_quinten_palette = matplotlib.colors.LinearSegmentedColormap.from_list(
            "", config.dic_quinten_linear_colors[entity])

    def set_style_quinten(
        self,
        sns_default_base_tehme=True,
        axe_grey_background=True,
        axe_grid = True,
        figsize=config.dic_rc_params["figsize"],
        axes_titlesize=config.dic_rc_params["axes_titlesize"],
        axes_labelsize=config.dic_rc_params["axes_labelsize"],
        lines_linewidth=config.dic_rc_params["lines_linewidth"],
        lines_markersize=config.dic_rc_params["lines_markersize"],
        xtick_labelsize=config.dic_rc_params["xtick_labelsize"],
        ytick_labelsize=config.dic_rc_params["ytick_labelsize"],
        font_family=config.dic_rc_params["font_family"],
    ):
        """ Set up matplotlib and seaborn with the graphic chart of Quinten's specifid entity.

        Args:
            sns_set (bool, optional): whether to call seaborn.set() at the start, which apply default seaborn's settings to matplotlib. Defaults to True.
            figsize (tuple, optional): rc_params defined in config.py. Defaults to config.dic_rc_params["figsize"].
            axes_titlesize (float, optional): rc_params defined in config.py. Defaults to config.dic_rc_params["axes_titlesize"].
            axes_labelsize (float, optional): rc_params defined in config.py. Defaults to config.dic_rc_params["axes_labelsize"].
            lines_linewidth (float, optional): rc_params defined in config.py. Defaults to config.dic_rc_params["lines_linewidth"].
            lines_markersize (float, optional): rc_params defined in config.py. Defaults to config.dic_rc_params["lines_markersize"].
            xtick_labelsize (float, optional): rc_params defined in config.py. Defaults to config.dic_rc_params["xtick_labelsize"].
            ytick_labelsize (float, optional): rc_params defined in config.py. Defaults to config.dic_rc_params["ytick_labelsize"].
            font_family (float, optional): rc_params defined in config.py. Defaults to config.dic_rc_params["font_family"].

        """
        # apply the default theme of seaborn upon which we apply below modifications
        if sns_default_base_tehme:
            sns.set_theme()
        # switch background from default grey to white
        if not axe_grey_background:
            matplotlib.rcParams.update({'axes.facecolor': '#ffffff'})
        # deactivate axe grid
        if not axe_grid:
            matplotlib.rcParams.update({'axes.grid': False})
        # if grid but no grey background, need to switch grid color from white to grey and deactivate x-axis grid
        if axe_grid and not axe_grey_background :
            grid_color = config.dic_quinten_colors[self.entity][0] # first color of the palette
            matplotlib.rcParams.update({"axes.grid.axis":"y", 'grid.color': grid_color})

        sns.set_palette(self.quinten_palette)

        plt.rc("figure", figsize=figsize)

        from cycler import cycler  # cycler for palette

        matplotlib.rcParams.update(
            {
                "axes.titlesize": axes_titlesize,  # axe title
                "axes.labelsize": axes_labelsize,
                "axes.prop_cycle": cycler(
                    "color",
                    self.quinten_colors,
                ),
                "lines.linewidth": lines_linewidth,
                "lines.markersize": lines_markersize,
                "xtick.labelsize": xtick_labelsize,
                "ytick.labelsize": ytick_labelsize,
                "font.family": font_family,
            }
        )

        return None
