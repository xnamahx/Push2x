# uncompyle6 version 3.6.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.17 (v2.7.17:c2f86d86e6, Oct 19 2019, 21:01:17) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\device_util.py
# Compiled at: 2020-01-14 09:08:47
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import liveobj_valid

def is_drum_pad(item):
    return liveobj_valid(item) and isinstance(item, Live.DrumPad.DrumPad)


def find_chain_or_track(item):
    u"""
    Finds a chain for the given item.
    - If it's a device, returns the parent chain or track
    - If it's a drum pad, returns the first chain if it exists, otherwise also the parent
      chain or track
    """
    if is_drum_pad(item) and item.chains:
        chain = item.chains[0]
    else:
        chain = item
        while liveobj_valid(chain) and not isinstance(chain, (Live.Track.Track, Live.Chain.Chain)):
            chain = getattr(chain, 'canonical_parent', None)

    return chain


def find_rack(item):
    u"""
    Finds the parent rack of the given item or None, if it doesn't exist
    """
    rack = item
    while liveobj_valid(rack) and not isinstance(rack, Live.RackDevice.RackDevice):
        rack = getattr(rack, 'canonical_parent', None)

    return rack