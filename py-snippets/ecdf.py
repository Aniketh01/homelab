import matplotlib.pyplot as plt
import numpy as np

def ecdf(x, y_label='ECDF', x_label=None, ax=None, percentile=None,
         ecdf_color=None, ecdf_marker='o', percentile_color='black',
         percentile_linestyle='--'):

    if ax is None:
        ax = plt.gca()

    x = np.sort(x)
    y = np.arange(1, x.shape[0] + 1) / float(x.shape[0])

    ax.plot(x, y,
            marker=ecdf_marker,
            linestyle='',
            color=ecdf_color)
    ax.set_ylabel('ECDF')
    if x_label is not None:
        ax.set_xlabel(x_label)
    if percentile:
        targets = x[y <= percentile]
        percentile_threshold = targets.max()
        percentile_count = targets.shape[0]
        ax.axvline(percentile_threshold,
                   color=percentile_color,
                   linestyle=percentile_linestyle)

    else:
        percentile_threshold = None
        percentile_count = None

    return ax, percentile_threshold, percentile_count
