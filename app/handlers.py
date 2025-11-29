from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import CommandStart


import app.keyboards as kb
from app.database.requests import set_user, get_item

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id)
    await message.answer("Привет! Добро пожаловать IT Shop.",
                         reply_markup=kb.menu)
    
    
@router.callback_query(F.data == "start")
async def callback_start(callback: CallbackQuery):
    await callback.answer('Вы вернулись в главное меню.')
    await callback.message.edit_text("Добро пожаловать в IT Shop!", 
                                     reply_markup=kb.menu)
    

@router.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery):
    await callback.answer('')
    
    if callback.message.photo:
        await callback.message.delete()
        await callback.message.answer("Выберите категорию:", 
                                      reply_markup=await kb.categories())
    else:
        await callback.message.edit_text("Выберите категорию:", 
                                         reply_markup=await kb.categories())
    
    
@router.callback_query(F.data.startswith("category_"))
async def category(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.edit_text("Выберите товар по категориям:", 
                                     reply_markup=await kb.get_items(callback.data.split("_")[1]))
    
    
@router.callback_query(F.data.startswith("item_"))
async def item_handler(callback: CallbackQuery):
    item = await get_item(callback.data.split("_")[1])
    await callback.answer("")
    
    media = InputMediaPhoto(media=item.photo_url, 
                            caption=f"{item.name}\n\n{item.description}\n\nЦена: {item.price}.")
    await callback.message.edit_media(media=media, 
                                     reply_markup=kb.item_kb(callback.data.split("_")[1]))
    
    
@router.callback_query(F.data == "contacts")
async def contact_handler(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.edit_text("Наши контакты:\n\nТелефон: +1234567890\nEmail:@example.com",
                                    reply_markup=kb.menu_catalog)

    
    

    