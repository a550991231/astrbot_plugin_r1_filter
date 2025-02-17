导入​
来自Jinja2进口环境，基本装载机
来自actrbot.api.event进口过滤器，aStrmessageEvent
从actrbot.api.star进口上下文，星星，注册
来自actrbot.api.provider导入llmresponse

@register("r1-filter", "Soulter", "可选择是否过滤推理模型的思考内容", "1.0.0", 'https://github.com/Soulter/astrbot_plugin_r1_filter')
R1Filter类（星）：
    def  __init__ （自我，上下文：上下文，配置：dict ）：
        极好的（）。__init__ （上下文）
        自己。config = config
        自己。display_reasoning_text = self。config。获取（'display_reasoning_text'，true ）
        
        # 初始化 Jinja2 环境并添加自定义过滤器
        自己。env =环境（ loader = baseloader （））
        自己。env。过滤器[ 'remove_think' ] = self。_remove_think_filter

    def _remove_think_filter(self, msg: str) -> str:
”“”
        Jinja2 自定义过滤器，用于递归移除 <think> 标签。
        :param msg: 原始文本
        :return: 移除 <think> 标签后的文本
        ”“”
 r'<think [^>]*> [\ s \ s]*？</think>'
        try:
            # 一次性移除所有 <think> 标签（包括嵌套标签）

            # 移除多余的空白行

            return cleaned_msg
        except re.error as e:
            self.ap.logger.error(f"正则表达式处理失败: {e}")
            return msg  # 如果正则处理失败，返回原始文本

    @filter.on_llm_response()
    async def resp(self, event: AstrMessageEvent, response: LLMResponse):
”“”
        处理 LLM 响应，移除其中的 <think> 标签。
        :param event: 消息事件
        :param response: LLM 响应
        ”“”

            回复。plote_text = self。_remove_think_filter （响应。完成_text ）
