import time

try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from speedometer import *


class UsageTest(TestCase):
    def runTest(self):
        self.speedometer.patch_object(self.testable, 'call_me')
        self.testable.call_me()
        stats = self.speedometer.pop_stats()
        self.assertEqual(1, stats.count)
        self.assertGreater(stats.time, 0)

    def setUp(self):
        self.speedometer = Speedometer(MetricComposite(
            time = TimeMetric(),
            count = CountMetric()
        ))
        self.testable = Testable()


class Testable(object):
    result = object()
    SLEEP_MINIMUM_DELAY = 0.000001

    def call_me(self):
        time.sleep(self.SLEEP_MINIMUM_DELAY)
        return self.result

