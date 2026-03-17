import os
from dotenv import load_dotenv

# 加载.env文件中的变量到Windows系统的环境变量
load_dotenv()
#通过os.getenv获取
KEY = os.getenv("DP_SK_API_KEY")
print(KEY)


#测试.json()方法
text1=   {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "千禧年七大数学难题是**克雷数学研究所**于2000年公布的七个未解决的经典数学问题，每个问题的解答可获得100万美元奖金。具体如下：  \n\n1. **P与NP问题**  \n   判断计算问题的易解性（P类）与可验证性（NP类）是否等价。  \n\n2. **霍奇猜想**  \n   探究代数几何中复杂形状能否用简单几何构件组合表示。  \n\n3. **庞加莱猜想**  \n   已由佩雷尔曼证明（2003年），确认三维球面是单连通闭三维流形。  \n\n4. **黎曼猜想**  \n   关于黎曼ζ函数非平凡零点的实部是否均为1/2，与素数分布密切相关。  \n\n5. **杨-米尔斯存在性与质量间隙**  \n   在量子场论中证明杨-米尔斯理论存在性，并解释质量间隙现象。  \n\n6. **纳维-斯托克斯方程解的存在性与光滑性**  \n   确定描述流体运动的方程是否总有光滑解。  \n\n7. **贝赫和斯维讷通-戴尔猜想**  \n   探究代数方程的有理数解与相关L函数的关系。  \n\n至今除庞加莱猜想外，其余六题仍未解决。"
      },
      "logprobs": None,
      "finish_reason": "stop"
    }
test2="千禧年七大数学难题是**克雷数学研究所**于2000年公布的七个未解决的经典数学问题"
"""
print(test2.json())  
AttributeError: 'str' object has no attribute 'json'

print(text1.json())
AttributeError: 'dict' object has no attribute 'json'
"""
import json
json_text1=json.dumps(text1,ensure_ascii=False)
# print(json_text1)
print(type(json_text1))
print(json_text1.json())