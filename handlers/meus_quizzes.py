# handlers/meus_quizzes.py
async def listar_quizzes(update, context):
    # Exemplo: buscar quizzes salvos no context.user_data
    quizzes = context.user_data.get("quizzes", [])
    if not quizzes:
        await update.message.reply_text("📁 Você ainda não tem quizzes salvos.")
        return
    # Enviar lista com botões
