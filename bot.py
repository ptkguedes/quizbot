import os
import asyncio
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
from handlers.novo_quiz import (
    iniciar_fluxo_quiz,
    tratar_resposta_quiz,
    tratar_callback_quiz
)
from handlers.iniciar_quiz import iniciar_quiz_handler
from dotenv import load_dotenv

# 🔐 Carrega variáveis do .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# 🔐 Lista de administradores autorizados (privado)
ADMINS_AUTORIZADOS = [
    7477496964,  # Jake
    5489033929   # Maria
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

# 🚀 Inicialização do bot
if __name__ == "__main__":
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    app = ApplicationBuilder().token(TOKEN).build()

    # 🧠 Handlers principais — ordem reorganizada
    app.add_handler(CommandHandler("quiz", iniciar_fluxo_quiz))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, tratar_resposta_quiz))
    app.add_handler(CallbackQueryHandler(tratar_callback_quiz, pattern="^(qtd_|alt_|tempo_|dif_|confirmar_quiz)$"))
    app.add_handler(CallbackQueryHandler(iniciar_quiz_handler, pattern="^iniciar_quiz$"))
    app.add_handler(CallbackQueryHandler(callback_handler, pattern="^(novo_quiz|meus_quizzes|estatisticas|parar_quiz)$"))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, grupo_mencao_handler))

    print("🤖 Bot rodando como Bot do AMIZADES...")
    app.run_polling()
