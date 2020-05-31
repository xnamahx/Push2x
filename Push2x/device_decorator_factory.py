# uncompyle6 version 3.6.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.17 (v2.7.17:c2f86d86e6, Oct 19 2019, 21:01:17) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\device_decorator_factory.py
# Compiled at: 2020-01-14 09:08:47
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import DeviceDecoratorFactory as DeviceDecoratorFactoryBase
from .auto_filter import AutoFilterDeviceDecorator
from .compressor import CompressorDeviceDecorator
from .device_decoration import SamplerDeviceDecorator, PedalDeviceDecorator, DrumBussDeviceDecorator, UtilityDeviceDecorator
from .delay import DelayDeviceDecorator
from .echo import EchoDeviceDecorator
from .eq8 import Eq8DeviceDecorator
from .operator import OperatorDeviceDecorator
from .simpler import SimplerDeviceDecorator
from .wavetable import WavetableDeviceDecorator

class DeviceDecoratorFactory(DeviceDecoratorFactoryBase):
    DECORATOR_CLASSES = {'OriginalSimpler': SimplerDeviceDecorator, 
       'Operator': OperatorDeviceDecorator, 
       'MultiSampler': SamplerDeviceDecorator, 
       'AutoFilter': AutoFilterDeviceDecorator, 
       'Eq8': Eq8DeviceDecorator, 
       'Compressor2': CompressorDeviceDecorator, 
       'Pedal': PedalDeviceDecorator, 
       'DrumBuss': DrumBussDeviceDecorator, 
       'Echo': EchoDeviceDecorator, 
       'InstrumentVector': WavetableDeviceDecorator, 
       'StereoGain': UtilityDeviceDecorator, 
       'Delay': DelayDeviceDecorator}