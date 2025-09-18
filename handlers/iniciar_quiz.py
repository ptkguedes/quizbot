# handlers/iniciar_quiz.py
from core.enviar_quiz import enviar_quiz

async def iniciar_quiz_handler(update, context):
    quiz = context.user_data.get("quiz")
    chat_id = update.effective_chat.id
    if quiz:
        await enviar_quiz(context, chat_id, quiz)
