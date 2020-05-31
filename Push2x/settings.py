# uncompyle6 version 3.6.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.17 (v2.7.17:c2f86d86e6, Oct 19 2019, 21:01:17) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\settings.py
# Compiled at: 2020-02-05 20:23:22
from __future__ import absolute_import, print_function, unicode_literals
from pushbase.setting import OnOffSetting

def create_settings(preferences=None):
    preferences = preferences if preferences is not None else {}
    return {'workflow': OnOffSetting(name='Workflow', value_labels=[
                  'Scene', 'Clip'], default_value=True, preferences=preferences)}