__all__ = ["critical",
           "debug",
           "error",
           "info",
           "log",
           "warning"]

from logging import\
    basicConfig,\
    critical,\
    CRITICAL,\
    debug,\
    DEBUG,\
    error,\
    ERROR,\
    info,\
    INFO,\
    log,\
    warning,\
    WARNING

LEVEL = DEBUG
__INITIALIZED__ = False

if __INITIALIZED__ is False:
    __INITIALIZED__ = True
    basicConfig(level=LEVEL,
                format="%(asctime)s | %(levelname)-8s | %(module)-25s | %(funcName)-25s | %(lineno)-5s: %(message)s",
                datefmt="%Y-%m-%d %H:%M")
