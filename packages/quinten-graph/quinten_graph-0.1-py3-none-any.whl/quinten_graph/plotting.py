"""
This sub-module contains functions and classes related to plotting.
The following functions are available:
    - plot_boxplot_kdeplot
    - plot_cat_countplot
    - radar_ploting_clustering
"""

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 

def plot_boxplot_kdeplot(data_df, var_list, hue=None, w=30, h=6):
    """# plot boxplot and kde plot with median and Std values for one or more designated variables

    args:
    - df
    - [variables] to plot (list with just the names between quotes, without the df)
    WIP:
    - hue: (str) key in df plugged into sns.kdeplot: Semantic variable that is mapped to determine the color of plot elements.
    ->  legend does not show as in classic sns.kdeplot

    kwargs:
    - width
    - height

    returns:
    - 1 boxplot
    - 1 kde plot with markers for min, max, med, mean
    - title with range, kurtosis and skew
    """
    # seting up the fig and the number of subplots according to the number of variables
    fig, axes = plt.subplots(len(var_list), 2)
    fig.set_size_inches(w, h * len(var_list))
    # setting up the space between subplots
    fig.tight_layout(h_pad=8, w_pad=3)

    # plotting for each variable
    for i, var in enumerate(var_list):

        # computing indicators to display
        mini = data_df[var].min()
        maxi = data_df[var].max()
        ran = data_df[var].max() - data_df[var].min()
        mean = data_df[var].mean()
        skew = data_df[var].skew()
        kurt = data_df[var].kurtosis()
        median = data_df[var].median()
        st_dev = data_df[var].std()
        points = mean - st_dev, mean + st_dev

        # boxplot
        sns.boxplot(
            x=data_df[var],
            ax=axes[i, 0],
            # color="#4D5B86",
            medianprops={"color": "white", "linewidth": 3},
            showmeans=True,
            meanprops={
                "marker": "o",
                "markerfacecolor": "red",
                "markeredgecolor": "white",
                "markersize": "15",
            },
        )
        axes[i, 0].set_xlabel(var, fontsize=25, **{"fontname": "Arial"})
        axes[i, 0].tick_params(axis="both", labelsize=15)

        # kde plot
        sns.kdeplot(
            data=data_df,
             x=var,
             ax=axes[i, 1],
            #  color="#4D5B86",
             hue=hue)
        axes[i, 1].set_ylabel(None)

        # ploting indicators over the kde plot
        max_y = axes[i, 1].get_ylim()[
            1
        ]  # this enables us to plot indicators at a readable scale VS kde plot, see below
        sns.lineplot(
            x=points,
            y=[max_y / 2.5, max_y / 2.5],
            ax=axes[i, 1],
            linestyle="dashed",
            color="black",
            label="std_dev",
        )
        sns.scatterplot(
            x=mini,
            y=[max_y / 2],
            ax=axes[i, 1],
            color="orange",
            label="min",
            marker=">",
            s=200,
        )
        sns.scatterplot(
            x=maxi,
            y=[max_y / 2],
            ax=axes[i, 1],
            color="orange",
            label="max",
            marker="<",
            s=200,
        )
        sns.scatterplot(
            x=[mean],
            y=[max_y / 2],
            ax=axes[i, 1],
            color="red",
            label="mean",
            marker="o",
            s=150,
        )
        sns.scatterplot(
            x=[median],
            y=max_y / 2,
            ax=axes[i, 1],
            color="blue",
            label="median",
            marker="v",
            s=150,
        )

        # setting tile, ticks and displaying indicators over the kde plot
        axes[i, 1].set_xlabel(var, fontsize=25, **{"fontname": "Arial"})
        axes[i, 1].tick_params(axis="both", labelsize=15)
        axes[i, 1].set_title(
            "std_dev = {} || kurtosis = {} || nskew = {} || range = {} \n || nmean = {} || median = {}".format(
                (round(st_dev, 2)),
                round(kurt, 2),
                round(skew, 2),
                (round(mini, 2), round(maxi, 2), round(ran, 2)),
                round(mean, 2),
                round(median, 2),
            ),
            fontsize=20,
        )
        axes[i, 1].legend(fontsize=15)

def plot_cat_countplot(
    data,
    var_list,
    hue=None,
    granularity=None,
    w=30,
    h=6,
    perc_annotation=True,
    annotation_size=15,
):
    """# plot countplot for one or more designated variables

    args:
    - df (df)
    - var_list (list of strings): list with just the names of the categorical variables to plot between quotes

    kwargs:
    - hue : hue to split the data for a given modality
    - granularite (string) : granularity of the df to be used in xlabel. ex: granularity='customer' => xlabel will be "count customer"
    - width : width of the figure
    - height : height of the figure, gets adjusted depending on the number of vars in var_list
    - perc_annotation (bool): whether to annotate % of one modality/hue vs total number
    - annotation_size (int): if perc_annotation: fontsize of the annotated %

    returns:
    - 1 countplot with modalities on X-axis and count on Y-axis

    issues:
    if no palette specified, sns checks that the length of the palette > cardinality of the plotted var, otherwise defaults to "dark" palette regardless of the palette set to default by sns.set_palette (https://github.com/mwaskom/seaborn/blob/0f5182ee01d28f2daeee805c7d4deb4a05b30bf0/seaborn/categorical.py#L655). This implies that quinten_palette won't be used if the plotted var has too high a cardinality. An alternative is to use sns.countplot manually with palette=QuintenSettings.quinten_palette after QuintenSettings is initialized.
    """
    from math import ceil

    # create figure and suplots depending on var_list
    fig, axes = plt.subplots(ceil(len(var_list) / 2), 2)
    fig.set_size_inches(w, h * len(var_list) * 0.8)
    fig.tight_layout(w_pad=6, h_pad=6)
    # populate each subplot (1 per var)
    for axe, ind in enumerate(var_list):
        #        data_count = data.groupby(ind)[index_col].count()
        ax = sns.countplot(
            data=data,
            x=ind,
            hue=hue,
            # palette=quinten_palette,
            ax=axes.ravel()[axe],
            orient="h",
            edgecolor ='black'
        )
        ax.set_xlabel(ind, fontsize=30)
        # if granularite is specified, add ylabel
        if granularity:
            ax.set_ylabel("count {}".format(granularity), fontsize=30)
        ax.tick_params(rotation=45)
        # add percentage as anotations
        if perc_annotation:
            total = float(data.shape[0])
            for p in ax.patches:
                percentage = "{:.1f}%".format(100 * p.get_height() / total)
                x = p.get_x() + p.get_width()
                y = p.get_height()
                ax.annotate(
                    percentage,
                    (x, y),
                    ha="right",
                    va="center",
                    fontsize=annotation_size,
                )

# functions for clustering plotting

from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

def _radar_factory(num_vars, frame="circle"):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = "radar"

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location("N")

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == "circle":
                return Circle((0.5, 0.5), 0.5)
            elif frame == "polygon":
                return RegularPolygon((0.5, 0.5), num_vars, radius=0.5, edgecolor="k")
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

        def draw(self, renderer):
            """Draw. If frame is polygon, make gridlines polygon-shaped"""
            if frame == "polygon":
                gridlines = self.yaxis.get_gridlines()
                for gl in gridlines:
                    gl.get_path()._interpolation_steps = num_vars
            super().draw(renderer)

        def _gen_axes_spines(self):
            if frame == "circle":
                return super()._gen_axes_spines()
            elif frame == "polygon":
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(
                    axes=self,
                    spine_type="circle",
                    path=Path.unit_regular_polygon(num_vars),
                )
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(
                    Affine2D().scale(0.5).translate(0.5, 0.5) + self.transAxes
                )

                return {"polar": spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


def radar_ploting_clustering(df, title):
    """DEPENDENT to function _radar_factory in the same module useful_functions.py

     Plot a radar chart displaying the different mean values of clusters for the numerical features of the df. Data should be standardized.
     The df should be grouped by clusters, and the clusters must be indicated in the first column of the df with name 'cluster'

     example of df:
          cluster  |  nb_orders  |  review_score  |  review_delay
    -----------------------------------------------------------
     0      0      |  1.000000   |  4.501408      |  9.215493
     1      1      |  1.000000   |  4.429864      |  6.090498
     2      2      |  2.145161   |  4.064516      |  5.500000

     parameters:
     - dataframe with the cluster indicated in the first column as 'cluster', other columns are numerical features that will form the axes of the radar
     - title to be given to the plot

     Output
     - radar chart with legend"""

    N = len(df.iloc[:, 1:].columns)
    theta = _radar_factory(N, frame="polygon")

    clusters = df.iloc[:, 0].values
    spoke_labels = df.iloc[:, 1:].columns
    case_data = df.iloc[:, 1:].values

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(projection="radar"))
    fig.subplots_adjust(top=0.85, bottom=0.05)

    # ax.set_rgrids([0.2, 0.4, 0.6, 0.8])
    ax.set_yticklabels([])  # remove r ticks
    ax.set_title(title, position=(0.5, 1.0), ha="center", fontsize=25)

    for d in case_data:
        line = ax.plot(theta, d)
        ax.fill(theta, d, alpha=0.15)
    ax.set_varlabels(spoke_labels)

    # add legend relative to top-left plot
    fig.text(0.98, 0.84, "Clusters", fontsize=14)
    legend = plt.gca().legend(clusters, loc=(1.1, 0.80), labelspacing=0.1, fontsize=12)

    plt.show()


def drop_columns(df):
    df.drop("id_client",
    axis=1, inplace= True)
    df.drop("branche",
    axis= 1, inplace= True)  # we drop branche for sake of simplicity
    return df