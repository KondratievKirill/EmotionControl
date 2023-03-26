import logging
import dat
from random import shuffle
from aiogram import Bot, Dispatcher, executor, types
with open('inform.txt') as t:
    token = t.read()

bot = Bot(token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

hello = '''Здравствуйте.\nЯ ваш персональный помощник в поисках эмоций. Благодаря мне Вы сможете быстро подобрать музыку или картинки для поднятия или поддержания своего настроения.\nЧтобы посмотреть, что я умею, воспользуйтесь командой /help.'''
instruction = '/startwork - начать работу'

WORKMODE = ''
EMOTION = ''
DATATYPE = ''
CONTENT = []
COUNT = 0

@dp.message_handler(commands = ['start'])
async def new_people(message: types.Message):
    await message.answer(hello)

@dp.message_handler(commands = ['help'])
async def help(message: types.Message):
    await message.answer(instruction)

@dp.message_handler(commands=['startwork'])
async def choose_mode(message: types.Message()):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Поиск картинки или музыки', callback_data='mode_search'))
    keyboard.add(types.InlineKeyboardButton(text='Внести вклад в проект', callback_data='mode_append'))
    await message.answer('Выберите действие: ', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('mode_'))
async def meeting(message: types.CallbackQuery):
    global WORKMODE
    WORKMODE = message.data.split('_')[-1]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text = 'Радость 😄', callback_data = 'emotion_радость'))
    keyboard.add(types.InlineKeyboardButton(text='Грусть 😢', callback_data = 'emotion_грусть'))
    keyboard.add(types.InlineKeyboardButton(text='Гнев 😡', callback_data = 'emotion_гнев'))
    keyboard.add(types.InlineKeyboardButton(text='Спокойствие 😌', callback_data = 'emotion_спокойствие'))
    keyboard.add(types.InlineKeyboardButton(text='Мотивация 😤', callback_data = 'emotion_мотивация'))
    await message.message.answer('Выберите эмоцию: ', reply_markup=keyboard)
    await message.answer()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('emotion_'))
async def cancel(message: types.CallbackQuery):
    global EMOTION
    EMOTION = message.data.split('_')[-1]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Картинка', callback_data='data_картинка'))
    keyboard.add(types.InlineKeyboardButton(text='Музыка', callback_data='data_музыка'))
    if WORKMODE == 'search':
        text = 'Выберите, что вы хотите получить: '
    elif WORKMODE == 'append':
        text = 'Выберите, что вы хотите отравить: '
    await message.message.answer(text, reply_markup=keyboard)
    await message.answer()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('data_'))
async def forma(message: types.CallbackQuery):
    global DATATYPE, WORKMODE, EMOTION, CONTENT, COUNT
    DATATYPE = message.data.split('_')[-1]
    print(WORKMODE, DATATYPE)
    if WORKMODE == 'append':
        if DATATYPE == 'картинка':
            print('Work Block')
            await message.message.answer('Отправьте картинку в виде файла (если вы передумали, введите "."):')
        elif DATATYPE == 'музыка':
            print('Work Block')
            await message.message.answer('Отправьте ссылку на музыку (если вы передумали, введите "."):')
    elif WORKMODE == 'search':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Продолжить', callback_data='search_next'))
        keyboard.add(types.InlineKeyboardButton(text='Закончить', callback_data='search_end'))
        CONTENT = list(set(dat.get_data(DATATYPE, EMOTION)))
        print(len(CONTENT))
        if len(CONTENT) == 0:
            await message.message.answer('Упс. На данный момент у нас нет ничего из этих категорий')
        else:
            shuffle(CONTENT)

            if DATATYPE == 'картинка':
                await message.message.answer_photo(CONTENT[COUNT % len(CONTENT)], reply_markup=keyboard)
            elif DATATYPE == 'музыка':
                await message.message.answer(CONTENT[COUNT % len(CONTENT)], reply_markup=keyboard)
    await message.answer()


@dp.callback_query_handler(text=['search_next'])
async def nextStep(message: types.CallbackQuery):
    global CONTENT, COUNT, DATATYPE
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Продолжить', callback_data='search_next'))
    keyboard.add(types.InlineKeyboardButton(text='Закончить', callback_data='search_end'))
    if DATATYPE == 'картинка':
        COUNT += 1
        await message.message.answer_photo(CONTENT[COUNT % len(CONTENT)], reply_markup=keyboard)    
    elif DATATYPE == 'музыка':
        COUNT += 1
        await message.message.answer(CONTENT[COUNT % len(CONTENT)], reply_markup=keyboard)
    await message.answer()  


@dp.callback_query_handler(text=['search_end'])
async def SearchEnd(message: types.CallbackQuery):
    global WORKMODE, EMOTION, DATATYPE, CONTENT, COUNT
    WORKMODE = ''
    EMOTION = ''
    DATATYPE = ''
    CONTENT = []
    COUNT = 0
    await message.answer()



@dp.message_handler(content_types=['photo', 'text'])
async def forma(message: types.Message):
    global DATATYPE, WORKMODE, EMOTION
    if WORKMODE == 'append':
        if message.text != '.':
            if DATATYPE == 'картинка':
                file_info = await bot.get_file(message.photo[-1].file_id)
                dowloaded_file = await bot.download_file(file_info.file_path)
            
                try:
                    dat.add_data(dowloaded_file.read(), EMOTION, DATATYPE)
                except:
                    await message.answer('Произошла ошибка.\nПроверьте, пожалуйста, корректность вводимых данных и попробуйте снова')
                else:
                    await message.answer('Фото загружено. Спасибо!')
            elif DATATYPE == 'музыка':
                if message.text[0:4] == 'http':
                    try:
                        dat.add_data(message.text, EMOTION, DATATYPE)
                    except:
                        await message.answer('Произошла ошибка.\nПроверьте, пожалуйста, корректность вводимых данных и попробуйте снова')
                    else:
                        await message.answer('Ссылка загружена. Спасибо!')
                else:
                    await message.answer('Произошла ошибка.\nПроверьте, пожалуйста, корректность вводимых данных и попробуйте снова')
        DATATYPE = ''
        WORKMODE = ''
        EMOTION = ''



if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)