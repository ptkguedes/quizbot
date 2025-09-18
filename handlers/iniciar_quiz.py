import asyncio
from telegram import Update
from telegram.ext import ContextTypes

# 🧠 Envia o quiz pergunta por pergunta
async def enviar_quiz(context: ContextTypes.DEFAULT_TYPE, chat_id: int, quiz: list):
    tempo = int(context.user_data.get("tempo", 30))  # Tempo por pergunta

    for pergunta in quiz:
        enunciado = pergunta.get("enunciado", "Pergunta sem enunciado")
        alternativas = pergunta.get("alternativas", [])
        correta = pergunta.get("correta")

        # Validação básica
        if not alternativas or correta not in alternativas:
            alternativas = alternativas or ["Alternativa A", "Alternativa B"]
            correta = alternativas[0]  # fallback seguro

        try:
            await context.bot.send_poll(
                chat_id=chat_id,
                question=enunciado,
                options=alternativas,
                type="quiz",
                correct_option_id=alternativas.index(correta),
                is_anonymous=False
            )
        except Exception as e:
            await context.bot.send_message(chat_id=chat_id, text=f"⚠️ Erro ao enviar pergunta: {str(e)}")

        await asyncio.sleep(tempo)

    await context.bot.send_message(chat_id=chat_id, text="✅ Quiz finalizado!")

# ▶️ Handler que inicia o envio do quiz
async def iniciar_quiz_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    quiz = context.user_data.get("quiz")
    chat_id = update.effective_user.id

    if not quiz or not isinstance(quiz, list):
        await context.bot.send_message(chat_id=chat_id, text="⚠️ Nenhum quiz encontrado ou formato inválido.")
        return

    await context.bot.send_message(chat_id=chat_id, text="▶️ Iniciando o quiz...")
    await enviar_quiz(context, chat_id, quiz)
