__all__ = (
    "CrawlJobCore",
)

import re
import json

class CrawlJobCore:
    '''
        爬虫任务内容核心
        支持json序列化和反序列化，可以用于数据传输
        提供了任务的name，还有获取页面内容的规则（css_selector[CSS选择器] 和 reg[正则表达式]）
        设计上支持多级，
        上一层爬取的 url （注意，只能是 url） 作为下一层的输入
        每一层有独立的爬取规则，由 css_selector 和 reg 定义

        构造方式如下：
            rules = [
                {
                    "selectors":[("#content",False),("h1",True)],
                    "reg": "<a.+? href=\\\"(.+?)\\\">",
                },
                {
                    "selectors":[],
                    "reg":r"<span class=\"year\">(.+?)</span>",
                },
            ]

            crawler.CrawlJobCore("hahaha",rules)

        json 形式如下：
        {
            "name": "hahaha",
            "rules":[
                {
                    "selectors": [
                        ["#content",false],
                        ["h1",true]
                    ],
                    "reg": "<a.+? href=\\\"(.+?)\\\">",
                },
                {
                    "selectors": [],
                    "reg":r"<span class=\"year\">(.+?)</span>"
                }
            ]
        }

        selectors 格式如下:
            [("#content",True),("h1",False)]
            每一项的第一项为 css-selector 字符串
            每一项的第二项是 bool 类型数据，表示是否选取多个元素,如果为 True 选取多个（select_elements_by_css_selector）

        reg:
            正则表达式
            作用于 selectors 最后结果的每一项
            如果 selectors 没有提供，则作用与原始页面内容
    '''
    __slots__=("name","rules")
    
    def __init__(self, name: str, rules:list):
        self.name = name 
        self.rules = []
        for rule in rules:
            rule:dict
            selectors = rule.get("selectors",[])
            reg = rule.get("reg",None)
            if (not bool(selectors)) and (not bool(reg)):
                # 如果该条规则为空，跳过
                continue
            if selectors is None:
                selectors = []
            if reg is not None:
                reg = re.compile(reg)
            self.rules.append({
                "selectors":selectors,
                "reg":reg,
            })
            
    def __str__(self):
        return "{}({})".format(self.__class__.__name__,self.dumps())

    def layer_cnt(self):
        return len(self.rules)

    def dumps(self):
        rule_ls = []
        for rule in self.rules:
            selectors = rule["selectors"]
            reg = rule["reg"]
            rule_ls.append({
                "selectors":selectors,
                "reg":reg,
            })
        x = {"name":self.name,"rules":rule_ls}
        _json_str = json.dumps(x,ensure_ascii=False)
        return _json_str

    @classmethod
    def loads(cls,_json_str):
        _json = json.loads(_json_str)
        name = _json["name"]
        rules = _json["rules"]

        assert isinstance(name,str)
        rules = rules if rules else []
        return cls(name,rules)




# __all__ = (
#     "CrawlJobCore",
# )

# import re
# import json

# class CrawlJobCore:
#     '''
#         爬虫任务内容核心
#         支持json序列化和反序列化，可以用于数据传输
#         提供了任务的name，还有获取页面内容的规则（css_selector[CSS] 和 reg[正则表达式]）

#         构造方式如下：
#             crawler.CrawlJobCore("hahaha",[("#content",True),("h1",False)],r"<span class=\"year\">(.+?)</span>")

#         selectors 格式如下:
#             [("#content",True),("h1",False)]
#             每一项的第一项为 css-selector 字符串
#             每一项的第二项是 bool 类型数据，表示是否选取多个元素,如果为 True 选取多个（select_elements_by_css_selector）

#         reg:
#             正则表达式
#             作用于 selectors 最后结果的每一项
#             如果 selectors 没有提供，则作用与原始页面内容
#     '''
#     __slots__=("name","selectors","reg")
    
#     def __init__(self, name: str, selectors: list = None, reg: str = None):
#         self.name = name 
        
#         if selectors is not None:
#             self.selectors = selectors
#         else:
#             self.selectors = []

#         if reg is not None:
#             self.reg = re.compile(reg)
#         else:
#             self.reg = None

#     def __str__(self):
#         return "{}({})".format(self.__class__.__name__,self.dumps())

#     def dumps(self):
#         x = {
#             "name":self.name,
#             "selectors":self.selectors,
#             "reg":self.reg.pattern if self.reg else None,
#         }
#         _json_str = json.dumps(x,ensure_ascii=False)
#         return _json_str

#     @classmethod
#     def loads(cls,_json_str):
#         _json = json.loads(_json_str)
#         name = _json["name"]
#         selectors = _json["selectors"]
#         reg = _json["reg"]
#         assert isinstance(name,str)
#         selectors = selectors if selectors else []
#         reg = reg if reg else None
#         return cls(name,selectors,reg)
