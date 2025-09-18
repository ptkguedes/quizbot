# handlers/estatisticas.py
async def mostrar_estatisticas(update, context):
    await update.message.reply_text("📊 Você criou 5 quizzes. O mais jogado foi sobre 'História'.")
