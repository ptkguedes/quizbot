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
from handlers.menu import enviar_menu_privado, callback_handler
from handlers.novo_quiz import iniciar_fluxo_quiz, tratar_resposta_quiz


# 🔐 Lista de administradores autorizados
ADMINS_AUTORIZADOS = [
    7477496964,5489033929 # IDs dos usuários autorizados
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
        text="Olá, querido usuário! Escolha uma opção abaixo para comandar seus quizzes:",
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
if __name__ == "__main__":
    import asyncio

    # Corrige o loop de eventos no Windows
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    TOKEN = "8486546752:AAHCdjdhljy_71qxDKMc9YT0GK6nFDn7veM"  # ⚠️ Token real — revogue após testes
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, grupo_mencao_handler))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(CommandHandler("quiz", iniciar_fluxo_quiz))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, tratar_resposta_quiz))
   
    print("🤖 Bot rodando como Bot do AMIZADES...")
    app.run_polling()

