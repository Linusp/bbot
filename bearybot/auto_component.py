# -*- coding: utf-8 -*-
"""一个简单的 BearyChat 交互式组件

Author: Linusp
Date: 2015/10/13
"""

from Queue import Queue


class AutoComponet(object):
    """组件将包含三种基本状态，分别是:

    1. 未运行
    2. 准备中
    3. 运行中

    __call__ 方法用来接受参数输入，并根据当前状态决定该如何处理输入
    """

    _STATUS_NOT_READY = 0       # 未运行
    _STATUS_READY = 1           # 准备中
    _STATUS_RUNNING = 2         # 运行中

    def __init__(self, *args, **kwargs):
        """初始化，并将游戏设置为初始状态"""
        self.status = None
        self.init(*args, **kwargs)

    def __call__(self, paras, info):
        """核心科技"""
        return self.process(paras, info)

    def init(self, *args, **kwargs):
        """初始化核心功能相关的内部数据"""
        self.status = self._STATUS_NOT_READY

    def reset_status(self):
        """重置组件状态"""
        self.status = self._STATUS_NOT_READY

    def process(self, paras, info):
        return paras
