#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: DSDcc receiver
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
import math
from gnuradio import audio
from gnuradio import dsdcc
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
import sip



class rtlsdr_rx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "DSDcc receiver", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("DSDcc receiver")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "rtlsdr_rx")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.dsd_in_rate = dsd_in_rate = 48000
        self.decimation_2 = decimation_2 = 4
        self.decimation_1 = decimation_1 = 10
        self.samp_rate = samp_rate = decimation_1 * decimation_2 * dsd_in_rate
        self.if_rate = if_rate = decimation_2 * dsd_in_rate
        self.squelch_threshold = squelch_threshold = -25
        self.offset = offset = 100e3
        self.low_pass_taps = low_pass_taps = firdes.low_pass(1.0, samp_rate, if_rate * 0.4,if_rate * 0.2, window.WIN_HAMMING, 6.76)
        self.fsk_deviation_hz = fsk_deviation_hz = 1944 * 4
        self.freq = freq = 441.000e6
        self.dsd_out_rate = dsd_out_rate = 8000

        ##################################################
        # Blocks
        ##################################################

        self._squelch_threshold_range = qtgui.Range(-50, 0, 1, -25, 200)
        self._squelch_threshold_win = qtgui.RangeWidget(self._squelch_threshold_range, self.set_squelch_threshold, "Squelch threshold", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._squelch_threshold_win)
        self._freq_msgdigctl_win = qtgui.MsgDigitalNumberControl(lbl='Frequency', min_freq_hz=30e6, max_freq_hz=1000e6, parent=self, thousands_separator=",", background_color="black", fontColor="white", var_callback=self.set_freq, outputmsgname='freq')
        self._freq_msgdigctl_win.setValue(441.000e6)
        self._freq_msgdigctl_win.setReadOnly(False)
        self.freq = self._freq_msgdigctl_win

        self.top_layout.addWidget(self._freq_msgdigctl_win)
        self.soapy_rtlsdr_source_0 = None
        dev = 'driver=rtlsdr'
        stream_args = 'bufflen=16384'
        tune_args = ['']
        settings = ['']

        def _set_soapy_rtlsdr_source_0_gain_mode(channel, agc):
            self.soapy_rtlsdr_source_0.set_gain_mode(channel, agc)
            if not agc:
                  self.soapy_rtlsdr_source_0.set_gain(channel, self._soapy_rtlsdr_source_0_gain_value)
        self.set_soapy_rtlsdr_source_0_gain_mode = _set_soapy_rtlsdr_source_0_gain_mode

        def _set_soapy_rtlsdr_source_0_gain(channel, name, gain):
            self._soapy_rtlsdr_source_0_gain_value = gain
            if not self.soapy_rtlsdr_source_0.get_gain_mode(channel):
                self.soapy_rtlsdr_source_0.set_gain(channel, gain)
        self.set_soapy_rtlsdr_source_0_gain = _set_soapy_rtlsdr_source_0_gain

        def _set_soapy_rtlsdr_source_0_bias(bias):
            if 'biastee' in self._soapy_rtlsdr_source_0_setting_keys:
                self.soapy_rtlsdr_source_0.write_setting('biastee', bias)
        self.set_soapy_rtlsdr_source_0_bias = _set_soapy_rtlsdr_source_0_bias

        self.soapy_rtlsdr_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)

        self._soapy_rtlsdr_source_0_setting_keys = [a.key for a in self.soapy_rtlsdr_source_0.get_setting_info()]

        self.soapy_rtlsdr_source_0.set_sample_rate(0, samp_rate)
        self.soapy_rtlsdr_source_0.set_frequency(0, (freq - offset))
        self.soapy_rtlsdr_source_0.set_frequency_correction(0, 0)
        self.set_soapy_rtlsdr_source_0_bias(bool(False))
        self._soapy_rtlsdr_source_0_gain_value = 20
        self.set_soapy_rtlsdr_source_0_gain_mode(0, bool(True))
        self.set_soapy_rtlsdr_source_0_gain(0, 'TUNER', 20)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            (int(dsd_in_rate * 0.060)), #size
            dsd_in_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.01)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            if_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.01)
        self.qtgui_freq_sink_x_0.set_y_axis((-100), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            decimation_2,
            firdes.low_pass(
                1,
                if_rate,
                10000,
                5000,
                window.WIN_HAMMING,
                6.76))
        self.freq_xlating_fft_filter_ccc_0 = filter.freq_xlating_fft_filter_ccc(decimation_1, low_pass_taps, offset, samp_rate)
        self.freq_xlating_fft_filter_ccc_0.set_nthreads(1)
        self.freq_xlating_fft_filter_ccc_0.declare_sample_delay(0)
        self.dsdcc_dsdcc_block_0 = dsdcc.dsdcc_block(dsdcc.DSDDecodeAuto)
        self.audio_sink_0 = audio.sink(dsd_out_rate, '', True)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf((dsd_in_rate/(2*math.pi*fsk_deviation_hz)))
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc(squelch_threshold, (1e-3), 0, False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.dsdcc_dsdcc_block_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.dsdcc_dsdcc_block_0, 1), (self.audio_sink_0, 1))
        self.connect((self.dsdcc_dsdcc_block_0, 0), (self.audio_sink_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_pwr_squelch_xx_0, 0))
        self.connect((self.soapy_rtlsdr_source_0, 0), (self.freq_xlating_fft_filter_ccc_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "rtlsdr_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_dsd_in_rate(self):
        return self.dsd_in_rate

    def set_dsd_in_rate(self, dsd_in_rate):
        self.dsd_in_rate = dsd_in_rate
        self.set_if_rate(self.decimation_2 * self.dsd_in_rate)
        self.set_samp_rate(self.decimation_1 * self.decimation_2 * self.dsd_in_rate)
        self.analog_quadrature_demod_cf_0.set_gain((self.dsd_in_rate/(2*math.pi*self.fsk_deviation_hz)))
        self.qtgui_time_sink_x_0.set_samp_rate(self.dsd_in_rate)

    def get_decimation_2(self):
        return self.decimation_2

    def set_decimation_2(self, decimation_2):
        self.decimation_2 = decimation_2
        self.set_if_rate(self.decimation_2 * self.dsd_in_rate)
        self.set_samp_rate(self.decimation_1 * self.decimation_2 * self.dsd_in_rate)

    def get_decimation_1(self):
        return self.decimation_1

    def set_decimation_1(self, decimation_1):
        self.decimation_1 = decimation_1
        self.set_samp_rate(self.decimation_1 * self.decimation_2 * self.dsd_in_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_low_pass_taps(firdes.low_pass(1.0, self.samp_rate, self.if_rate * 0.4, self.if_rate * 0.2, window.WIN_HAMMING, 6.76))
        self.soapy_rtlsdr_source_0.set_sample_rate(0, self.samp_rate)

    def get_if_rate(self):
        return self.if_rate

    def set_if_rate(self, if_rate):
        self.if_rate = if_rate
        self.set_low_pass_taps(firdes.low_pass(1.0, self.samp_rate, self.if_rate * 0.4, self.if_rate * 0.2, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.if_rate, 10000, 5000, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, self.if_rate)

    def get_squelch_threshold(self):
        return self.squelch_threshold

    def set_squelch_threshold(self, squelch_threshold):
        self.squelch_threshold = squelch_threshold
        self.analog_pwr_squelch_xx_0.set_threshold(self.squelch_threshold)

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.freq_xlating_fft_filter_ccc_0.set_center_freq(self.offset)
        self.soapy_rtlsdr_source_0.set_frequency(0, (self.freq - self.offset))

    def get_low_pass_taps(self):
        return self.low_pass_taps

    def set_low_pass_taps(self, low_pass_taps):
        self.low_pass_taps = low_pass_taps
        self.freq_xlating_fft_filter_ccc_0.set_taps(self.low_pass_taps)

    def get_fsk_deviation_hz(self):
        return self.fsk_deviation_hz

    def set_fsk_deviation_hz(self, fsk_deviation_hz):
        self.fsk_deviation_hz = fsk_deviation_hz
        self.analog_quadrature_demod_cf_0.set_gain((self.dsd_in_rate/(2*math.pi*self.fsk_deviation_hz)))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq, self.if_rate)
        self.soapy_rtlsdr_source_0.set_frequency(0, (self.freq - self.offset))

    def get_dsd_out_rate(self):
        return self.dsd_out_rate

    def set_dsd_out_rate(self, dsd_out_rate):
        self.dsd_out_rate = dsd_out_rate




def main(top_block_cls=rtlsdr_rx, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
