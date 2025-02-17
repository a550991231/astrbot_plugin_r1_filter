import re
from jinja2 import Environment, BaseLoader
from bs4 import BeautifulSoup
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import LLMResponse

@register("r1-filter", "Soulter", "过滤内容", "1.0.0", 'https://github.com/a550991231/astrbot_plugin_r1_filter')
class R1Filter(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        self.display_reasoning_text = self.config.get('display_reasoning_text', True)
        
        # 从配置文件中获取自定义正则表达式，如果没有则使用默认值
        self.pattern = self.config.get('custom_regex', r'<details[^>]*>[\s\S]*?</details>')
        
        # 初始化 Jinja2 环境并添加自定义过滤器
        self.env = Environment(loader=BaseLoader())
        self.env.filters['remove_think'] = self._remove_think_filter

    #def _remove_think_filter(self, msg: str) -> str:
        #try:
            # 使用配置文件中的正则表达式移除所有匹配的标签（包括嵌套标签）
           # cleaned_msg = re.sub(self.pattern, '', msg)
            # 移除多余的空白行
           # cleaned_msg = re.sub(r'\n\s*\n', '\n', cleaned_msg.strip())
           # return cleaned_msg
       # except re.error as e:
          #  self.ap.logger.error(f"正则表达式处理失败: {e}")
           # return msg  # 如果正则处理失败，返回原始文本
    def _remove_details_filter(self, msg: str) -> str:
        soup = BeautifulSoup(msg, 'html.parser')
        for details in soup.find_all('details'):
        details.decompose()  # 移除 details 标签及其内容
    return str(soup)

    @filter.on_llm_response()
    async def resp(self, event: AstrMessageEvent, response: LLMResponse):
        if re.search(self.pattern, response.completion_text):
           response.completion_text = self._remove_think_filter(response.completion_text)
