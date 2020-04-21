import scipy.signal


class MedianBaselineCorrector:
    def __init__(self, med_bc_window_length):
        self.med_bc_window_length = med_bc_window_length

    def apply(self, y):
        mf = MedianFilter(self.med_bc_window_length)
        med_y = mf.apply(y)
        return y - med_y


class SGFilter():
    def __init__(self, window_length, polyorder):
        self.windown_length = window_length
        self.polyorder = polyorder

    def apply(self, data):
        if len(data) < self.windown_length:
            return data
        return scipy.signal.savgol_filter(data, self.windown_length, self.polyorder)


class MedianFilter():
    def __init__(self, filtersize):
        self.filtersize = filtersize

    def apply(self, data):
        return scipy.signal.medfilt(data, self.filtersize)
