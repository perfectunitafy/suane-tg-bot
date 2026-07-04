from aiogram import Router, types, F

router = Router()

@router.message(F.content_type.in_({'new_chat_members', 'left_chat_member', 'new_chat_photo'}))
async def delete_system_msg(message: types.Message):
    try:
        await message.delete()
    except:
        pass

@router.message(F.new_chat_members)
async def greet_new_user(message: types.Message):
    await message.answer(f"Привет, {message.new_chat_members[0].full_name}! Добро пожаловать.")
