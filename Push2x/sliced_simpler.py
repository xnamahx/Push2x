# uncompyle6 version 3.6.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.17 (v2.7.17:c2f86d86e6, Oct 19 2019, 21:01:17) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\sliced_simpler.py
# Compiled at: 2020-01-14 09:08:47
from __future__ import absolute_import, print_function, unicode_literals
from pushbase.colors import Pulse
from pushbase.sliced_simpler_component import SlicedSimplerComponent
from .colors import IndexedColor
NEXT_SLICE_PULSE_SPEED = 48

def next_slice_color(track_color_index):
    return Pulse(color1=IndexedColor.from_live_index(track_color_index, shade_level=2), color2=IndexedColor.from_live_index(track_color_index, shade_level=1), speed=NEXT_SLICE_PULSE_SPEED)


class Push2SlicedSimplerComponent(SlicedSimplerComponent):

    def _next_slice_color(self):
        return next_slice_color(self.song.view.selected_track.color_index)