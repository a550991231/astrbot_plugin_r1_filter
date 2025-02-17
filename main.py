import re
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import LLMResponse
from openai.types.chat.chat_completion import ChatCompletion

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
                        and response.raw_completion.choices[0].message:
                    message = response.raw_completion.choices[0].message
                    reasoning_content = ""  # 初始化 reasoning_content

                    # 检查 Groq deepseek-r1-distill-llama-70b模型的 'reasoning' 属性
                    if hasattr(message, 'reasoning') and message.reasoning:
                        reasoning_content = message.reasoning
                    # 检查 DeepSeek deepseek-reasoner模型的 'reasoning_content'
                    elif hasattr(message, 'reasoning_content') and message.reasoning_content:
                        reasoning_content = message.reasoning_content

                    if reasoning_content:
                        response.completion_text = f"🤔思考：{reasoning_content}\n\n{message.content}"
                    else:
                        response.completion_text = message.content
                    
        else: 
            # DeepSeek 官方的模型的思考存在了 reason_content 字段因此不需要过滤
            completion_text = response.completion_text
            details_start = '<details style="color:gray;background-color: #f8f8f8;padding: 8px;border-radius: 4px;" open> <summary> Thinking... </summary>'
            details_end = '</details>'

    # 删除 <details> 标签及其内容
            if details_start in response.completion_text and details_end in response.completion_text:
                start_index = response.completion_text.find(details_start)
                end_index = resp.completion_text.find(details_end) + len(details_end)
                response.completion_text = response.completion_text[:start_index] + response.completion_text[end_index:].strip()
