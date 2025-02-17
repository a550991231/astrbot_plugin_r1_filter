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
     # 定义要删除的 <details> 标签内容
    details_start = '<details style="color:gray;background-color: #f8f8f8;padding: 8px;border-radius: 4px;" open> <summary> Thinking... </summary>'
    details_end = '</details>'

    # 删除 <details> 标签及其内容
    if details_start in response.completion_text and details_end in response.completion_text:
        start_index = response.completion_text.find(details_start)
        end_index = response.completion_text.find(details_end) + len(details_end)
        response.completion_text = response.completion_text[:start_index] + response.completion_text[end_index:].strip()
