import scipy.signal
import numpy as np
import matplotlib.pyplot as plt

from signal_preprocessing import SGFilter, MedianBaselineCorrector


class PeakFinder():
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def find(self, x, y):
        peaks, props = scipy.signal.find_peaks(y, **self.kwargs)
        return peaks, props


def plot_peaks(peaks, props, x, y, axes=None):
    axes = axes or plt.gca()
    axes.plot(x[peaks], y[peaks], "x")

    axes.vlines(x=x[peaks], ymin=y[peaks] - props["prominences"],
                ymax=y[peaks], color="C1")

    # import pdb; pdb.set_trace()
    left_ips = [int(round(x)) for x in props['left_ips']]
    right_ips = [int(round(x)) for x in props['right_ips']]
    axes.hlines(y=props["width_heights"], xmin=x[left_ips],
                xmax=x[right_ips], color="C1")


class BlinkDetector:
    peak_finder = PeakFinder(prominence=0.03, wlen=29, width=(3, 16))
    preprocessors = [
        SGFilter(window_length=7, polyorder=2),
        MedianBaselineCorrector(med_bc_window_length=31)
    ]
    _update_plot_every = 10
    _plot_update_cnt = 0

    def __init__(self, time_window=2.0, frame_delay=5, plot=True):
        self._time_window = time_window
        self.frame_delay = frame_delay

        self.data = []
        self.timestamps = []
        self._last_blink_end_time = -1

        self._plot = plot
        if self._plot:
            fig = plt.figure("Graph")
            self.ax1 = fig.add_subplot(2, 1, 1)
            self.ax2 = fig.add_subplot(2, 1, 2)

            plt.ion()

    def send(self, value, timestamp):
        # add new values
        self.data.append(value)
        self.timestamps.append(timestamp)

        # delete values that are too old
        if len(self.timestamps) > 0:
            earliest_time = self.timestamps[0]
            while timestamp - earliest_time > self._time_window:
                del self.data[0]
                del self.timestamps[0]
                earliest_time = self.timestamps[0]

    def get_blink(self):
        '''Returns blink time and duration'''
        x = np.array(self.timestamps)
        y = -np.array(self.data)
        self._plot_update_cnt += 1
        if self._plot and self._plot_update_cnt % self._update_plot_every == 0:
            self.ax2.clear()
            self.ax2.plot(x, y)
            self.ax2.set_title('Original signal')

        # preprocess data
        for p in self.preprocessors:
            y = p.apply(y)
        peaks, peak_props = self.peak_finder.find(x[:-self.frame_delay], y[:-self.frame_delay])

        # plot graph
        if self._plot and self._plot_update_cnt % self._update_plot_every == 0:
            self.ax1.clear()
            self.ax1.plot(x, y)
            self.ax1.set_ylim(-0.02, 0.06)
            self.ax1.set_title('Processed signal')

            plt.xticks(range(int(x[0]), int(x[-1] + 1)))

            # plot peaks
            plot_peaks(peaks, peak_props, x, y, axes=self.ax1)
            plt.draw()
            plt.pause(0.001)

        if len(peaks) == 0:
            return

        peak_index = peaks[-1]
        peak_time = self.timestamps[peak_index]
        if peak_time > self._last_blink_end_time:
            right_base = self.timestamps[peak_props['right_bases'][-1]]
            left_base = self.timestamps[peak_props['left_bases'][-1]]
            peak_width = right_base - left_base
            self._last_blink_end_time = right_base
            return peak_time, peak_width
