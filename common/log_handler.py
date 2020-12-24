import logging
import os
import time
from functools import wraps


# 方法一： 函数封装 def getLogger()
def getLogger(name="root", file=None, logger_level="DEBUG", stream_level="DEBUG", file_level="DEBUG",
              format="%(asctime)s::%(levelname)s::%(message)s"):
    logger = logging.getLogger(name)
    logger.setLevel(logger_level)
    strem_handler = logging.StreamHandler()
    strem_handler.setLevel(stream_level)
    fmt = logging.Formatter(format)
    strem_handler.setFormatter(fmt)
    logger.addHandler(strem_handler)
    if file:
        file_handler = logging.FileHandler(file, encoding="utf-8", mode='a')
        file_handler.setLevel(file_level)
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)

    return logger


# lg=getLogger(name="tyx",file="tyx.logs")
# lg.info("jaj")

# 类封装 class LoggerHander(logging.Logger)
# 提示：得到收集器 logger 可以用 super()__init__ ！

class LoggerHander(logging.Logger):
    def __init__(self, name=None, file=None, logger_level="DEBUG", stream_level="DEBUG", file_level="DEBUG",
                 format="%(asctime)s::%(levelname)s::%(message)s"):
        super().__init__(name, logger_level)
        self.setLevel(logger_level)
        strem_handler = logging.StreamHandler()
        strem_handler.setLevel(stream_level)
        fmt = logging.Formatter(format)
        strem_handler.setFormatter(fmt)
        self.addHandler(strem_handler)
        if file:
            file_handler = logging.FileHandler(file)
            file_handler.setLevel(file_level)
            file_handler.setFormatter(fmt)
            self.addHandler(file_handler)


# lg=LoggerHander(name="tyx",file="test.logs")
# lg.info("hshsh")


# 日志记录，默认日志文件是test开头，默认路径是conf，可以指定模块
def logWrite(logfileName="test",
             path=os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
             , module=None):
    conf_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), path)
    date = time.strftime("%Y-%m-%d", time.localtime())
    logfileName = "./" + logfileName + "-%s" % date + ".logs"
    if module == None:
        lg = getLogger(name="tyx", file=conf_path + logfileName)
        lg.info("hha")
    else:
        module_path = os.path.join(conf_path, module)
        if module not in os.listdir(conf_path):
            os.mkdir(module_path)
            lg = getLogger(name="tyx", file=module_path + logfileName)
            lg.info("hha")
        else:
            lg = getLogger(name="tyx", file=module_path + logfileName)
            lg.info("hha")




if __name__ == '__main__':
    import logging
    from logging import FileHandler, Formatter
    import os.path as fpath
    from datetime import datetime

    logfile = fpath.join(fpath.dirname(fpath.abspath(__file__)), datetime.now().strftime('%Y%m%d') + '.log')

    formatter = '%(asctime)s %(levelname)-8s %(name)-15s %(funcName)s %(message)s'
    dateformatter = '%Y-%m-%d %H:%M:%S'
    default_level = {
        'critical': 50,
        'error': 40,
        'warning': 30,
        'info': 20,
        'debug': 10
    }


    def bindlog(level='debug'):
        def wrapper(cls):
            print(cls)
            logger = logging.getLogger(cls.__name__)
            logger.setLevel(default_level[level])
            file_handle = FileHandler(logfile)
            file_handle.setFormatter(Formatter(formatter, dateformatter))
            logger.addHandler(file_handle)

            def inner(*args, **kwargs):
                if not hasattr(cls, 'log'):
                    setattr(cls, 'log', logger)
                return (cls(*args, **kwargs))

            return inner

        return wrapper


    @bindlog()
    class Test:

        def add(self):
            for _ in range(100):
                self.log.info('sdsd.')

