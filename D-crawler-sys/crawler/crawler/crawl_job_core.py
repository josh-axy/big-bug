__all__ = (
    "CrawlJobCore",
)

import re
import json

class CrawlJobCore:
    '''
        爬虫任务内容核心
        支持json序列化和反序列化，可以用于数据传输
        提供了任务的name，还有获取页面内容的规则（css_selector[CSS] 和 reg[正则表达式]）

        构造方式如下：
            crawler.CrawlJobCore("hahaha",[("#content",True),("h1",False)],r"<span class=\"year\">(.+?)</span>")

        selectors 格式如下:
            [("#content",True),("h1",False)]
            每一项的第一项为 css-selector 字符串
            每一项的第二项是 bool 类型数据，表示是否选取多个元素,如果为 True 选取多个（select_elements_by_css_selector）

        reg:
            正则表达式
            作用于 selectors 最后结果的每一项
            如果 selectors 没有提供，则作用与原始页面内容
    '''
    def __init__(self, name: str, selectors: list = None, reg: str = None):
        self.name = name 
        
        if selectors is not None:
            self.selectors = selectors
        else:
            self.selectors = []

        if reg is not None:
            self.reg = re.compile(reg)
        else:
            self.reg = None

    def __str__(self):
        return "{}({})".format(self.__class__.__name__,self.dumps())

    def dumps(self):
        x = {
            "name":self.name,
            "selectors":self.selectors,
            "reg":self.reg.pattern if self.reg else None,
        }
        _json_str = json.dumps(x,ensure_ascii=False)
        return _json_str

    @classmethod
    def loads(cls,_json_str):
        _json = json.loads(_json_str)
        name = _json["name"]
        selectors = _json["selectors"]
        reg = _json["reg"]
        assert isinstance(name,str)
        selectors = selectors if selectors else []
        reg = reg if reg else None
        return cls(name,selectors,reg)
