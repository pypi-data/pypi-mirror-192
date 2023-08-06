import os
import sys
import string
import random

from hashlib import md5
from pyco_utils import (
    _json,
    _coimp,
    _compat,
    _format,
    _subproc,
    co_shutil,
    colog,
    decorators,
    form_data,
    reverify,
    const,
)

from pyco_utils._coimp import (
    print_log,
    reload_module,
    import_file,
    clean_module,
    clean_modules_from_dir,
)

__version__ = '23.2.16'
__module_name = "pyco_utils"


# from . import _json
## fixed: compat with _json.cpython on python>=3.7  
sys.modules["pyco_utils._json"] = _json


def md5sum(content):
    m = md5()
    if not isinstance(content, bytes):
        content = content.encode('utf-8').strip()
    m.update(content)
    s = m.hexdigest().lower()
    return s


def short_uuid(length):
    charset = string.ascii_letters + string.digits
    return ''.join([random.choice(charset) for i in range(length)])


def ensure_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def dirpath(path, depth=1):
    """
    usage: index to source and add to sys.path
    >>> folder = dirpath(__file__, 1)
    >>> sys.path.insert(0, folder)
    """
    path = os.path.abspath(path)
    for i in range(depth):
        path = os.path.dirname(path)
    return path



def get_suffix_num(word: str):
    if not word[-1].isdigit():
        return -1
    elif word.isdecimal():
        return int(word)
    cnt = len(word)
    idx = cnt - 1
    plus = 1
    value = 0
    while word[idx].isdigit() and idx > 0:
        value += int(word[idx]) * plus
        plus *= 10
        idx -= 1
    return value

