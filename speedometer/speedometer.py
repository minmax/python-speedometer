from functools import wraps
from threading import Lock
import logging


__all__ = [
    'Speedometer',
]


class Speedometer(object):
    logger = logging.getLogger('speedometer')

    def __init__(self, metric, debug=__debug__):
        self.metric = metric
        self._lock = Lock()
        self.debug = debug

    def patch_object(self, original, *method_names):
        for name in method_names:
            setattr(
                original,
                name,
                self.create_method_wrapper(original, name)
            )

    def create_method_wrapper(self, original, name):
        original_method = getattr(original, name)

        @wraps(original_method)
        def wrapper(*args, **kwargs):
            metric_start = self.metric.start()
            try:
                return original_method(*args, **kwargs)
            finally:
                if self.debug:
                    self._update_metric(metric_start)
                else:
                    self._safely_update_metric(metric_start)
        return wrapper

    def _safely_update_metric(self, metric_start):
        try:
            self._update_metric(metric_start)
        except Exception:
            try:
                self.logger.exception('Cant update metric')
            except Exception:
                pass

    def _update_metric(self, metric_start):
        with self._lock:
            self.metric.finish(metric_start)

    def pop_stats(self):
        with self._lock:
            result = self.metric.get_results()
            self.metric.cleanup()
        return result
