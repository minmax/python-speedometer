try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from mock import Mock

from speedometer.speedometer import Speedometer


class SpeedometerTest(TestCase):
    def test_wrapped_method_called(self):
        self.original.method()
        self.assertTrue(self.mock.called)

    def test_drop_stats_after_check(self):
        self.original.method()
        self.assertIs(self.metric_result, self.speedometer.pop_stats())
        self.assertIsNone(self.speedometer.pop_stats())

    def test_safely_finalize_metric_in_not_debug(self):
        self.metric.raise_exception = True
        self.speedometer.debug = False
        self.original.method()

    def test_raise_exception_in_debug(self):
        self.metric.raise_exception = True
        with self.assertRaises(Exception):
            self.original.method()

    class Original(object):
        def __init__(self, function):
            self.function = function

        def method(self):
            return self.function()

    def setUp(self):
        self.mock = Mock()
        self.original = self.Original(self.mock)
        self.metric_result = object()
        self.metric = TestMetric(self.metric_result)
        self.speedometer = Speedometer(metric=self.metric)
        self.speedometer.patch_object(self.original, 'method')


class TestMetric(object):
    def __init__(self, result):
        self.result = result
        self.cleaned = False
        self.start_hook = object()
        self.raise_exception = False

    def start(self):
        return self.start_hook

    def finish(self, start_value):
        assert start_value is self.start_hook
        if self.raise_exception:
            raise Exception()

    def cleanup(self):
        self.cleaned = True
        self.result = None

    def get_results(self):
        return self.result
