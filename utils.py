from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI

def get_chat_response(prompt, memory, api_key, model, platform, creativity):
    llm = None
    if platform == "阿里云":
        llm = ChatOpenAI(openai_api_key=api_key, model=model, temperature=creativity,
                           openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1")
    elif platform == "OpenAI":
        llm = ChatOpenAI(openai_api_key=api_key, model=model, temperature=creativity,
                           openai_api_base="https://api.aigc369.com/v1")
    chain = ConversationChain(llm=llm, memory=memory)

    response = chain.invoke({"input": prompt})
    return response["response"]

