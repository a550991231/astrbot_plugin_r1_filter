from astrbot.api.provider import LLMResponse

@filter.on_llm_response()
async def on_llm_resp(self, event: AstrMessageEvent, response: LLMResponse):
    # 定义要删除的 <details> 标签内容
    details_start = '<details style="color:gray;background-color: #f8f8f8;padding: 8px;border-radius: 4px;" open> <summary> Thinking... </summary>'
    details_end = '</details>'

    # 删除 <details> 标签及其内容
    if details_start in response.completion_text and details_end in response.completion_text:
        start_index = response.completion_text.find(details_start)
        end_index = response.completion_text.find(details_end) + len(details_end)
        response.completion_text = response.completion_text[:start_index] + response.completion_text[end_index:].strip()

    return resp
