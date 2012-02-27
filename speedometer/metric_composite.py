from itertools import izip
from operator import methodcaller


__all__ = [
    'MetricComposite',
]


class MetricsResults(object):
    def __init__(self, results):
        self.__dict__.update(results)


class MetricComposite(object):
    def __init__(self, **metrics):
        self.metrics_by_names = metrics
        self.metrics_object = metrics.values() # used as sorted dict values

    def get_results(self, as_dict=False):
        results = self._get_results_dict()
        if not as_dict:
            results = MetricsResults(results)
        return results

    def _get_results_dict(self):
        results = {}
        for name, metric in self.metrics_by_names.iteritems():
            results[name] = metric.get_results()
        return results

    def start(self):
        return map(methodcaller('start'), self.metrics_object)

    def finish(self, start_values):
        for value, metric in izip(start_values, self.metrics_object):
            metric.finish(value)

    def cleanup(self):
        for metric in self.metrics_object:
            metric.cleanup()
