# uncompyle6 version 3.2.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.1 (v3.7.1:260ec2c36a, Oct 20 2018, 14:57:15) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: c:\Jenkins\live\output\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\device_component_provider.py
# Compiled at: 2018-09-20 16:54:22
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import depends, listenable_property, listens, liveobj_changed
from ableton.v2.control_surface.mode import ModesComponent
from .auto_filter import AutoFilterDeviceComponent
from .compressor import CompressorDeviceComponent
from .echo import EchoDeviceComponent
from .eq8 import Eq8DeviceComponent
from .operator import OperatorDeviceComponent
from .simpler import SimplerDeviceComponent
from .wavetable import WavetableDeviceComponent
from .device_component import GenericDeviceComponent
from .real_time_channel import RealTimeDataComponent
DEVICE_COMPONENT_MODES = {b'Generic': GenericDeviceComponent, 
   b'OriginalSimpler': SimplerDeviceComponent, 
   b'Eq8': Eq8DeviceComponent, 
   b'Compressor2': CompressorDeviceComponent, 
   b'InstrumentVector': WavetableDeviceComponent, 
   b'Operator': OperatorDeviceComponent, 
   b'Echo': EchoDeviceComponent, 
   b'AutoFilter': AutoFilterDeviceComponent}

class DeviceComponentProvider(ModesComponent):
    """
    Provides the currently selected device, its options and parameters
    to other components.
    It has access to the device provider and listens to its device changes.
    When a new device is set, it chooses the right device component that knows how to
    handle behavior specific to the given device.
    """
    __events__ = ('device', )

    @depends(device_provider=None)
    def __init__(self, device_component_layer=None, device_decorator_factory=None, banking_info=None, device_bank_registry=None, device_provider=None, delete_button=None, decoupled_parameter_list_change_notifications=False, *a, **k):
        super(DeviceComponentProvider, self).__init__(*a, **k)
        self._device_provider = device_provider
        self._visualisation_real_time_data = RealTimeDataComponent(channel_type=b'visualisation', parent=self)
        self.__on_visualisation_attached.subject = self._visualisation_real_time_data
        self.__on_visualisation_channel_changed.subject = self._visualisation_real_time_data
        self._device_component_modes = {}
        for mode_name, component_class in DEVICE_COMPONENT_MODES.iteritems():
            self._device_component_modes[mode_name] = component_class(parent=self, device_decorator_factory=device_decorator_factory, banking_info=banking_info, device_bank_registry=device_bank_registry, device_provider=device_provider, name=(b'{}DeviceComponent').format(mode_name), visualisation_real_time_data=self._visualisation_real_time_data, is_enabled=False, delete_button=delete_button, decoupled_parameter_list_change_notifications=decoupled_parameter_list_change_notifications)

        for mode_name, device_component in self._device_component_modes.iteritems():
            self.add_mode(mode_name, [
             device_component,
             (
              device_component, device_component_layer)])

        self.selected_mode = b'Generic'
        self.__on_provided_device_changed.subject = device_provider
        self.__on_provided_device_changed()
        self.__on_selected_track_changed.subject = self.song.view

    def set_device(self, device):
        self._device_provider.device = device

    def _set_device(self, device):
        name = device.class_name if device and device.class_name in self._device_component_modes else b'Generic'
        self.selected_mode = name
        device_component = self._device_component_modes[name]
        self.__on_parameters_changed.subject = device_component
        self.__on_shrink_parameters_changed.subject = device_component
        self.__on_options_changed.subject = device_component
        self.__on_visualisation_visible_changed.subject = device_component
        device_component.set_device(device)
        self.notify_shrink_parameters()
        self._visualisation_real_time_data.set_data(device)

    @property
    def device_component(self):
        return self._device_component_modes[self.selected_mode or b'Generic']

    @listenable_property
    def parameters(self):
        return self.device_component.parameters

    @listenable_property
    def shrink_parameters(self):
        return self.device_component.shrink_parameters

    @listenable_property
    def options(self):
        return self.device_component.options

    def device(self):
        return self.device_component.device()

    def device_changed(self, device):
        current_device = getattr(self.device(), b'_live_object', self.device())
        return liveobj_changed(current_device, device)

    @listens(b'device')
    def __on_provided_device_changed(self):
        device = self._device_provider.device
        if self.device_changed(device):
            self._set_device(device)
            self.notify_device()

    @listens(b'parameters')
    def __on_parameters_changed(self):
        self.notify_parameters()
        self.device_component.parameters_changed()

    @listens(b'shrink_parameters')
    def __on_shrink_parameters_changed(self):
        self.notify_shrink_parameters()

    @listens(b'options')
    def __on_options_changed(self):
        self.notify_options()

    @listens(b'attached')
    def __on_visualisation_attached(self):
        self.device_component.initialize_visualisation_view_data()

    @listens(b'selected_track')
    def __on_selected_track_changed(self):
        self.device_component.initialize_visualisation_view_data()

    @listens(b'channel_id')
    def __on_visualisation_channel_changed(self):
        self.notify_visualisation_real_time_channel_id()

    @listenable_property
    def visualisation_real_time_channel_id(self):
        if self.device_component.visualisation_visible:
            return self._visualisation_real_time_data.channel_id
        return

    @listens(b'visualisation_visible')
    def __on_visualisation_visible_changed(self):
        self.notify_visualisation_real_time_channel_id()

    def disconnect(self):
        super(DeviceComponentProvider, self).disconnect()
        self._visualisation_real_time_data.set_data(None)
        return