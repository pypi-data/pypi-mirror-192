import os
import sys
import json
import shutil
import datetime
from time import time
from pprint import pformat


def _sys_insert_module_path(imp=__file__, depth=2):
    if os.path.isdir(imp):
        curdir = os.path.abspath(imp)
    else:
        curdir = os.path.abspath(os.path.dirname(imp))
    pardir = curdir
    while depth > 1:
        pardir = os.path.abspath(os.path.join(pardir, '..'))
        sys.path.insert(0, pardir)
        print("add pardir:", pardir)
        depth -= 1
    sys.path.insert(0, curdir)
    print("add curdir:", curdir)


def get_current_info(data=None, **kwargs):
    now = datetime.datetime.now()
    info = OrderedDict(
        _cwd=os.getcwd(),
        _pid=os.getpid(),
        _ppid=os.getppid(),
        _python_path=sys.executable,
        _python_version=sys.version,
        _sys_args=list(sys.argv),
        _created_at=str(now),
        _created_ts=int(time())
    )
    info.update(kwargs)
    return info


def _gen_gitprj_paths(absolute_dir: str, max_depth=-1, limit=1):
    """
    :param absolute_dir:
    :param max_depth: -1 无限
    :param limit: -1 无限
    :return:
    """
    git_dir = os.path.join(absolute_dir, ".git")
    pardir = os.path.dirname(absolute_dir)
    max_depth -= 1
    if os.path.isdir(git_dir):
        yield absolute_dir
        limit -= 1
    if limit and max_depth and pardir != "/":
        yield from _gen_gitprj_paths(pardir, max_depth=max_depth, limit=limit)


def sys_auto_add_paths(current_dir, max_depth=-1, limit=-1):
    if not os.path.isfile(current_dir):
        abs_dir = os.path.abspath(os.path.dirname(current_dir))
    else:
        abs_dir = os.path.abspath(current_dir)
    print_log("dir0:", abs_dir)
    ps = list(_gen_gitprj_paths(abs_dir, max_depth, limit))
    ps.append(abs_dir)
    cnt = len(ps)
    for i, p in ps[::-1]:
        print_log("[sys.path]", cnt - i, p)
        sys.path.insert(0, p)
    return ps


##############################################################
##############################################################
import logging
from logging.handlers import RotatingFileHandler
from collections import OrderedDict
from pyco_utils.colog import getLogger
from pyco_utils._json import CustomJSONEncoder

glogger = logging.getLogger()  # type: logging.Logger
g_default_logfile = ""
NowStr = lambda fmt="%Y-%m-%d_%H%M": datetime.datetime.now().strftime(fmt)
K_LogFileSets = set()


# def get_logger(logger_name, auto_strip=True, set_as_global=False, logdir="logs", stdout=True, logfile=None):
def get_glogger_file():
    hdls = glogger.handlers
    for i, hdl in enumerate(hdls):
        if isinstance(hdl, RotatingFileHandler):
            return hdl.baseFilename


def rename_glogger_file(new_log_file=None, replace=True):
    from pyco_utils.colog import rotating_file_hdl
    new_log_file2 = os.path.abspath(new_log_file)
    hdls = glogger.handlers
    for i, hdl in enumerate(hdls):
        if isinstance(hdl, RotatingFileHandler):
            logfp = hdl.baseFilename
            if logfp == new_log_file2:
                pass
            elif not os.path.isdir(new_log_file2):
                hdl.close()
                if not os.path.exists(new_log_file2) or replace:
                    shutil.move(logfp, new_log_file2)
                glogger.handlers[i] = rotating_file_hdl(logfile=new_log_file2)
                print_log(f"rename logfile: {logfp} = > {new_log_file2}")
            else:
                hdl.close()
                hdls.remove(hdl)
            break


def get_logger(logger_name, auto_strip=True, set_as_global=False, logdir="./logs", logfile=None, **kwargs):
    if auto_strip:
        logger_name = os.path.basename(logger_name).split(".")[0].split("_")[-1]
    now = NowStr()
    # logdir = kwargs.get("logdir", K_LogDir)
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    if logfile is None:
        logfile = os.environ.get(
            "YJ_LOGFILE_DEFAULT",
            f"YJ_{logger_name}.{now}.{os.getpid()}.bak.log"
        )
    if logdir:
        logfile = os.path.join(logdir, logfile)

    logfile = os.path.abspath(logfile)
    logdir2 = os.path.dirname(logfile)
    if not os.path.exists(logdir2):
        os.makedirs(logdir2, exist_ok=True)

    kwargs.setdefault("stdout", True)
    kwargs.setdefault("logfile", logfile)
    logger2 = getLogger(logger_name, **kwargs)

    setattr(logger2, "yj_logfile", logfile)
    if logfile not in K_LogFileSets:
        logger2.info(f"add LogFile: {logger_name} ({logfile})")
        K_LogFileSets.add(logfile)

    global glogger
    global g_default_logfile
    if set_as_global and glogger is not logger2:
        default_logfile = os.environ.setdefault("YJ_LOGFILE_DEFAULT", logfile)
        logger2.info(f"glogger => {logger_name} ({logfile}), default_logfile: {default_logfile}")
        logger2.info(f"[entry]: {sys.argv}")
        glogger = logger2
        g_default_logfile = default_logfile

    return logger2


def _glog(*args, stacklevel=2, log_level=50, **kwargs):
    """
    :param log_level: 
        CRITICAL = 50
        FATAL = CRITICAL
        ERROR = 40
        WARNING = 30
        WARN = WARNING
        INFO = 20
        DEBUG = 10
        NOTSET = 0
    """
    # _log(*args, **kwargs, logger_name=logger.name, level=50, stacklevel=3)
    # logger = getLogger(logger_name, **kwargs)
    result = kwargs.pop('result', None)
    sep = ", "
    msg = sep.join(map(format_v2, args))
    if kwargs:
        msg += "\n" + pformat(kwargs, indent=2, width=120)
    if result is not None:
        msg += '\n[result] : \n\t{}'.format("\n\t".join(result.split("\n")))
    if msg:
        if sys.version_info > (3, 8, 0):
            ## Changed in version 3.8: The stacklevel parameter was added.
            glogger.log(log_level, msg, stacklevel=stacklevel)
        elif msg:
            glogger.log(log_level, msg)


def format_v2(v):
    if v is None:
        return str(v)
    elif isinstance(v, (int, str, bytes, bool, float, datetime.datetime)):
        return str(v)
    elif isinstance(v, (tuple, list, dict, set)):
        return pformat(v)
    else:
        return format_any(v)


def format_any(v, depth=2):
    return " :: ".join([str(type(v)), pformat(v, indent=4, width=80, depth=depth)])


def format_json(data, cls=CustomJSONEncoder, indent=2, ensure_ascii=False, **kwargs):
    return json.dumps(data, cls=cls, indent=indent, ensure_ascii=ensure_ascii, **kwargs)


def save_file(filename: str, data, indent=2, mode="w", _stdout=False, _cache_if_failed=True, **kwargs):
    fext = filename.rsplit('.', 1)[-1]
    if fext.startswith("json"):
        if isinstance(data, bytes):
            data = data.decode()
        elif not isinstance(data, str):
            data = format_json(data, indent=indent, **kwargs)

    try:
        with open(filename, mode) as fw:
            fw.write(data)
            size = fw.tell()
        print_log(f"output@{fext}:", filename, size)

    except Exception as e:
        fp2 = "_cached.bak.{}".format(os.path.basename(filename))
        with open(fp2, mode) as fw:
            fw.write(data)
            size = fw.tell()
        print_log(e)
        print_log(f"CACHED@{fext}:", filename, size)
    if _stdout:
        print_log(data)
    return fext, size


####################################################
####################################################
def _get_print_log():
    global glogger
    env_k = "YJCO_PRINT_LOG"
    env_v = os.environ.get(env_k, "log")
    if env_v in ["ignored", "no", "No", "disabled", "false", "False"]:
        def _print_log(*args, **kwargs):
            pass

        print(f'[ENV] ${env_k} = "{env_v}", logger is ignored')
        return _print_log

    elif env_v == "log":
        try:
            gLogDir = os.environ.setdefault("YJ_LOG_DIR", "./logs")
            glogger = get_logger("YJLog", set_as_global=True, logdir=gLogDir)

            def _print_log(*args, stacklevel=4, **kwargs):
                _glog(*args, **kwargs, stacklevel=stacklevel)

            _print_log(f"init Logger: {glogger.name}", glogger, glogger.handlers)
            return _print_log
        except Exception as e:
            print("failed", e)

    glogger = logging.getLogger()
    print(f'[ENV] ${env_k} = "{env_v}"', glogger)

    def _print_log(*args, **kwargs):
        print(*args, kwargs)

    return _print_log


print_log = _get_print_log()

