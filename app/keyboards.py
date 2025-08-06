from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main_ru = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Настройки'),
                                     KeyboardButton(text='Мой аккаунт')],
                                     [KeyboardButton(text='Премиум'),
                                     KeyboardButton(text='О нас')]],
                           resize_keyboard=True)

main_en = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Settings'),
                                     KeyboardButton(text='My account')],
                                     [KeyboardButton(text='Premium'),
                                     KeyboardButton(text='About us')]],
                           resize_keyboard=True)

settings_ru = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Выбор языка', callback_data='language')],
                                                 [InlineKeyboardButton(text='Выбор модели', callback_data='model')]])

settings_en = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Choose languages', callback_data='language')],
                                                 [InlineKeyboardButton(text='Choose models', callback_data='model')]])

languages = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Русский', callback_data='Rus_lang')],
                                                  [InlineKeyboardButton(text='English', callback_data='Eng_lang')]])