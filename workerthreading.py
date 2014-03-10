#coding=utf-8
#*********************************
#  Author: hanker
#   Email: hanpeiyi1@gmail.com
#*********************************
import Queue, threading, sys
from threading import Thread


#定义Worker为线程
class Worker(Thread):
    #count = 0
    def __init__(self, workQueue, resultQueue, timeout = 1):
        Thread.__init__(self)
        self.setDaemon(True)
        self.workQueue = workQueue
        self.resultQueue = resultQueue
        self.timeout = timeout
        self.start()
        
	#timeout设置从队列中取数据的超时时间，如果超时则引发Empty异常
    def run(self):
        while True:
            try:
                callable, args, kwds = self.workQueue.get(timeout=self.timeout)
                res = callable(*args, **kwds)
                self.resultQueue.put(res)
            except Queue.Empty:
                break
            except Exception, e:
                print e
                
#定义WorkerManager为线程池管理者
class WorkerManager:
    def __init__(self, num_of_workers=10, timeout=1):
        self.workQueue= Queue.Queue()
        self.resultQueue = Queue.Queue()
        self.workers = []
        self.timeout = timeout
        self._recruitThreads(num_of_workers)
    
    #初始化Worker线程池
    def _recruitThreads(self, num_of_workers):
        for i in range(num_of_workers):
            worker = Worker(self.workQueue, self.resultQueue, self.timeout)
            self.workers.append(worker)
                
    #将打开的所有子线程都杀死
    def wait_for_complete(self):
        while len(self.workers): 
            worker = self.workers.pop()
            worker.join()
            if worker.isAlive() and not self.workQueue.empty():
                self.workers.append(worker)
        
    def add_job(self, callable, *args, **kwds):
        self.workQueue.put((callable, args, kwds))
        
    def get_result(self):
        return self.resultQueue
