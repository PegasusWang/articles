#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""测试motorengine, 话说这玩意github上star太少了，用的有点忐忑
基于py.test, https://pytest.org/latest/unittest.html
这里使用py.test偷懒下，不用assertEqual等方法，pytest里都可以使用assert，
而且可以单独测试函数，不用都搞一个类，pytest可以直接运行unittest类
参考：http://xidui.github.io/2015/12/09/%E8%B0%88%E8%B0%88%E9%A1%B9%E7%9B%AE%E9%87%8D%E6%9E%84%E4%B8%8E%E6%B5%8B%E8%AF%95/#comments
使用py.test -q test_xxx.py运行一个模块的测试
"""

import _env
import pytest
import copy
from models.post import Post
from models.user import User
from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.testing import gen_test, AsyncTestCase
from motorengine.connection import connect
from config.config import CONFIG

save_user = {
    'name': '老王',
    'slug': 'lao-wang',
    'email': 'test@qq.com',
}

save_post = {
    #'author': User(**save_user),
    'title': 'python如何用协程模拟线程',
    'slug': 'test',
    'markdown': '''
###协程模拟线程的例子
先看一个简单的例子，来自《Python Cookbook》，这本书会在[书籍](http://pyhome.org/tag/book/)里分享。


    #!/usr/bin/env python3

    def countdown(n):
        while n > 0:
            print('T-minus', n)
            yield
            n -= 1
        print("Blastoff!")


    def countup(n):
        x = 0
        while x < n:
            print('Counting up', x)
            yield
            x += 1

    from collections import deque

    class TaskScheduler:
        def __init__(self):
            self._task_queue = deque()

        def new_task(self, task):
            """Admit a newly started task to the scheduler"""
            self._task_queue.append(task)

        def run(self):
            """run until there are no more tasks"""
            while self._task_queue:
                task = self._task_queue.popleft()
                try:
                    # Run until the next yield statement
                    next(task)
                    self._task_queue.append(task)
                except StopIteration:
                    # Generator is no longer executing
                    pass


    def main():
        sched = TaskScheduler()
        sched.new_task(countdown(10))
        sched.new_task(countdown(5))
        sched.new_task(countup(15))
        sched.run()


    if __name__ == '__main__':
        main()


这里只有两个协程和一个调度类，执行这段代码以后，有如下输出：

```
('T-minus', 10)
('T-minus', 5)
('Counting up', 0)
('T-minus', 9)
('T-minus', 4)
('Counting up', 1)
('T-minus', 8)
('T-minus', 3)
('Counting up', 2)
('T-minus', 7)
('T-minus', 2)
('Counting up', 3)
('T-minus', 6)
('T-minus', 1)
('Counting up', 4)
('T-minus', 5)
Blastoff!
('Counting up', 5)
('T-minus', 4)
('Counting up', 6)
('T-minus', 3)
('Counting up', 7)
('T-minus', 2)
('Counting up', 8)
('T-minus', 1)
('Counting up', 9)
Blastoff!
('Counting up', 10)
('Counting up', 11)
('Counting up', 12)
('Counting up', 13)
('Counting up', 14)

```
看起来是不是很像开了三个线程在并发执行的结果，但实际上却是一个线程。这里没有使用系统线程，而是用协程来模拟线程，又叫做用户级线程或者绿色线程。解释器遇到yield会挂起执行，在任务调度器类里TaskScheduler用队列进行任务切换，就模拟出了线程的效果。可见，用协程模拟线程主要在于如何调度和驱动这些coroutine的执行。

###怎么用tornado写一个高性能异步爬虫
之前写的那个小爬虫用来处理10万级以下的页面完全没有太大压力，现在就来一步一步试试怎么写出来。
先来看怎么用tornado写抓一个网页的例子:

```
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from tornado import gen
import tornado.httpclient
import tornado.ioloop

@gen.coroutine
def main():
    http_client = tornado.httpclient.AsyncHTTPClient()
    response = yield http_client.fetch('http://httpbin.org/get')
    print(response.body)

tornado.ioloop.IOLoop.current().run_sync(main)
```
当然你也可以试试python3.5的async/await语法。写成下边这样子:

```
#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-

from tornado import gen
import tornado.httpclient
import tornado.ioloop


async def main():
    http_client = tornado.httpclient.AsyncHTTPClient()
    response = await http_client.fetch('http://httpbin.org/get')
    print(response.body)

tornado.ioloop.IOLoop.current().run_sync(main)
```
这里的run_sync方法启动IOLoop，运行传入的函数，然后结束loop。
照着这个思路，如果有很多网页需要抓，我们需要抓取、解析等函数，同样使用异步的httpclient，
首先是用异步AsyncHTTPClient发请求得到一个response对象。
```
from tornado.httpclient import AsyncHTTPClient
from tornado import ioloop, gen, queues
@gen.coroutine
def fetch(url):
    print('fetcing', url)
    response = yield AsyncHTTPClient().fetch(url, raise_error=False)
    raise gen.Return(response)
```
这里使用了装饰器gen.coroutine，我们知道协程对象需要先send(None)或者用next()方法『启动』一下，下边就是个简单的coroutine实现（只是为了说明coroutine工作原理，和爬虫示例无关）

```
def coroutine(func):
    def start(*args, **kwargs):
        rc = func(*args, **kwargs)
        rc.next()
        return rc
    return start
```
现在有了一个异步httpclient发请求了，还要干啥呢，当然是拿到请求的结果然后处理了。

```
from bs4 import BeautifulSoup
_q = queues.Queue()    # tornado.queues

@gen.coroutine
def run():
    try:
        url = yield _q.get()
        res = yield fetch(url)
        html = res.body
        soup = BeautifulSoup(html)
        print(str(soup.find('title')))
    finally:
        _q.task_done()

```
这里依旧很简单，这个run方法从队列里拿到url并发送请求（注意这个队列是tornado提供的支持协程的队列），得到页面的html，这里用bs4库抠出来title标签。接下来是一个worker，

```
@gen.coroutine
def worker():
    while True:
        yield run()
```
为什么需要一个worker呢，我们需要抓取的过程一直能够进行，直到队列为空为止，这里的worker就是个死循环，一直yield任务。最后写一个main函数执行:

```
@gen.coroutine
def main():
    for i in range(73000, 73100):
        url = "http://www.jb51.net/article/%d.htm" % i
        _q.put(url)
    for _ in range(10):    # 跑十个，十个worker一直从队列取任务执行
        worker()
    yield _q.join(timeout=timedelta(seconds=30))


if __name__ == '__main__':
    ioloop.IOLoop.current().run_sync(main)
```

下边是完整代码:


    #!/usr/bin/env python
    # -*- coding:utf-8 -*-


    from datetime import timedelta
    from bs4 import BeautifulSoup
    from tornado.httpclient import AsyncHTTPClient
    from tornado import ioloop, gen, queues


    @gen.coroutine
    def fetch(url):
        print('fetcing', url)
        response = yield AsyncHTTPClient().fetch(url, raise_error=False)
        raise gen.Return(response)

    _q = queues.Queue()


    @gen.coroutine
    def run():
        try:
            url = yield _q.get()
            res = yield fetch(url)
            html = res.body
            soup = BeautifulSoup(html)
            print(str(soup.find('title')))
        finally:
            _q.task_done()


    @gen.coroutine
    def worker():
        while True:
            yield run()


    @gen.coroutine
    def main():
        for i in range(73000, 73100):    # 放100个链接进去
            url = "http://www.jb51.net/article/%d.htm" % i
            yield _q.put(url)
        for _ in range(100):    # 模拟100个线程
            worker()
        yield _q.join(timeout=timedelta(seconds=30))


    if __name__ == '__main__':
        ioloop.IOLoop.current().run_sync(main)

不到50行的代码一个速度还不错的小爬虫就出来了。你也可以把『并发数量』10改成100，可以看见几乎一瞬间100个网页就解析出来了，真他喵的强悍。

####练习
给读者一个练习，尝试把这个简单的示例改成一个可以重用的类，把发请求，处理页面等拆出来以便子类可以重写这些常见的爬虫操作。还可以使用motor等异步库把得到的结果存储到mongodb数据库里。''' ,
}


class TestModelPost(AsyncTestCase):
    """Post测试
    注意改变数据结构后先删除mongo数据库，否则会有超时
    """

    def setUp(self):
        self.io_loop = IOLoop.current()
        connect(CONFIG.MONGO.DATABASE, host=CONFIG.MONGO.HOST,
                port=CONFIG.MONGO.PORT,
                io_loop=self.io_loop)    # connect mongoengine

    @gen_test
    def test_create(self):
        """非幂等，对应http中的post"""
        user = yield User.objects.create(**save_user)
        save_post['author'] = user
        post = yield Post.objects.create(**save_post)
        assert post is not None
        assert post.slug == 'test'

        post_nums = yield Post.objects.filter(slug='test').delete()
        user_nums = yield User.objects.filter(slug=save_user['slug']).delete()
        assert post_nums == 1
        assert user_nums == 1

    @gen_test
    def test_save(self):
        """幂等，对应http中的put"""
        post = yield Post.objects.create(**save_post)
        assert post.slug == 'test'
        post.slug = 'save'
        post = yield post.save()
        assert post.slug == 'save'
        nums = yield Post.objects.filter(slug='save').delete()
        assert nums == 1

    @gen_test
    def test_bulk_insert(self):
        post_list = []
        n = 10
        for i in range(n):
            post = copy.deepcopy(save_post)    # note use deepcopy
            post['slug'] = post['slug'] + str(i)
            post_obj = Post(**post)
            post_list.append(post_obj)
        yield Post.objects.bulk_insert(post_list)
        post_obj_list = yield Post.objects.find_all()
        assert n == len(post_obj_list)
        nums = yield Post.objects.delete()
        assert nums == n


@coroutine
def create_posts():
    user = yield User.objects.create(**save_user)
    post_list = []
    n = 35
    for i in range(n):
        post = copy.deepcopy(save_post)    # note use deepcopy
        post['slug'] = post['slug'] + str(i)
        post['author'] = user
        post_obj = Post(**post)
        post_list.append(post_obj)
    yield Post.objects.bulk_insert(post_list)


if __name__ == '__main__':
    connect(CONFIG.MONGO.DATABASE, host=CONFIG.MONGO.HOST,
            port=CONFIG.MONGO.PORT,
            io_loop=IOLoop.current())    # connect mongoengine
    IOLoop.current().run_sync(create_posts)
