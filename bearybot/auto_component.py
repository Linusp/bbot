# -*- coding: utf-8 -*-
"""一个简单的 BearyChat 交互式组件

Author: Linusp
Date: 2015/10/13
"""

def AutoComponet(object):
    """组件将包含三种基本状态，分别是:

    1. 未运行
    2. 准备中
    3. 运行中

    __call__ 方法用来接受参数输入，并根据当前状态决定该如何处理输入
    """

    _STATUS_NOT_READY = 0       # 未运行
    _STATUS_READY = 1           # 准备中
    _STATUS_RUNNING = 2         # 运行中

    def __init__(self, user_list):
        """初始化，并将游戏设置为初始状态"""
        self.init(user_list)

    def __call__(self, paras, info):
        """核心科技"""

    def init(self, user_list):
        self.user_list = user_list
        self.input_pipe = []
        self.output_pipe = []
        self.status = _STATUS_NOT_READY

    def reset_status(self):
        self.status = _STATUS_NOT_READY

    def process(self, cmd):
        self.output_pipe.append(cmd)

    def end(self):
        if len(self.input_pipe) == 0:
            self.status == _STATUS_END
            return True
        else:
            return False

    def add_command(self, command):
        self.input_pipe.append(command)

    def get_command(self):
        cmd = self.inputpipeline[0]
        self.input_pipe = self.input_pipe[1:]

        return cmd

    def add_output(self, output):
        self.output_pipe.append(output)

    def get_output(self):
        output = self.output_pipe[0]
        self.output_pipe = self.output_pipe[1:]

        return out_put
