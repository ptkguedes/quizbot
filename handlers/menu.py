from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# 📩 Envia o menu privado para o usuário
async def enviar_menu_privado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧠 Novo Quiz", callback_data="novo_quiz")],
        [InlineKeyboardButton("📋 Meus Quizzes", callback_data="meus_quizzes")],
        [InlineKeyboardButton("📊 Estatísticas", callback_data="estatisticas")],
        [InlineKeyboardButton("🛑 Parar Quiz", callback_data="parar_quiz")]
    ]

    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text="📚 Menu principal do QuizBot:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# 🎮 Trata os botões clicados no menu
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "novo_quiz":
        await query.message.reply_text("🧠 Iniciando novo quiz... Use /quiz no privado.")
    elif data == "meus_quizzes":
        await query.message.reply_text("📋 Você ainda não tem quizzes salvos.")
    elif data == "estatisticas":
        await query.message.reply_text("📊 Estatísticas ainda não disponíveis.")
    elif data == "parar_quiz":
        await query.message.reply_text("🛑 Quiz encerrado.")
