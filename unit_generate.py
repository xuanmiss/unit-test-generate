from flask import Blueprint, request, jsonify
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
import re

from langchain_core.prompts import PromptTemplate

load_dotenv('.env')
CUS_OPENAI_API_BASE = os.environ["CUS_OPENAI_API_BASE"]
CUS_OPENAI_TOKEN = os.environ["CUS_OPENAI_TOKEN"]
CUS_OPENAI_MODEL = os.environ["CUS_OPENAI_MODEL"]
llm = ChatOpenAI(
    openai_api_key=CUS_OPENAI_TOKEN,
    openai_api_base=CUS_OPENAI_API_BASE,
    model=CUS_OPENAI_MODEL,
    # temperature=0.1,
    streaming=False,
    max_tokens=10000
)

template = '''
    SYSTEM
    你是一个精通Java和Junit,Mockito库的测试工程师。

    请为下面代码和Java类的基本信息生成单元测试代码，不要返回代码解释和其他内容，只需要返回代码文本即可。

    代码：
    {code}

    Java类的基本信息：
    代码使用了SpringBoot框架，类名为{class_name}

    测试方法：
    '''
prompt = PromptTemplate(template=template, input_variables=["code", "class_name"])
unit_test_chain = LLMChain(llm=llm, prompt=prompt)

unit_api = Blueprint("unit_generate", __name__)



@unit_api.route("/testCode", methods=['POST'])
def generate_test_code():
    json_data = request.json
    if not json_data:
        return jsonify(error='No JSON data found'), 400
    code = json_data.get('code')
    class_name = json_data.get('className')
    test_code = unit_test_chain.run(code=code, class_name=class_name)
    return extract_code_snippets(test_code)


def extract_code_snippets(markdown_text):
    pattern = r'```.*?\n([\s\S]*?)\n```'
    # pattern = r'```.*?\n([\s\S]*?)\n```|`([^`]+)`'
    code_snippets = re.findall(pattern, markdown_text, re.MULTILINE | re.DOTALL)

    # 处理两种匹配情况，第一组是多行代码块，第二组是单行代码
    # extracted_snippets = []
    # for snippet in code_snippets:
    #     # 如果是多行代码块（三个反引号包裹）
    #     if snippet[0]:
    #         extracted_snippets.append(snippet[0])
    #     # 如果是单行代码（反引号包裹）
    #     elif snippet[1]:
    #         extracted_snippets.append(snippet[1])

    return code_snippets[0]
