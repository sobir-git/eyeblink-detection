from time import time
import json


class DataLogger:
    def __init__(self, columns):
        self.timestamps = []
        self.columns = columns
        self.data = {c: [] for c in columns}
        self.timestamps = {c: [] for c in columns}

    def log(self, value, column, timestamp=None):
        if timestamp is None:
            timestamp = time()

        timestamps = self.timestamps[column]
        data = self.data[column]

        # append new data
        data.append(value)
        timestamps.append(timestamp)

    def get_last_n_seconds(self, n, column):
        now = time()
        data = self.data[column]
        timestamps = self.timestamps[column]

        i = len(data)
        while i >= 1 and now - timestamps[i - 1] < n:
            i = i - 1

        return data[i:], timestamps[i:]

    def save(self, path):
        with open(path, 'w') as f:
            json.dump({'data': self.data, 'timestamps': self.timestamps}, f, indent=2)
