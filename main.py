import re
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

    def _remove_details(self, msg: str) -> str:
        try:
            # 使用 BeautifulSoup 移除 <details> 标签
            soup = BeautifulSoup(msg, 'html.parser')
            for details_tag in soup.find_all('details'):
                details_tag.decompose()  # 移除标签及其内容
            
            # 将清理后的 HTML 转换为纯文本
            cleaned_msg = soup.get_text(separator=' ', strip=True)

            # 移除多余的空白行
            cleaned_msg = re.sub(r'\n\s*\n+', '\n', cleaned_msg).strip()
            
            return cleaned_msg
        except Exception as e:
            logger.error(f"HTML 处理失败: {e}")
            return msg  # 如果处理失败，返回原始文本

    def _remove_details_with_regex(self, msg: str) -> str:
        try:
            # 使用正则表达式移除 <details> 标签及其内容
            cleaned_msg = re.sub(r'<details[^>]*>[\s\S]*?</details>', '', msg, flags=re.DOTALL)
            # 移除多余的空白行
            cleaned_msg = re.sub(r'\n\s*\n+', '\n', cleaned_msg).strip()
            return cleaned_msg
        except Exception as e:
            logger.error(f"正则表达式处理失败: {e}")
            return msg  # 如果处理失败，返回原始文本

    @filter.on_llm_response()
    async def on_llm_resp(self, event: AstrMessageEvent, resp: LLMResponse):
        original_completion_text = resp.completion_text
        
        # 首先尝试使用 BeautifulSoup
        cleaned_completion_text = self._remove_details(original_completion_text)
        
        # 如果 BeautifulSoup 没有移除 <details> 标签，则使用正则表达式作为备用方案
        if '<details' in cleaned_completion_text:
            logger.warning("BeautifulSoup 未能完全移除 <details> 标签，使用正则表达式进行二次处理。")
            cleaned_completion_text = self._remove_details_with_regex(original_completion_text)
        
        resp.completion_text = cleaned_completion_text
        return resp
