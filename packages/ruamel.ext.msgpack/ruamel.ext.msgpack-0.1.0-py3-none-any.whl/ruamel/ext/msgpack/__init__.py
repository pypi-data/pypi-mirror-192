# coding: utf-8

from typing import Dict, Any

_package_data: Dict[str, Any] = dict(
    full_package_name='ruamel.ext.msgpack',
    version_info=(0, 1, 0),
    __version__='0.1.0',
    version_timestamp='2023-02-16 16:13:57',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='thin wrapper around msgpack to deal with naive datetime and ruamel'
    ' defined extension types',
    keywords='pypi statistics',
    entry_points='msgpack=ruamel.ext.msgpack.__main__:main',
    # entry_points=None,
    license='Copyright Ruamel bvba 2007-2023',
    since=2023,
    # status='α|β|stable',  # the package status on PyPI
    # data_files="",
    # universal=True,  # py2 + py3
    install_requires=['msgpack>=1.0.4'],
    tox=dict(env='3',),  # *->all p->pypy
    mypy=False,
    python_requires='>=3',
)  # NOQA


version_info = _package_data['version_info']
__version__ = _package_data['__version__']

#################

import struct  # NOQA
import datetime  # NOQA
from functools import partial  # NOQA
import msgpack  # NOQA


class MsgPackDefault:
    def __init__(self):
        self.date = 17

    def __call__(self, obj):
        # date has to come after its subclass datetime.datetime
        # https://docs.python.org/3/library/datetime.html#available-types
        if isinstance(obj, datetime.datetime):
            return obj.replace(tzinfo=datetime.UTC)
        if self.date is not None and isinstance(obj, datetime.date):
            if 2000 < obj.year < 2126:
                yb = (obj.year - 2000) << 9
                month = obj.month - 1
                qb, miqb = divmod(month, 3)
                qb = qb << 7
                miqb = miqb << 5
                dayb = obj.day
                bits = yb | qb | miqb | dayb
                # print(yb, qb, miqb, dayb, bits, f'{bits:4_b}')
                return msgpack.ExtType(self.date, struct.pack('>H', bits))
        else:
            raise ValueError('year out of range 2000-2126')
            return obj
        return obj

    def ext_hook(self, code, data):
        if code == self.date:
            bits = struct.unpack('>H', data)[0]
            return datetime.date(
                year=((bits & 0xFE00) >> 9) + 2000,
                month=((bits & 0x0180) >> 7) * 3 + ((bits & 0x06) >> 5) + 1,
                day=bits & 0x1F,
            )
        return msgpack.ExtType(code, data)


msgpack_default = MsgPackDefault()

pack = partial(msgpack.pack, default=msgpack_default, use_bin_type=False, datetime=True)
packb = partial(msgpack.packb, default=msgpack_default, use_bin_type=False, datetime=True)
unpackb_raw = partial(msgpack.unpackb, strict_map_key=False)
unpackb = partial(
    msgpack.unpackb, ext_hook=msgpack_default.ext_hook, strict_map_key=False, timestamp=3
)


def hex(ba):
    return ''.join(['\\x{:02x}'.format(x) for x in ba])
