import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# 🔐 Lista de administradores autorizados (definidos manualmente)
ADMINS_AUTORIZADOS = [
    7477496964,  # Substitua com seu ID real
    987654321,  # Outro admin
]

# 🔍 Verifica se o usuário é admin no grupo
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    member = await context.bot.get_chat_member(chat_id, user_id)
    return member.status in ['administrator', 'creator']

# 🔐 Verifica se o usuário é autorizado no privado
def is_autorizado(user_id: int) -> bool:
    return user_id in ADMINS_AUTORIZADOS

# 📣 Handler para quando o bot é mencionado no grupo
async def grupo_mencao_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text and f"@{context.bot.username}" in update.message.text:
        user_id = update.effective_user.id
        if await is_admin(update, context):
            await enviar_menu_privado(update, context)

# 📬 Envia o menu privado com botões inline
async def enviar_menu_privado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🆕 Novo Quiz", callback_data='novo_quiz')],
        [InlineKeyboardButton("📁 Meus Quizzes", callback_data='meus_quizzes')],
        [InlineKeyboardButton("📊 Estatísticas", callback_data='estatisticas')],
        [InlineKeyboardButton("🛑 Parar Quiz", callback_data='parar_quiz')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text="Olá, comandante do quiz! Escolha uma opção abaixo:",
        reply_markup=reply_markup
    )

# 🎮 Handler para os botões inline
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if not is_autorizado(user_id):
        await query.edit_message_text("⚠️ Você não está autorizado a usar este menu.")
        return

    match query.data:
        case 'novo_quiz':
            await query.edit_message_text("🎉 Vamos começar um novo quiz! Escolha o tema...")
            # Aqui entra a lógica de seleção de tema
        case 'meus_quizzes':
            await query.edit_message_text("📁 Aqui estão seus quizzes salvos:")
            # Lógica para listar quizzes
        case 'estatisticas':
            await query.edit_message_text("📊 Estatísticas dos quizzes:")
            # Lógica para mostrar estatísticas
        case 'parar_quiz':
            await query.edit_message_text("🛑 Quiz encerrado com sucesso.")
            # Lógica para parar quiz

# 🚀 Inicialização do bot
async def main():
    TOKEN = os.getenv("BOT_TOKEN") or "SEU_TOKEN_AQUI"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, grupo_mencao_handler))
    app.add_handler(CallbackQueryHandler(callback_handler))

    print("🤖 Bot rodando...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
