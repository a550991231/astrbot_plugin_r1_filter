import re
from jinja2 import Environment, BaseLoader
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import LLMResponse
from astrbot.core import logger, sp
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

@register("r1-filter", "Soulter", "可选择是否过滤推理模型的思考内容", "1.0.0", 'https://github.com/Soulter/astrbot_plugin_r1_filter')
class R1Filter(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        self.display_reasoning_text = self.config.get('display_reasoning_text', True)
        
        # 初始化 Jinja2 环境并添加自定义过滤器
        self.env = Environment(loader=BaseLoader())
        self.env.filters['remove_details'] = self._remove_details_filter

    def _remove_details_filter(self, msg: str) -> str:
        try:
            # 使用 BeautifulSoup 移除 <details> 标签
            soup = BeautifulSoup(msg, 'html.parser')
            for details_tag in soup.find_all('details'):
                details_tag.decompose()  # 移除标签及其内容
            cleaned_msg = str(soup)
            # 移除多余的空白行
            cleaned_msg = re.sub(r'\n\s*\n', '\n', cleaned_msg.strip())
            return cleaned_msg
        except Exception as e:
            logger.error(f"HTML 处理失败: {e}")
            return msg  # 如果处理失败，返回原始文本

    @filter.on_llm_response()
    async def on_llm_resp(self, event: AstrMessageEvent, response: LLMResponse):
        if isinstance(response.completion_text, list):
            msg = "".join(response.completion_text)
        else:
            msg = response.completion_text
        if not self.display_reasoning_text and "<details" in msg:
            response.completion_text = self._remove_details_filter(msg)

