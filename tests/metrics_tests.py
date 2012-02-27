try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from speedometer.metrics import CountMetric, TimeMetric


class BaseMetricTest(TestCase):
    metric_cls = NotImplemented

    def call_ones(self):
        result = self.metric.start()
        self.metric.finish(result)

    def setUp(self):
        if not self._is_base_class():
            self.metric = self.metric_cls()

    def _is_base_class(self):
        return type(self) is BaseMetricTest


class CountMetricTest(BaseMetricTest):
    metric_cls = CountMetric

    def test_inc_counter(self):
        self.call_ones()
        self.assertEqual(1, self.metric.get_results())

    def test_cleanup_counter(self):
        self.call_ones()
        self.metric.cleanup()
        self.assertEqual(0, self.metric.get_results())


class TimeMetricTest(BaseMetricTest):
    metric_cls = TimeMetric

    def test_inc_time(self):
        self.call_ones()
        self.assertEqual(2, self.metric.get_results())

    def test_cleanup_counter(self):
        self.call_ones()
        self.metric.cleanup()
        self.assertEqual(0, self.metric.get_results())

    def setUp(self):
        super(TimeMetricTest, self).setUp()
        self.times = [3, 5]
        self.metric.timer = self._timer

    def _timer(self):
        return self.times.pop(0)
