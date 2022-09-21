import aiogram
import requests
import json

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from decouple import config

from loader import dp, bot
from states.get_info import GetState
from keyboards.inline.get_search import items_keyboard, call_data


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!\n"
                         f"Biror musiqa nomini yoki artist nomini kiriting")


@dp.message_handler(content_types=['audio'], state=None)
async def post_music(message: types.Message):
    user_id = message.from_user.id
    print(user_id)
    msg_id = message.message_id
    music_title = message.audio.title
    performer = message.audio.performer

    TOKEN = config('TOKEN')
    BASE_URL = config('BASE_URL')
    header = {'Authorization': 'token {}'.format(TOKEN)}

    try:
        response = requests.post(url=BASE_URL, headers=header, data={
            'title': f"{performer} - {music_title}",
            'message_id': msg_id,
            'from_user_id': user_id
        })
        if response.status_code != 404:
            await message.reply('Musiqa muvoffaqiyatli saqlandi!')
        else:
            await message.reply("Uzr saqlay olmadim keyinroq urunib ko'ring")
    except requests.HTTPError or requests.ConnectionError as er:
        print(er)


@dp.message_handler(state=None)
async def search_music(message: types.Message, state: FSMContext):
    async with state.proxy() as st:
        msg_type = message.content_type

        if msg_type == 'text':
            msg = message.text

            TOKEN = config('TOKEN')
            SEARCH_URL = config('SEARCH_URL')
            header = {'Authorization': 'token {}'.format(TOKEN)}

            try:
                response = requests.get(url=f"{SEARCH_URL}{msg}", headers=header)
                data = json.loads(response.content)
                links = data['links']
                st['next'] = links['next']
                st['back'] = links['previous']
                st['end'] = msg
                reply_murkup = await items_keyboard(data)
                if data['total'] != 0:
                    title = f"Natijalar {data['total']} ta\n"
                    items = data['results']

                    for item in items:
                        title += f"{item['title']}\n"

                    await message.reply(text=title, reply_markup=reply_murkup)
                else:
                    await message.reply(text="Hech narsa topilmadi 😔", reply_markup=reply_murkup)
            except requests.HTTPError or requests.ConnectionError as er:
                print(er)
        else:
            await message.reply(text="Afsuski bunday musiqa topilmadi!")


@dp.callback_query_handler(text='next')
async def next_items(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:

        next_page = data['next']

        TOKEN = config('TOKEN')
        header = {'Authorization': 'token {}'.format(TOKEN)}

        if data['next'] is not None:
            try:
                response = requests.get(url=f"{next_page}", headers=header)

                responses = json.loads(response.content)

                links = responses['links']
                if links['next'] is not None:
                    data['next'] = links['next']
                else:
                    data['next'] = None
                if links['previous'] is not None:
                    data['back'] = links['previous']
                else:
                    data['back'] = None

                reply_murkup = await items_keyboard(responses)
                if responses['total'] != 0:
                    title = f"Natijalar {responses['total']} ta\n"
                    items = responses['results']

                    for item in items:
                        title += f"{item['title']}\n"

                    await call.message.edit_text(text=title, reply_markup=reply_murkup)
                else:
                    await call.message.reply(text="Hech narsa topilmadi 😔", reply_markup=reply_murkup)

            except requests.HTTPError or requests.ConnectionError as er:
                print(er)

    await bot.answer_callback_query(callback_query_id=call.id)


@dp.callback_query_handler(text="back")
async def back_items(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        previous_page = data['back']

        TOKEN = config('TOKEN')
        header = {'Authorization': 'token {}'.format(TOKEN)}

        if data['back'] is not None:
            try:
                response = requests.get(url=f"{previous_page}", headers=header)

                responses = json.loads(response.content)

                links = responses['links']
                if links['next'] is not None:
                    data['next'] = links['next']
                else:
                    data['next'] = None

                if links['previous'] is not None:
                    data['back'] = links['previous']
                else:
                    data['back'] = None

                reply_murkup = await items_keyboard(responses)

                if responses['total'] != 0:
                    title = f"<b>Natijalar</b> {responses['total']} ta\n"
                    items = responses['results']

                    for item in items:
                        title += f"{item['title']}\n"

                    await call.message.edit_text(text=title, reply_markup=reply_murkup)
                else:
                    await call.message.reply(text="Hech narsa topilmadi 😔", reply_markup=reply_murkup)

            except requests.HTTPError or requests.ConnectionError as er:
                print(er)

    await bot.answer_callback_query(callback_query_id=call.id)


@dp.callback_query_handler(text="end")
async def items(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await bot.answer_callback_query(callback_query_id=call.id)
        await call.message.edit_text(data['end'])
        await state.finish()


@dp.callback_query_handler(call_data.filter())
async def get_music(call: types.CallbackQuery, callback_data: dict):
    from_chat_id = call.message.chat.id
    message_id = int(callback_data.get('message_id'))
    user_id = int(callback_data.get('from_user_id'))

    await bot.answer_callback_query(callback_query_id=call.id)
    await bot.forward_message(chat_id=user_id, message_id=message_id, from_chat_id=from_chat_id)
