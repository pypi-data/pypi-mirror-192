import logging
import os
import sys
from io import IOBase

from pyco_utils._helper import glogger

G_Flag_Mocked = "_is_mocked::pyco_utils.co_mock"

class MockStdout():
    """ mock sys.stdout, customize `print`
    ### 原始的 sys.stdout 是 "<_io.TextIOWrapper name='<stdout>' mode='w' encoding='UTF-8'>"
    ### 使用 MockStdout, 可以让 print 函数的输出，全部重定向到自定义的 logger 或文件(log_fd)里。
    ### 使用场景：
            有时候，拿到了别人的代码，如果原始的 stdout过多，就不好调试。
            这时候，直接改别人的源码，不一定是个好选择。
            不如，把系统的 print 直接 mock 掉。
    import sys
    sys.stdout = MockStdout()
    """

    def __init__(self, fd=None, use_glogger=False, stdout=True):
        self._sys_stdout = sys.stdout
        if not fd:
            if use_glogger:
                fd = glogger
            else:
                fd = os.environ.setdefault("YJ_LOGFILE_DEFAULT", "YJ_STDOUT.log")
        if isinstance(fd, IOBase):
            self._log_fd = fd
            self._log_file = getattr(fd, "name", str(fd))
        elif isinstance(fd, logging.Logger):
            self._log_fd = fd.handlers[-1].stream.buffer  # type: io.BufferedIOBase
            self._log_file = getattr(self._log_fd, "name", str(fd))
        else:
            self._log_file = fd
            self._log_fd = open(str(fd), "a")

        self._mode = self._log_fd.mode
        if "b" in self._mode:
            self.write = self._write_bytes
        else:
            self.write = self._write

    def _write(self, text: str):
        self._sys_stdout.write(text)
        self._log_fd.write(text)
        self.flush()

    def _write_bytes(self, text: str):
        self._sys_stdout.write(text)
        self._log_fd.write(text.encode())
        self.flush()

    def flush(self):
        self._sys_stdout.flush()
        self._log_fd.flush()

    @classmethod
    def mock_sys_stdout(cls, fd=None, use_glogger=False):
        cls.reset_sys_stdout()
        sys.stdout = cls(fd=fd, use_glogger=use_glogger)
        print(f"mock sys.stdout=> {fd} => {sys.stdout._log_file}")
        return sys.stdout

    @classmethod
    def reset_sys_stdout(cls):
        ## 恢复原始的 sys.stdout
        while isinstance(sys.stdout, cls):
            sys.stdout = sys.stdout._sys_stdout
        return sys.stdout
    

def mock_os_environ_setdefault():
    ## import os
    ## TODO
    pass

