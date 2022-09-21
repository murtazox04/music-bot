from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from decouple import config

bot = Bot(token=config('BOT_TOKEN'), parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# data = {
#     "links": {"next": "http://127.0.0.1:8000/api/search/?page=2&search=as", "previous": null}, "per_page": 10,
#     "current_page": 1, "total_pages": 2, "total": 12,
#     "results": [{"title": "asdgjj", "message_id": 32432, "from_user_id": 234324},
#                 {"title": "asdhhg", "message_id": 124421, "from_user_id": 432},
#                 {"title": "asdfgj", "message_id": 123, "from_user_id": 123},
#                 {"title": "asfhjjh", "message_id": 53345, "from_user_id": 56765},
#                 {"title": "asd", "message_id": 456456, "from_user_id": 65467},
#                 {"title": "asd", "message_id": 12344, "from_user_id": 12344},
#                 {"title": "asd", "message_id": 214, "from_user_id": 5643},
#                 {"title": "asdf", "message_id": 321, "from_user_id": 345},
#                 {"title": "asd", "message_id": 123123, "from_user_id": 34324},
#                 {"title": "asd", "message_id": 312, "from_user_id": 1123}]}
