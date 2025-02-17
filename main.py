import re
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import LLMResponse
from openai.types.chat.chat_completion import ChatCompletion

@register("r1-filter", "Soulter", "可选择是否过滤推理模型的思考内容", "1.0.0", 'https://github.com/Soulter/astrbot_plugin_r1_filter')
@filter.on_llm_response()
async def resp(self, event: AstrMessageEvent, response: LLMResponse):
    details_start = '<details style="color:gray;background-color: #f8f8f8;padding: 8px;border-radius: 4px;" open> <summary> Thinking... </summary>'
    details_end = '</details>'
    if details_start in response.completion_text and details_end in response.completion_text:
        start_index = response.completion_text.find(details_start)
        end_index = response.completion_text.find(details_end) + len(details_end)
        response.completion_text = response.completion_text[:start_index] + response.completion_text[end_index:].strip()
