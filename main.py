import re
from jinja2 import Environment, BaseLoader
from bs4 import BeautifulSoup  # 引入 BeautifulSoup
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import LLMResponse

@register("r1-filter", "Soulter", "过滤内容", "1.0.0", 'https://github.com/a550991231/astrbot_plugin_r1_filter')
class R1Filter(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        self.display_reasoning_text = self.config.get('display_reasoning_text', True)
        
        # 初始化 Jinja2 环境并添加自定义过滤器
        self.env = Environment(loader=BaseLoader())
        self.env.filters['remove_details'] = self._remove_details_filter

    def _remove_details_filter(self, msg: str) -> str:
        """
        使用 BeautifulSoup 移除 details 标签及其内容。
        :param msg: 原始文本
        :return: 移除 details 标签后的文本
        """
        try:
            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(msg, 'html.parser')
            
            # 查找所有的 <details> 标签并移除
            for details in soup.find_all('details'):
                details.decompose()  # 移除标签及其内容
            
            # 返回处理后的文本
            return str(soup)
        except Exception as e:
            self.ap.logger.error(f"HTML 解析失败: {e}")
            return msg  # 如果处理失败，返回原始文本

    @filter.on_llm_response()
    async def resp(self, event: AstrMessageEvent, response: LLMResponse):
        """
        处理 LLM 响应，移除其中的 details 标签。
        :param event: 消息事件
        :param response: LLM 响应
        """
        if "<details" in response.completion_text:
            response.completion_text = self._remove_details_filter(response.completion_text)
