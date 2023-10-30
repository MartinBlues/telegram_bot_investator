import telebot
from telebot import types
from strategy import calculate_profit, load_data
from data_generator import generate_random_data
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import BytesIO
import threading

# Ініціалізація бота
bot = telebot.TeleBot('6521819969:AAFmAyOnH1HLwCo4VASm9Eihk6HrGrpTUvc')

# Генерувація випадкові дані
generate_random_data()

# Завантення даних
data = load_data()

# Розрахування прибутку
stats = calculate_profit(data)

# Генерація графіку
def create_plot():
    plt.plot(data['Date'], data['Buy Price'], label='Stock Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Price History')
    plt.legend()
    plt.xticks(rotation=45)

# Функція потоку для надсилання графіку
def send_plot_thread(chat_id):
    create_plot() 

    # Збереження графіку в об’єкт BytesIO
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Відправка графіку користувачу
    bot.send_photo(chat_id, buf)

    # Закриття
    plt.close()

# Команда Handle /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton('Отримати статистику'))
    markup.add(types.KeyboardButton('Отримати графік'))
    bot.reply_to(message, "Ласкаво просимо! Щоб отримати статистику, натисніть «Отримати статистику».", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'get_stats':
        stats_message = f"Прибуткові угоди: {stats['profitable_trades']}\n"
        stats_message += f"Програшні угоди: {stats['losing_trades']}\n"
        stats_message += f"Загальний відсоток прибутку: {stats['total_profit_percentage']:.2f}%\n"

        bot.send_message(call.message.chat.id, stats_message)

# Команда Handle /send_plot
@bot.message_handler(func=lambda message: message.text == 'Отримати графік')
def send_plot(message):
     threading.Thread(target=send_plot_thread, args=(message.chat.id,)).start()
        
# Команда Handle /stats
@bot.message_handler(func=lambda message: message.text == 'Отримати статистику')
def send_stats(message):
    bot.send_message(message.chat.id, "Будь ласка, зачекайте, поки я збираю статистику...")
    bot.send_message(message.chat.id, "Ось така статистика:")
    bot.send_message(message.chat.id, f"Прибуткові угоди: {stats['profitable_trades']}")
    bot.send_message(message.chat.id, f"Програшні угоди: {stats['losing_trades']}")
    bot.send_message(message.chat.id, f"Загальний відсоток прибутку: {stats['total_profit_percentage']:.2f}%")

# Запуск бота
bot.polling()
