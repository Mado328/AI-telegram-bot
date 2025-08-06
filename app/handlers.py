from aiogram import Router, F
from aiogram.types import Message, Contact, FSInputFile, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import sqlite3
import app.keyboards as kb

from app.generate import ai_generate

router = Router()
# класс определения состояния использующийся в функции stop_flood
class Gen(StatesGroup):
    wait = State()

@router.message(CommandStart())
async def cmd_start(message: Contact, state: FSMContext):


    # сохранение информации о пользователе в базу данных
    con = sqlite3.connect("./database.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                username TEXT,
                nickname TEXT,
                language TEXT)""")
    if message.from_user.language_code != 'ru' and message.from_user.language_code != 'en':
        data = [(f'{message.from_user.id}', f'{message.from_user.username}', f'{message.from_user.full_name}',
                 'en')]
    else:
        data = [(f'{message.from_user.id}',f'{message.from_user.username}',f'{message.from_user.full_name}',f'{message.from_user.language_code}')]

    cur.executemany(f"INSERT OR IGNORE INTO users VALUES(?,?,?,?)", data)
    con.commit()

    res = cur.execute(f"SELECT language FROM users WHERE id = '{message.from_user.id}'")
    data = res.fetchone()

    language = data[0]

    res = cur.execute(f"SELECT start from language_text WHERE code_id='{language}'")
    data = res.fetchone()


    cur.close()
    con.close()

    if language == 'en':
        await message.answer(data[0],
        reply_markup=kb.main_en)
    else:
        await message.answer(data[0],
        reply_markup=kb.main_ru)

# функция для остановки флуда
@router.message(Gen.wait)
async def stop_flood(message: Message):
    con = sqlite3.connect("./database.db")
    cur = con.cursor()

    res = cur.execute(f"SELECT language FROM users WHERE id = '{message.from_user.id}'")
    data = res.fetchone()
    res = cur.execute(f"SELECT wait from language_text WHERE code_id='{data[0]}'")
    data = res.fetchone()

    cur.close()
    con.close()

    await message.answer(data[0])
# кнопка "Настройки"
@router.message(F.text == 'Настройки')
@router.message(F.text == 'Settings')
async def settings(message: Message):
    con = sqlite3.connect("./database.db")
    cur = con.cursor()

    res = cur.execute(f"SELECT language FROM users WHERE id = '{message.from_user.id}'")
    data = res.fetchone()

    language = data[0]

    res = cur.execute(f"SELECT settings from language_text WHERE code_id='{language}'")
    data = res.fetchone()

    cur.close()
    con.close()

    if language =='en':
        await message.answer(data[0],
        reply_markup=kb.settings_en)
    else:
        await message.answer(data[0],
        reply_markup=kb.settings_ru)

@router.callback_query(F.data == 'language')
async def language(callback: CallbackQuery):
    con = sqlite3.connect("./database.db")
    cur = con.cursor()

    res = cur.execute(f"SELECT language FROM users WHERE id = '{callback.from_user.id}'")
    data = res.fetchone()

    language = data[0]

    res = cur.execute(f"SELECT settings from language_text WHERE code_id='{language}'")
    data = res.fetchone()

    cur.close()
    con.close()

    await callback.answer(' ')
    if language == 'en':
        await callback.message.answer('Select language', reply_markup=kb.languages)
    else:
        await callback.message.answer('Выберите язык', reply_markup=kb.languages)

@router.callback_query(F.data == 'model')
async def models(callback: CallbackQuery):
    con = sqlite3.connect("./database.db")
    cur = con.cursor()

    res = cur.execute(f"SELECT language FROM users WHERE id = '{callback.from_user.id}'")
    data = res.fetchone()

    language = data[0]

    res = cur.execute(f"SELECT settings from language_text WHERE code_id='{language}'")
    data = res.fetchone()

    cur.close()
    con.close()

    await callback.answer(' ')
    if language == 'en':
        await callback.message.answer('There is currently only one AI model available.', reply_markup=kb.languages)
    else:
        await callback.message.answer('В данный момент доступна только одна модель ИИ', reply_markup=kb.languages)

@router.callback_query(F.data == 'Eng_lang')
async def eng_language(callback: CallbackQuery):
    con = sqlite3.connect("./database.db")
    cur = con.cursor()

    cur.execute(f"SELECT id FROM users")
    cur.execute(f"UPDATE users SET language= 'en' WHERE id= '{callback.from_user.id}'")

    con.commit()
    cur.close()
    con.close()
    await callback.message.answer('Language changed', reply_markup=kb.main_en)
    await callback.answer(' ')
@router.callback_query(F.data == 'Rus_lang')
async def rus_language(callback: CallbackQuery):
    con = sqlite3.connect("./database.db")
    cur = con.cursor()

    cur.execute(f"UPDATE users SET language= 'ru' WHERE id= '{callback.from_user.id}'")

    con.commit()
    cur.close()
    con.close()
    await callback.message.answer('Язык изменён', reply_markup=kb.main_ru)
    await callback.answer(' ')

# кнопка "О нас"
@router.message(F.text == 'О нас')
@router.message(F.text == 'About us')
async def about_us(message: Message):
    con = sqlite3.connect("./database.db")
    cur = con.cursor()

    res = cur.execute(f"SELECT language FROM users WHERE id = '{message.from_user.id}'")
    data = res.fetchone()
    res = cur.execute(f"SELECT about_us from language_text WHERE code_id='{data[0]}'")
    data = res.fetchone()

    cur.close()
    con.close()

    await message.answer(data[0])
# кнопка "Мой аккаунт"
@router.message(F.text == 'Мой аккаунт')
@router.message(F.text == 'My account')
async def my_account(message: Message):
    con = sqlite3.connect("./database.db")
    cur = con.cursor()

    res = cur.execute(f"SELECT language FROM users WHERE id = '{message.from_user.id}'")
    data = res.fetchone()

    language = data[0]

    cur.close()
    con.close()

    if language == 'en':
        await message.answer(f'''User ID:{message.from_user.id}\nSubscription Type: Free\nAI Model: DeepSeek R1\nInterface Language: {message.from_user.language_code}''')

    else:
        await message.answer(f'''ID пользователя: {message.from_user.id}\nТип подписки: Free\nМодель ИИ: DeepSeek R1\nЯзык интерфейса: {message.from_user.language_code}''')

# кнопка "Премиум"
@router.message(F.text == 'Премиум')
@router.message(F.text == 'Premium')
async def premium(message: Message):
    con = sqlite3.connect("./database.db")
    cur = con.cursor()

    res = cur.execute(f"SELECT language FROM users WHERE id = '{message.from_user.id}'")
    data = res.fetchone()
    res = cur.execute(f"SELECT premium from language_text WHERE code_id='{data[0]}'")
    data = res.fetchone()

    cur.close()
    con.close()

    await message.answer(data[0])

# функция получения вопроса пользователя и отправки ответа от ИИ
@router.message()
async def generating(message: Message, state: FSMContext):
    await state.set_state(Gen.wait)

    print(f'################ {message.from_user.username} ################',
            '\n-----------------Вопрос пользователя------------------\n',
                                    message.text,
            '\n------------------------------------------------------\n')

    response = await ai_generate(message.text, " ")
    await message.answer(f'{response}', parse_mode="HTML")

    print('\n----------------------Ответ бота----------------------\n',
                                    response,
          '\n------------------------------------------------------\n')
    await state.clear()

