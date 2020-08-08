import pytest
from traitlets import HasTraits, TraitError
import numpy as np

from pandas_visual_analysis import DataSource
from pandas_visual_analysis.utils.config import Config
from pandas_visual_analysis.widgets import ScatterWidget
from tests import sample_dataframes


@pytest.fixture(scope="module")
def small_df():
    return sample_dataframes.small_df()


@pytest.fixture(scope="module")
def populated_config():
    config = Config()
    config.alpha = 0.75
    config.select_color = (0, 0, 0)
    config.deselect_color = (0, 0, 0)


def test_on_selection(small_df, populated_config):
    ds = DataSource(small_df, None)
    scatter_widget = ScatterWidget(ds, 0, 0, 1.0, 400)

    def simple_observe(change):
        assert change['old'] == list(range(len(small_df)))
        assert change['new'] == [0]

    HasTraits.observe(ds, simple_observe, '_brushed_indices')

    class Points:
        point_inds= [0]

    scatter_widget.on_selection(None, Points(), None)


def test_on_deselection(small_df, populated_config):
    ds = DataSource(small_df, None)
    original_indices = ds.indices
    scatter_widget = ScatterWidget(ds, 0, 0, 1.0, 400)

    ds.brushed_indices = [0]

    def simple_observe(change):
        assert change['new'] == original_indices

    HasTraits.observe(ds, simple_observe, '_brushed_indices')

    class Points:
        point_inds = [0]

    scatter_widget.on_deselection(Points(), None)


def test_on_axis_x_change(small_df, populated_config):
    ds = DataSource(small_df, None)
    scatter_widget = ScatterWidget(ds, 0, 0, 1.0, 400)

    scatter_widget.x_selection.value = 'e'

    assert list(scatter_widget.figure_widget.data[0].x) == list(small_df['e'])


def test_on_axis_y_change(small_df, populated_config):
    ds = DataSource(small_df, None)
    scatter_widget = ScatterWidget(ds, 0, 0, 1.0, 400)

    scatter_widget.y_selection.value = 'd'

    assert list(scatter_widget.figure_widget.data[0].y) == list(small_df['d'])


def test_on_axis_size_change(small_df, populated_config):
    ds = DataSource(small_df, None)
    scatter_widget = ScatterWidget(ds, 0, 0, 1.0, 400)

    scatter_widget.size_selection.value = 'c'
    assert list(scatter_widget.figure_widget.data[0].marker['size']) == list(small_df['c'])


def test_on_axis_change_size_date_error(small_df, populated_config):
    ds = DataSource(small_df, None)
    scatter_widget = ScatterWidget(ds, 0, 0, 1.0, 400)

    assert 'datetime64' in str(small_df['d'].dtype)
    with pytest.raises(TraitError):  # selection not found
        scatter_widget.size_selection.value = 'd'  # data time not allowed


def test_on_axis_change_bool_date_error(small_df, populated_config):
    ds = DataSource(small_df, None)
    scatter_widget = ScatterWidget(ds, 0, 0, 1.0, 400)

    assert 'bool' in str(small_df['e'].dtype)
    with pytest.raises(TraitError):  # selection not found
        scatter_widget.size_selection.value = 'e'  # bool not allowed


def test_on_axis_change_size_none(small_df, populated_config):
    ds = DataSource(small_df, None)
    scatter_widget = ScatterWidget(ds, 0, 0, 1.0, 400)

    scatter_widget.size_selection.value = 'c'
    scatter_widget.size_selection.value = "None"
    assert scatter_widget.figure_widget.data[0].marker['size'] is None


def test_redraw_plot_with_none(small_df, populated_config):
    ds = DataSource(small_df, None)
    scatter_widget = ScatterWidget(ds, 0, 0, 1.0, 400)
    scatter_widget._redraw_plot(None)
