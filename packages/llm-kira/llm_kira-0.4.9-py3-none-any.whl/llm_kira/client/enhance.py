# -*- coding: utf-8 -*-
# @Time    : 1/23/23 8:11 PM
# @FileName: enhance.py
# @Software: PyCharm
# @Github    ：sudoskys
from loguru import logger


class Support(object):
    async def run(self
                  ) -> str:
        return ""


class PluginSystem(Support):
    def __init__(self, plugin_table: dict, prompt: str):
        self.table = plugin_table
        self.prompt = prompt

    async def run(self) -> str:
        _append = "-"
        _return = []
        if not all([self.table, self.prompt]):
            return _append
        from .module.platform import ChatPlugin, PluginParam
        processor = ChatPlugin()
        for plugin in self.table.keys():
            processed = await processor.process(param=PluginParam(text=self.prompt, server=self.table),
                                                plugins=[plugin])
            _return.extend(processed)
        reply = "\n".join(_return) if _return else ""
        logger.debug(f"AllPluginReturn:{reply}")
        return reply
