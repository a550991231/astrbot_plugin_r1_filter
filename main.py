import re
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import LLMResponse
from openai.types.chat.chat_completion import ChatCompletion

@filter.on_llm_response()
async def on_llm_resp(self, event: AstrMessageEvent, resp: LLMResponse):
    # 使用正则表达式删除 <details> 标签及其内容
    resp.completion_text = re.sub(
        r'<details[^>]*>.*?</details>',  # 匹配 <details> 标签及其内容
        '',  # 替换为空字符串
        resp.completion_text,  # 要处理的文本
        flags=re.DOTALL  # 允许 . 匹配换行符
    ).strip()  # 去除多余的空格

    return resp
