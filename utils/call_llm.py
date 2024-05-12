from zhipuai_sdk.zhipuai import ZhipuAI
from openai import OpenAI 


def query_llm(api_key, model_name, user_input):
    if 'glm' in model_name.lower():
        client = ZhipuAI(api_key=api_key) 
    elif 'gpt' in model_name.lower():
        client = OpenAI(api_key=api_key)
    else:
        return None

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "你是一个撰写代码的专家，请依据用户输入信息，来撰写代码，直接输出代码函数，代码中不要包含注释。"
            },
            {
                "role": "user",
                "content": user_input,
            }
        ],
        model=model_name,
        top_p=0.7,
        temperature=0.9
    )

    return chat_completion.choices[0].message.content

if __name__ == '__main__':
    key = ""
    result = query_llm(key, "glm-4", "冒泡排序")
    print(result)
