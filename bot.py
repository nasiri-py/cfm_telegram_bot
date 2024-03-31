import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from mongoengine import connect

from common.utils import load_config
import services.messages as messages
import services.keyboards as keyboards
from models.mgo_models import User



# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
config = {}
bot = None



@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Handles the /start command from users.

    Args:
        message (Message): The incoming message object.
    Returns:
        None
    """

    # Check if the user already exists in the database
    user = User.objects.filter(telegram_id=message.from_user.id).first()
    new_user = False
    if not user:
        new_user = True
        # Prepare user data for creation
        user_data = {
            "telegram_id": message.from_user.id,
            "username": message.from_user.username,
            "full_name": message.from_user.full_name,
            "is_premium": message.from_user.is_premium
        }
    
    # Split the message text and process based on the length
    num_words = len(message.text.split())
    print(message.text)
    match num_words:
        # If only the command is send (just /start)
        case 1:
            # If it's a new user, create a record for them in the database
            if new_user:
                User.objects.create(**user_data)
        # If command has two arguments (ex: /start ref_1111111)
        case 2:
            # Extract the second part of the command, if present
            _, query_command = message.text.split()
            if query_command.startswith("ref_"):
                # Retrieve the inviter from the database
                inviter = User.objects.filter(telegram_id=int(query_command.split('_')[1])).first()
                # If it's a new user and the inviter exists, update inviter's invites count and create the new user
                if new_user and inviter:
                    inviter.invites += 1
                    inviter.save()
                    user_data["inviter"] = inviter.telegram_id
                    User.objects.create(**user_data)
                    # Send a message to the inviter acknowledging the referral
                    await bot.send_message(
                        chat_id=inviter.telegram_id, text=messages.inviter_message.format(full_name=message.from_user.full_name))
                else:
                    # If there's no inviter or the user already exists, simply create the user
                    User.objects.create(**user_data)
                    
    # Send the start message to the user with a keyboard
    await message.answer(f"{messages.start} {hbold(message.from_user.username)}!",
                             reply_markup=keyboards.start_keyboard())
    


@dp.callback_query()
async def handle_callback_query(callback_query: types.callback_query):
    # Extracting callback_data from the InlineKeyboardButton
    callback_data = callback_query.data
    # Here you can parse the callbak_data and take actions accordingly
    match (callback_data):
        case "invite_link":
            await callback_query.message.answer(
                messages.invite_link.format(bot_username=config['telegram']['username'],
                                            user_id=callback_query.from_user.id))
        case "wallet":
            user = User.objects.get(telegram_id=int(callback_query.from_user.id), reply_markup=keyboards.start_keyboard())
            await callback_query.message.answer(messages.wallet_balance.format(user.wallet), reply_markup=keyboards.start_keyboard())
        case "file_list":
            await callback_query.message.answer("You clicked the file_list!", reply_markup=keyboards.start_keyboard())
        case "my_files":
            await callback_query.message.answer("You clicked the my_files!", reply_markup=keyboards.start_keyboard())
        


async def main() -> None:
    # Load configs from yaml file
    global config, bot
    config = load_config("config.yaml")
    # Connect to db
    db = config['db']
    connect(
        db=db['dbname'],
        username=db['username'],
        password=db['password']
    )
    # Bot token can be obtained via https://t.me/BotFather
    TOKEN = config['telegram']['token']
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


def bot_runner():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())