""" TODO: ae.kivy_help unit tests. """
from ae.kivy_help import AbsolutePosSizeBinder, Tooltip, HelpToggler, TourOverlay


def test_widget_declaration():
    """ we need at least one test to prevent pytest exit code 5 (no tests collected) """
    assert AbsolutePosSizeBinder
    assert Tooltip
    assert HelpToggler
    assert TourOverlay
