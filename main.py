import logging
from aiogram import Bot, Dispatcher, executor, types
from inform import token

bot = Bot(token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

hello = '''Здравствуйте.\nЯ ваш персональный помощник в поисках эмоций. Благодаря мне Вы сможете быстро подобрать музыку или картинки для поднятия или поддержания своего настроения.
\nЧтобы посмотреть, что я умею, воспользуйтесь командой /help.'''
instruction = '''/inquiry - создать новый запрос\n/answer - принять чей-то запрос\n/delete - удалить запрос
/list - вывести списоксвоих запросов\n/help - справка'''
teast_state = False
answer_state = False
delete_state = False

@dp.message_handler(commands = ['start'])
async def new_people(message: types.Message):
    await message.answer(hello)

@dp.message_handler(commands = ['help'])
async def help(message: types.Message):
    await message.answer(instruction)

@dp.message_handler(commands = ['answer'])
async def answer(message: types.Message):
    global answer_state
    answer_state = True
    await message.answer('Введите номер запроса:')

@dp.message_handler(commands = ['delete'])
async def delete(message: types.Message):
    global delete_state
    delete_state = True
    await message.answer('Введите номер запроса, который вы хотите удалить.')


@dp.message_handler(commands = ['list'])
async def list_of_orders(message: types.Message):
    answ = []
    for data in orders.items():
        if data[1][0] == message['from']['id']:
            text = data[1][1].split('/')
            answ.append(f'Номер вашего запроса: {data[0]}\nВы нуждаетесь: {text[0]}\nВы готовы отдать: {text[1]}\nКонтакты: {text[2]}')
    if answ == []:
        await message.answer('У вас нет запросов.')
    else:
        await message.answer("\n\n".join(answ))

@dp.message_handler(commands = ['inquiry'])
async def meeting(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text = 'Отмена', callback_data = 'cancellation'))
    keyboard.add(types.InlineKeyboardButton(text='Создать запрос', callback_data = 'crate_call'))
    await message.answer('Вы хотите создать новый запрос?', reply_markup = keyboard)

@dp.callback_query_handler(text = 'cancellation')
async def cancel(message: types.CallbackQuery):
    global teast_state
    teast_state = False
    await message.message.answer('Действие отменено')
    await message.answer()

@dp.callback_query_handler(text='crate_call')
async def create(message: types.CallbackQuery):
    global teast_state
    await message.message.answer('Введите данные в указанном формате: \nПредмет, который вам нужен/Что вы готовы предложить/Контакты\nПрозьба указывать данные через "/"')
    teast_state = True
    await message.answer(teast_state)

@dp.message_handler()
async def teast(message: types.Message):
    global teast_state, answer_state, delete_state, list_of_inquirys, orders, number   
    if teast_state:
        orders[str(number)] = [message['from']['id'], message.text]
        text = message.text.split('/')
        users = user_list()
        try:    
            for x in users:
                if x == str(message['from']['id']): 
                    mes = (f'Номер вашего запроса: {number}\nВы нуждаетесь: {text[0]}\nВы готовы отдать: {text[1]}\nКонтакты: {text[2]}')
                    await bot.send_message(x, mes)
                else:
                    mes = (f'Номер запроса: {number}\nНуждаюсь: {text[0]}\nГотов отдать: {text[1]}\nКонтакты: {text[2]}')
                    await bot.send_message(x, mes)
        except IndexError:
            await message.answer("Проверьте свой запрос\nСкорее всего он не соответствует требованиям оформления.")
            del orders[str(number)]
        teast_state = False
        number += 1

    elif answer_state:
        try:
            adress = orders[message.text][0]
            await bot.send_message(adress, f'Ваш запрос (№{message.text}) принят.')
            await message.answer("Запрос успешно принят.")
            del orders[message.text]
        except:
            await message.answer("Такого запроса не существует.")
        answer_state = False

    elif delete_state:
        try:
            inform = orders[message.text]
            if inform[0] == message["from"]["id"]:
                del orders[message.text]
            else:
                await message.answer("Это не ваш запрос.")
        except:
            await message.answer("Такого запроса не существует.")
        print(orders)
        delete_state = False


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)