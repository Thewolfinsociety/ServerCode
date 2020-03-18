# -*- coding: utf-8 -*-
'''
标题： 根据类别列表提取网络报价的配置数据
作者： 娄小军
时间： 2019-11-04
更新： python3版本
更新时间： 2019-12-16
vesion 2.0.2
'''
import os
import sqlite3
import json
import sys
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
# import NetPriceSlidingData  # 调取趟门配置数据
# import NetPriceSwingData     # 掩门
import NetworkQuoteConfigData
from tornado.options import define, options
import importlib
define("port", default=5101, help="run on the given port", type=int)        # 设置端口号

importlib.reload(sys)


# 根据类别列表获取网络报价配置
class GetNetworkQuoteConfigHandl(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,access_token")
        # 这里要填写上请求带过来的Access-Control-Allow-Headers参数，如access_token就是我请求带过来的参数
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE")  # 请求允许的方法
        self.set_header("Access-Control-Max-Age", "3600")  # 用来指定本次预检请求的有效期，单位为秒，，在此期间不用发出另一条预检请求。

    def get(self, *args, **kwargs):
        print("---网络报价配置数据---")
        name = self.get_argument('name')
        slidingDoor = self.get_argument("slidingDoor")
        swingDoor = self.get_argument("swingDoor")
        rootPath = self.get_argument("rootPath")
        try:
            name = json.loads(name)
            slidingDoor = json.loads(slidingDoor)
            swingDoor = json.loads(swingDoor)
        except :
            pass
        data = NetworkQuoteConfigData.GetNetworkQuoteConfigHandl(name, slidingDoor, swingDoor, rootPath)
        result = json.dumps(data, ensure_ascii=False)
        self.write(result)
        self.finish()

    def post(self, *args, **kwargs):
        self.get()

application = tornado.web.Application([
    (r'/GetNetworkQuoteConfig', GetNetworkQuoteConfigHandl),
])


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()