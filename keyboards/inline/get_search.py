import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

call_data = CallbackData("show_menu", "message_id", "from_user_id")


def make_callback_data(message_id="0", from_user_id="0"):
    return call_data.new(message_id=message_id, from_user_id=from_user_id)


async def items_keyboard(data):
    item = 0
    markup = InlineKeyboardMarkup(row_width=5)

    results = data['results']
    for res in results:
        item += 1

        callback_data = make_callback_data(
            message_id=res['message_id'],
            from_user_id=res['from_user_id']
        )

        markup.insert(
            InlineKeyboardButton(text=f"{item}", callback_data=callback_data)
        )

    markup.row(
        InlineKeyboardButton(
            text="⬅",
            callback_data="back"
        ),
        InlineKeyboardButton(
            text="❌",
            callback_data="end"
        ),
        InlineKeyboardButton(
            text="➡",
            callback_data="next"
        )
    )
    return markup
