from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .firebase import check_user_exists, get_user_tasks, get_task_requirements, upload_image
from .ai_orchestrator import run_compliance_pipeline
import tempfile
import uuid
from uuid import uuid4

router = Router()
user_task_selection = {}

@router.message(Command("start"))
async def start_handler(message: Message):
    user_id = message.from_user.id
    print(f"User ID: {user_id}")
    if check_user_exists(user_id):
        tasks = get_user_tasks(user_id)
        if not tasks:
            await message.answer("You have no tasks.")
            return

        kb = InlineKeyboardBuilder()
        for task in tasks:
            kb.button(text=task["title"], callback_data=f"task:{task['id']}")
        await message.answer("Choose your task:", reply_markup=kb.as_markup())
    else:
        await message.answer("Access denied. You're not in the system.")

@router.callback_query(F.data.startswith("task:"))
async def task_selected(call: CallbackQuery):
    task_id = call.data.split(":")[1]
    user_task_selection[call.from_user.id] = task_id
    await call.message.answer("Send a photo for this task.")

@router.message(F.photo)
async def handle_photo(message: Message, bot: Bot):
    user_id = message.from_user.id
    task_id = user_task_selection.get(user_id)

    if not task_id:
        await message.answer("Please select a task first.")
        return

    # Берём самую большую версию фото
    photo = message.photo[-1]
    
    # Получаем объект файла
    file_info = await bot.get_file(photo.file_id)

    # Временный путь для сохранения
    temp_path = tempfile.NamedTemporaryFile(delete=False).name
    await bot.download_file(file_info.file_path, destination=temp_path)

    # Загружаем в Firebase
    filename = f"{uuid4()}.jpg"
    public_url = upload_image(temp_path, filename)

    await message.answer("✅ Image uploaded. Starting analysis...")

    requirements = get_task_requirements(task_id)
    report = await run_compliance_pipeline(public_url, requirements)

    await message.answer(f"<b>📄 Report:</b>\n<pre>{report}</pre>")
