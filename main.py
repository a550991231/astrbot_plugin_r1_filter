import re
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import LLMResponse


@register("r1-filter", "Soulter", "可选择是否过滤推理模型的思考内容", "1.0.0", 'https://github.com/Soulter/astrbot_plugin_r1_filter')

    
@filter.on_llm_response()
async def resp(self, event: AstrMessageEvent, response: LLMResponse):
    response.completion_text = " 测试1231"
