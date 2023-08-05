# -*- coding:utf-8 -*-
# 文件:  thread_pool.py
# 日期:  2022/8/19 9:50
"""

"""
import datetime
import threading
from concurrent import futures
from .logs import logger


__version__ = '1.4'
__all__ = ['JdThreadPool']


"""
Future 提供了如下方法：
cancel()：取消该 Future 代表的线程任务。如果该任务正在执行，不可取消，则该方法返回 False；否则，程序会取消该任务，并返回 True。
cancelled()：返回 Future 代表的线程任务是否被成功取消。
running()：如果该 Future 代表的线程任务正在执行、不可被取消，该方法返回 True。
done()：如果该 Future 代表的线程任务被成功取消或执行完成，则该方法返回 True。
result(timeout=None)：获取该 Future 代表的线程任务最后返回的结果。如果 Future 代表的线程任务还未完成，该方法将会阻塞当前线程，其中 timeout 参数指定最多阻塞多少秒。
exception(timeout=None)：获取该 Future 代表的线程任务所引发的异常。如果该任务成功完成，没有异常，则该方法返回 None。
add_done_callback(fn)：为该 Future 代表的线程任务注册一个“回调函数”，当该任务成功完成时，程序会自动触发该 fn 函数。
"""

# 0-未启动， 1-running, 2-canceled, 3-done
TASK_NOT_START = 0
TASK_RUNNING = 1
TASK_CANCELED = 2
TASK_DONE = 3


class JdTaskStatus(object):
    # 任务状态
    def __init__(self, name, future):
        self.name = name    # 任务名称
        self.start_time = datetime.datetime.today()  # 任务启动时间
        self.finish_time = None  # 任务完成时间
        self.status = 0     # 0-未启动， 1-running, 2-canceled, 3-done
        self.future = future    # 任务


class JdThreadPool(object):
    """
    线程池
    """

    def __init__(self, max_workers=5):
        """
        创建线程池
        """
        self.pool = futures.ThreadPoolExecutor(max_workers=max_workers)
        self._thread_lock = threading.Lock()
        self._future = {}  # future -> name
        self._task = {}   # name -> JdTaskStatus

    def add_job(self, callback, para=None, name=None) -> futures.Future:
        """
        添加任务
        callback:   任务入口函数
        para:       上述入口函数的参数， None时不传递
        name:       任务名称， 用于防止任务重复执行
        """
        thread_name = threading.current_thread().name
        logger.debug(f"[ {thread_name} ], {para}")
        
        if name and name in self._task:  # 任务已经添加过，且是运行状态时， 不再添加重复任务
            t = self._task[name]
            if isinstance(t, JdTaskStatus) and isinstance(t.future, futures.Future):
                if t.future.running():
                    return t.future
        
        if para is not None:
            future = self.pool.submit(callback, para)
        else:
            future = self.pool.submit(callback)
        self._thread_lock.acquire()
        self._future[future] = name or ''
        if name:
            self._task[name] = JdTaskStatus(name, future)
        self._thread_lock.release()
        future.add_done_callback(self._callback_finished)
        return future

    def _callback_finished(self, future: futures.Future):
        """
        线程执行完毕后的 回调函数
        """
        thread_name = threading.current_thread().name
        logger.debug(f"[ {thread_name} ]执行完成： {future.result()}")
        
        self._thread_lock.acquire()
        name = self._future.pop(future, None)
        if name in self._task:
            t = self._task[name]
            t.status = TASK_DONE    # 任务已经完成
        self._thread_lock.release()

    @classmethod
    def cancel(cls, future: futures.Future):
        """
        取消该 Future 代表的线程任务。如果该任务正在执行，不可取消，则该方法返回 False；
        否则，程序会取消该任务，并返回 True。
        """
        return future.cancel()

    @classmethod
    def cancelled(cls, future: futures.Future):
        """
        返回 Future 代表的线程任务是否被成功取消。
        """
        return future.cancelled()

    @classmethod
    def running(cls, future: futures.Future):
        """
        如果该 Future 代表的线程任务正在执行、不可被取消，该方法返回 True。
        """
        return future.running()

    @classmethod
    def done(cls, future: futures.Future):
        """
        如果该 Future 代表的线程任务被成功取消或执行完成，则该方法返回 True。
        """
        return future.done()
    
    def is_running(self, name):
        # 任务 name 是否处于运行状态  True-运行中 False-非运行中，已经结束 或 取消状态
        
        t = self._task.get(name)
        if t and isinstance(t, JdTaskStatus) and isinstance(t.future, futures.Future):
            return t.future.running()
        return False
