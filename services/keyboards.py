from aiogram.utils.keyboard import InlineKeyboardBuilder

from models.mgo_models import FileDownload


def start_keyboard():
    # Create ReplyKeyboardMarkup
    builder = InlineKeyboardBuilder()
    
    builder.button(text="لینک دعوت", callback_data='invite_link')
    builder.button(text="کیف پول", callback_data='wallet')
    builder.button(text="لیست فایل ها", callback_data='file_list')
    builder.button(text="فایل های من", callback_data='my_files')
    
    builder.adjust(2)
    return builder.as_markup()


def file_keyboard():
    builder = InlineKeyboardBuilder()
    
    for file in FileDownload.objects.all():
        builder.button(text=file.title, callback_data=f'file_{file.id}')
    
    builder.adjust(1)
    return builder.as_markup()