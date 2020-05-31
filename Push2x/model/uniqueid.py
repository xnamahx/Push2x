# uncompyle6 version 3.6.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.17 (v2.7.17:c2f86d86e6, Oct 19 2019, 21:01:17) [MSC v.1500 64 bit (AMD64)]
# Embedded file name: c:\Jenkins\live\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\model\uniqueid.py
# Compiled at: 2019-10-13 19:18:15
from __future__ import absolute_import, print_function, unicode_literals
from itertools import count

class UniqueIdMixin(object):
    _idgen = count()

    def __init__(self, *a, **k):
        super(UniqueIdMixin, self).__init__(*a, **k)
        self.__id__ = self._idgen.next()