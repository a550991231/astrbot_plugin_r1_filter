import re
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import LLMResponse

@register("r1-filter", "Soulter", "可选择是否过滤推理模型的思考内容", "1.0.0", 'https://github.com/a550991231/astrbot_plugin_r1_filter')
def __init__(self, context: Context, config: dict):
    super().__init__(context)
    self.config = config
    # 是否显示思考内容
    self.display_reasoning_text = self.config.get('display_reasoning_text', {}).get('value', True)
    # 加载自定义正则表达式
    self.custom_regex = self.config.get('custom_regex', {}).get('value', '')

def _remove_custom_content(self, msg: str) -> str:
    """
    根据自定义正则表达式删除内容。
    :param msg: 原始文本
    :return: 移除自定义内容后的文本
    """
    try:
        if self.custom_regex:
            msg = re.sub(self.custom_regex, '', msg)
        # 移除多余的空白行
        msg = re.sub(r'\n\s*\n', '\n', msg.strip())
        return msg
    except re.error as e:
        self.ap.logger.error(f"正则表达式处理失败: {e}")
        return msg  # 如果正则处理失败，返回原始文本
@filter.on_llm_response()
async def resp(self, event: AstrMessageEvent, response: LLMResponse):
    """
    处理 LLM 响应，根据配置决定是否移除自定义内容。
    :param event: 消息事件
    :param response: LLM 响应
    """
    if self.display_reasoning_text:
        # 如果需要显示思考内容，则不删除内容
        return
    # 如果需要删除内容，则根据自定义正则表达式处理
    if self.custom_regex:
        response.completion_text = self._remove_custom_content(response.completion_text)
