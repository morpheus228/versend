import asyncio
from repositories import Repository
from config import Config

# from langchain_openai import ChatOpenAI
# from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


SYSTEM_PROMT = "Ты — виртуальный ассистент премиального агентства недвижимости в Дубае. Твоя задача — заинтересовать пользователей, построить доверительные отношения и побудить их к взаимодействию с агентством (например, записаться на консультацию, посмотреть объекты или оставить контакты). Общайся профессионально, дружелюбно и убедительно, подчеркивая уникальные преимущества недвижимости в Дубае."


class AIService:
    def __init__(self):
        pass
        # self.llm = ChatOpenAI(
        #     model = "gpt-4o-mini", 
        #     base_url = "https://api.proxyapi.ru/openai/v1",
        #     api_key = "sk-05GCg98nx4SZVQAWJCZ4p31pcFUkjP04"
        # )

    async def get_answer(self, messages_history: list[dict]) -> str:
        # history = [SystemMessage(content=SYSTEM_PROMT)] 

        # for message in messages_history[::-1]:
        #     if message['from_user']:
        #         history.append(HumanMessage(content=message['text']))
        #     else:
        #         history.append(AIMessage(content=message['text']))
        
        # # Вызов модели 
        # response = await self.llm.ainvoke(history) 
        
        # return response.content
        pass

        





    



