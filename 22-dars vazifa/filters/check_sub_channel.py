from data.config import CHANNELS
from aiogram import filters,Bot
from aiogram.types import Message

class IsCheckSubChannels(filters.Filter):
    # for channel in CHANNELS:
    async def __call__(self,message:Message,bot:Bot):
        result = await bot.get_chat_member(CHANNELS[0],message.from_user.id)
        if result.status in ["member","adminstrator","creator"]:
            return False
        else:
            ChatInviteLink = await bot.create_chat_invite_link(CHANNELS[0])
            # await message.answer(f"{ChatInviteLink.invite_link} kanaliga azo bo'ling")
            return True