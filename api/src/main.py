import asyncio
import uvicorn
from fastapi import FastAPI
from config import Config

from repositories import Repository
from services import Service
from handlers import Handler

import logging

logging.basicConfig(level=logging.INFO)


Config.set()

repository = Repository()
service = Service(repository)
handler = Handler(service)

api = FastAPI(title="AISender")
handler.register(api)


async def test_orm_connection():
    from sqlalchemy import text

    try:
        with repository.orm.begin() as conn:
            res = conn.execute(text("SELECT NOW()"))
            logging.info(f"DATABASE CONNECTION -- success ✅")

    except Exception as e:
        logging.error(f"DATABASE CONNECTION -- error ❌ : {e}")


async def start_api():
    """Запуск uvicorn в asyncio.Task"""
    config = uvicorn.Config(api, host="0.0.0.0", port=int(Config.api.port), loop="asyncio", reload=False)
    server = uvicorn.Server(config)
    await server.serve()    


async def start_listener():
    """Запуск Telegram Listener в asyncio.Task"""
    await service.telegram.listen()


async def start_mailer():
    """Запуск Telegram Mailer в asyncio.Task"""
    await service.mailings.start()


async def main():
    await test_orm_connection()

    await service.telegram.load_clients()

    tasks = [
        asyncio.create_task(start_listener()),
        asyncio.create_task(start_api()),
        asyncio.create_task(start_mailer()),
    ]          

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
    



