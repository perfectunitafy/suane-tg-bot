from aiogram import Router, F, types

router = Router()

@router.message(F.new_chat_members | F.left_chat_member | F.new_chat_title | F.new_chat_photo | F.delete_chat_photo | F.pinned_message)
async def delete_system_messages(message: types.Message):
    try:
        await message.delete()
    except Exception:
        pass
