import common
from crawler_server import CrawlerServer
import asyncio

if __name__=="__main__":
    C = CrawlerServer()
    with C.run_crawler():
        # 这里利用了 run_forever 阻塞了主线程
        loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # loop.run_until_complete(self.init_app(loop))
        loop.run_forever()
    print("OVER")