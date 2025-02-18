import re
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import LLMResponse
from openai.types.chat.chat_completion import ChatCompletion

@register("r1-filter", "Soulter", "可选择是否过滤推理模型的思考内容", "1.0.0", 'https://github.com/Soulter/astrbot_plugin_r1_filter')
class R1Filter(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        self.display_reasoning_text = self.config.get('display_reasoning_text', True)
    
    @filter.on_llm_response()
    async def resp(self, event: AstrMessageEvent, response: LLMResponse):
        if self.display_reasoning_text:
            response.completion_text = " 测试1231"
