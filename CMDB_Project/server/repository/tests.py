#基于yield并发执行
import time
def consumer():
    '''任务1:接收数据,处理数据'''
    while True:
        x=yield # 相当于return，第一次返回数据给next(g)，第二次以后都返回给g.send()

def producer():
    '''任务2:生产数据'''
    g=consumer()    # 实例化函数，得到生成器
    next(g)   #  调用 consumer函数
    for i in range(10000000):
        g.send(i)   # 往生成器中发送数据

start=time.time()
#基于yield保存状态,实现两个任务直接来回切换,即并发的效果
#PS:如果每个任务中都加上打印,那么明显地看到两个任务的打印是你一次我一次,即并发执行的.
producer()

stop=time.time()
print(stop-start) #2.0272178649902344