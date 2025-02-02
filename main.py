import re
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import LLMResponse
from openai.types.chat.chat_completion import ChatCompletion

@register("r1-filter", "Soulter", "可选择是否过滤推理模型的思考内容", "1.0.0")
class R1Filter(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        self.display_reasoning_text = self.config.get('display_reasoning_text', True)
    
    @filter.on_llm_response()
    async def resp(self, event: AstrMessageEvent, response: LLMResponse):
        if self.display_reasoning_text:
            if response and response.raw_completion and isinstance(response.raw_completion, ChatCompletion):
                if len(response.raw_completion.choices) \
                    and response.raw_completion.choices[0].message \
                    and hasattr(response.raw_completion.choices[0].message, 'reasoning_content'):
                    message = response.raw_completion.choices[0].message
                    response.completion_text = f"🤔思考：{message.reasoning_content}\n\n{message.content}"
                    
        else: 
            # DeepSeek 官方的模型的思考存在了 reason_content 字段因此不需要过滤
            completion_text = response.completion_text
            # 适配 ollama deepseek-r1 模型
            if r'<think>' in completion_text or r'</think>' in completion_text:
                completion_text = re.sub(r'<think>.*?</think>', '', completion_text, flags=re.DOTALL).strip()
                # 可能有单标签情况
                completion_text = completion_text.replace(r'<think>', '').replace(r'</think>', '').strip()
            response.completion_text = completion_text
