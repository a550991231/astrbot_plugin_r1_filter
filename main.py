import re
from jinja2 import Environment, BaseLoader
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import LLMResponse

@register("r1-filter", "Soulter", "过滤内容", "1.0.0", 'https://github.com/a550991231/astrbot_plugin_r1_filter')
class R1Filter(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        self.display_reasoning_text = self.config.get('display_reasoning_text', True)
        self.custom_regex = self.config.get('custom_regex', r'<details[^>]*>[\s\S]*?</details>')
        
        # 初始化 Jinja2 环境并添加自定义过滤器
        self.env = Environment(loader=BaseLoader())
        self.env.filters['remove_details'] = self._remove_details_filter

    def _remove_details_filter(self, msg: str) -> str:
        """
        Jinja2 自定义过滤器，用于递归移除 details 标签或自定义正则表达式匹配的内容。
        :param msg: 原始文本
        :return: 移除指定内容后的文本
        """
        try:
            # 使用自定义正则表达式移除指定内容
            cleaned_msg = re.sub(self.custom_regex, '', msg)
            # 移除多余的空白行
            cleaned_msg = re.sub(r'\n\s*\n', '\n', cleaned_msg.strip())
            return cleaned_msg
        except re.error as e:
            self.ap.logger.error(f"正则表达式处理失败: {e}")
            return msg  # 如果正则处理失败，返回原始文本

    @filter.on_llm_response()
    async def resp(self, event: AstrMessageEvent, response: LLMResponse):
        """
        处理 LLM 响应，移除其中的 details 标签或自定义正则表达式匹配的内容。
        :param event: 消息事件
        :param response: LLM 响应
        """
        if not self.display_reasoning_text:
            response.completion_text = self._remove_details_filter(response.completion_text)
