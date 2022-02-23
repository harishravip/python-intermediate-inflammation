"""Tests for the view functions within the view layer."""
import matplotlib.pyplot as plt
import numpy as np
import numpy.testing as npt
from unittest.mock import patch


@patch("matplotlib.pyplot.show")
def test_visualize(mock_show):
    """Check that the image plotted has the correct data and it's
    displayed as expected."""
    from inflammation import models, views

    test_input = np.array([[1, 2, 1, 7],
                           [3, 4, 4, 1],
                           [5, 6, 5, 3]])

    view_data = {'average': models.daily_mean(test_input),
                 'max': models.daily_max(test_input),
                 'min': models.daily_min(test_input),
                 'std': models.daily_sd(test_input)}

    views.visualize(view_data)

    # Making sure there is an axes for each summary statistic.
    axs = plt.gcf().get_axes()
    assert len(view_data) == len(axs), "The number of subplots don't match the\
                                        amount of data to plot"

    for i, (_, v) in enumerate(view_data.items()):
        # Testing that there is only one line being plotted
        # for each summary statistic.
        ax = axs[i]
        lines = ax.get_lines()
        assert len(lines) == 1, "There should only be one\
                                line plot per subplot"

        # Testing that the data on the plot
        # is the same as the one from the input.
        line = lines[0]
        line_ydata = line.get_ydata()
        npt.assert_array_equal(
            line_ydata, v,
            err_msg="The y data plotted is different from the one expected"
        )
