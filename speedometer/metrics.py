import time


__all__ = [
    'CountMetric',
    'TimeMetric',
    'BaseMetric',
]


class BaseMetric(object):
    def __init__(self):
        self.cleanup()

    def cleanup(self):
        pass


class CountMetric(BaseMetric):
    def cleanup(self):
        self.count = 0

    def start(self):
        pass

    def finish(self, start):
        self.count += 1

    def get_results(self):
        return self.count


class TimeMetric(BaseMetric):
    timer = time.time

    def cleanup(self):
        self.time = 0.0

    def start(self):
        return self.timer()

    def finish(self, start):
        self.time += self.timer() - start

    def get_results(self):
        return self.time
