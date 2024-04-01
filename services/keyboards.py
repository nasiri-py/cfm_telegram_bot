from aiogram.utils.keyboard import InlineKeyboardBuilder

import services.messages as messages


def start_keyboard():
    # Create ReplyKeyboardMarkup
    builder = InlineKeyboardBuilder()
    builder.button(text="لینک دعوت", callback_data='invite_link')
    builder.button(text="کیف پول", callback_data='wallet')
    builder.button(text="لیست فایل ها", callback_data='file_list')
    builder.button(text="فایل های من", callback_data='my_files')
    builder.adjust(2)
    return builder.as_markup()
