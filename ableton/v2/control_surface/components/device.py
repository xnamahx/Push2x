# uncompyle6 version 3.2.5
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.1 (v3.7.1:260ec2c36a, Oct 20 2018, 14:57:15) [MSC v.1915 64 bit (AMD64)]
# Embedded file name: c:\Jenkins\live\output\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\components\device.py
# Compiled at: 2018-09-20 16:54:22
from __future__ import absolute_import, print_function, unicode_literals
from ...base import depends, listens, liveobj_valid, liveobj_changed
from ...control_surface import Component, ParameterProvider, create_device_bank
from ...control_surface.simpler_slice_nudging import SimplerSliceNudging


class DeviceComponent(ParameterProvider, Component):
    """
    Device component that serves as parameter provider for the
    DeviceParameterComponent.
    """
    __events__ = ('device', )
    _provided_parameters = tuple()
    class_name = 'DeviceComponent'

    @depends(device_provider=None)
    def __init__(self, device_decorator_factory=None, banking_info=None, device_bank_registry=None, device_provider=None, decoupled_parameter_list_change_notifications=False, *a, **k):
        self._bank = None
        self._lock_button = None
        self._lock_callback = None
        self._locked_to_device = False
        self._banking_info = banking_info
        self._decorated_device = None
        self._decorator_factory = device_decorator_factory
        self._device_provider = device_provider
        self._device_bank_registry = device_bank_registry
        self._parameters_dirty = True
        self._decoupled_parameter_list_change_notifications = decoupled_parameter_list_change_notifications
        super(DeviceComponent, self).__init__(*a, **k)
        self._initialize_subcomponents()
        self.__on_provided_device_changed.subject = device_provider
        self.__on_provided_device_changed()
        def make_button_slot(name):
            return self.register_slot(None, getattr(self, '_%s_value' % name), 'value')
        self._lock_button_slot = make_button_slot('lock')
        return

    def set_device(self, device):
        self._device_provider.device = device

    def device(self):
        return self._decorated_device

    def _initialize_subcomponents(self):
        self._slice_nudging = self.register_disconnectable(SimplerSliceNudging())

    @property
    def parameters(self):
        return self._provided_parameters

    @listens(b'device_bank')
    def __on_bank_changed(self, device, bank):
        if device == self.device():
            self._set_bank_index(bank)

    def _set_bank_index(self, bank):
        if self._bank is not None:
            self._bank.index = bank
        return

    def _update_parameters(self):
        self._parameters_dirty = True
        if not self._decoupled_parameter_list_change_notifications:
            self.update_and_notify_parameters()

    def update_and_notify_parameters(self):
        """
        This should either be called by _update_parameters or as a public method
        in the case that the parameter list change notifications are decoupled.
        
        For example, Push can potentially call this method every 100 ms when
        notifications are decoupled, and changes to the parameter list will not
        be notified immediately.
        """
        if self._parameters_dirty:
            self._provided_parameters = self._get_provided_parameters()
            self.notify_parameters()
            self._parameters_dirty = False

    def _setup_bank(self, device, bank_factory=create_device_bank):
        if self._bank is not None:
            self.disconnect_disconnectable(self._bank)
            self._bank = None
        if liveobj_valid(device):
            self._bank = self.register_disconnectable(bank_factory(device, self._banking_info))
        return

    def _get_decorated_device(self, device):
        if self._decorator_factory is not None:
            return self._decorator_factory.decorate(device)
        return device

    def _device_changed(self, device):
        current_device = getattr(self.device(), b'_live_object', self.device())
        return liveobj_changed(current_device, device)

    @listens(b'device')
    def __on_provided_device_changed(self):
        self._on_device_changed(self._device_provider.device)

    @listens(b'parameters')
    def __on_parameters_changed_in_device(self):
        self._update_parameters()

    def _on_device_changed(self, device):
        if self._device_changed(device):
            self._set_device(device)

    def _set_decorated_device(self, decorated_device):
        self._set_decorated_device_for_subcomponents(decorated_device)
        self._setup_bank(decorated_device)
        self._on_bank_parameters_changed.subject = self._bank
        self._decorated_device = decorated_device

    def _set_device(self, device):
        self._set_device_for_subcomponents(device)
        decorated_device = self._get_decorated_device(device)
        self._set_decorated_device(decorated_device)
        device_bank_registry = self._device_bank_registry
        self.__on_bank_changed.subject = device_bank_registry
        bank_index_for_device = device_bank_registry.get_device_bank(device)
        self._set_bank_index(bank_index_for_device)
        self.notify_device()
        self._update_parameters()
        self.__on_parameters_changed_in_device.subject = device

    def _set_device_for_subcomponents(self, device):
        pass

    def _set_decorated_device_for_subcomponents(self, decorated_device):
        self._slice_nudging.set_device(decorated_device)

    @listens(b'parameters')
    def _on_bank_parameters_changed(self):
        self._update_parameters()

    def _current_bank_details(self):
        if self._bank is not None:
            return (self._bank.name, self._bank.parameters)
        return (
         b'', [None] * 8)

    def _number_of_parameter_banks(self):
        if self._bank is not None:
            return self._bank.bank_count()
        return 0

    def _get_provided_parameters(self):
        _, parameters = self._current_bank_details() if self.device() else (None, ())
        return [ self._create_parameter_info(param, name) for param, name in parameters ]

    def _create_parameter_info(self, parameter, name):
        raise NotImplementedError()

    def set_lock_button(self, button):
        self._lock_button = button
        self._lock_button_slot.subject = button
        return

    def set_lock_callback(self, callback):
        self._lock_callback = callback

    def _lock_value(self, value):
        assert self._lock_button != None
        assert value != None
        assert isinstance(value, int)
        if not self._lock_button.is_momentary() or value is not 0:
            if self._locked_to_device:
                self._locked_to_device = False
            else:
                self._locked_to_device = True
            #self._lock_callback()
        return