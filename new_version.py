import telebot
from openai import OpenAI
import os
from dotenv import load_dotenv
from telebot.types import Message

load_dotenv()

TELEGRAM_TOKEN = os.getenv("token_telegram")
OPENAI_API_KEY = os.getenv("token_ai")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

client = OpenAI(
    api_key=OPENAI_API_KEY,
)


def load_prompt():
    with open('prompt.txt', 'r', encoding='utf-8') as file:
        return file.read()


def create_gpt_answer(message: Message):
    try:
        # Вопрос добавляю в историю сообщений
        messages.append({"role": "user", "content": message.text})

        # Генерация ответа
        new_response = client.chat.completions.create(
            model="gpt-4o", messages=messages
        )
        reply = new_response.choices[0].message.content.strip()
        # Ответ gpt добавляю в историю сообщений
        messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        print(e)
        reply = "Произошла ошибка при генерации ответа. Пожалуйста, попробуйте еще раз позже."

    return reply


knowledge_base = load_prompt()

messages = [
    {"role": "system",
     "content": "Вы - полезный ассистент, предназначенный для ответов на вопросы по Хакатону и латокену а так же"
                "тестирования кандидатов на основе теста хакатона. (После ответа на вопрос пользователя ТЫ ДОЛЖЕН "
                "ЗАДАВАТЬ ВОПРОС ПО ТЕСТИРОВАНИЮ И ЕСЛИ ПОЛЬЗОВАТЕЛЬ ОТВЕТИЛ ПРАВИЛЬНО НА ТВОЙ ВОПРОС ОТПРАВЛЯЙ В ЧАТ"
                "ЕМУ ПРАВИЛЬНО:"},
    {"role": "system", "content": f"Твоя база знаний: {knowledge_base}"},
    {"role": "user", "content": "Привет! Как дела?"},
    {"role": "assistant", "content": "Привет! У меня всё хорошо. Готов помочь тебе. Начнем с твоего первого вопроса?"},
]


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, созданный для помощи в хакатоне Латокен. Задайте мне вопрос.")


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Просто задайте мне вопрос, и я постараюсь помочь!")


@bot.message_handler(content_types=['text'])
def answer_to_hacaton(message: Message):
    print(message.chat.type)
    if message.chat.type in ['group', 'supergroup']:
        if (message.text.lower().startswith("бот") or "хакатон" in message.text.lower() or
                message.text.lower().startswith("ответ")):
            reply = create_gpt_answer(message)
            bot.send_message(message.chat.id, reply)
    elif message.chat.type in ["private"]:
        reply = create_gpt_answer(message)
        bot.send_message(message.chat.id, reply)


# Запуск бота
bot.infinity_polling()
