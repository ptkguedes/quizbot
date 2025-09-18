from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# 🚀 Inicia o fluxo pedindo o tema
async def iniciar_fluxo_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧠 Qual será o tema do quiz?")
    context.user_data.clear()
    context.user_data['etapa'] = 'tema'

# 🧠 Trata respostas enviadas por texto (tema)
async def tratar_resposta_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    etapa = context.user_data.get('etapa')

    if etapa == 'tema':
        context.user_data['tema'] = update.message.text
        context.user_data['etapa'] = 'qtd_perguntas'
        await enviar_opcoes_perguntas(update)

# 🎮 Trata cliques nos botões inline
async def tratar_callback_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("qtd_"):
        context.user_data['qtd'] = int(data.split("_")[1])
        context.user_data['etapa'] = 'opcoes'
        await enviar_opcoes_alternativas(query)

    elif data.startswith("alt_"):
        context.user_data['opcoes'] = int(data.split("_")[1])
        context.user_data['etapa'] = 'tempo'
        await enviar_opcoes_tempo(query)

    elif data.startswith("tempo_"):
        context.user_data['tempo'] = int(data.split("_")[1])
        context.user_data['etapa'] = 'dificuldade'
        await enviar_opcoes_dificuldade(query)

    elif data.startswith("dif_"):
        dificuldade = data.split("_")[1]
        context.user_data['dificuldade'] = dificuldade.capitalize()
        context.user_data['etapa'] = 'confirmar'
        await confirmar_quiz(query, context)

    elif data == "confirmar_quiz":
        await query.edit_message_text("🧠 Gerando quiz com IA... Aguarde!")
        # Aqui você pode chamar o quiz_engine para gerar as perguntas

# 📊 Botões: número de perguntas
async def enviar_opcoes_perguntas(update_or_query):
    keyboard = [
        [InlineKeyboardButton("15", callback_data='qtd_15')],
        [InlineKeyboardButton("20", callback_data='qtd_20')],
        [InlineKeyboardButton("25", callback_data='qtd_25')],
        [InlineKeyboardButton("30", callback_data='qtd_30')]
    ]
    await update_or_query.message.reply_text("📊 Quantas perguntas?", reply_markup=InlineKeyboardMarkup(keyboard))

# 🔢 Botões: número de alternativas
async def enviar_opcoes_alternativas(update_or_query):
    keyboard = [
        [InlineKeyboardButton("3", callback_data='alt_3')],
        [InlineKeyboardButton("4", callback_data='alt_4')],
        [InlineKeyboardButton("5", callback_data='alt_5')]
    ]
    await update_or_query.message.reply_text("🔢 Quantas alternativas por pergunta?", reply_markup=InlineKeyboardMarkup(keyboard))

# ⏱️ Botões: tempo por pergunta
async def enviar_opcoes_tempo(update_or_query):
    keyboard = [
        [InlineKeyboardButton("15s", callback_data='tempo_15')],
        [InlineKeyboardButton("30s", callback_data='tempo_30')],
        [InlineKeyboardButton("60s", callback_data='tempo_60')],
        [InlineKeyboardButton("90s", callback_data='tempo_90')]
    ]
    await update_or_query.message.reply_text("⏱️ Tempo por pergunta?", reply_markup=InlineKeyboardMarkup(keyboard))

# 🎯 Botões: dificuldade
async def enviar_opcoes_dificuldade(update_or_query):
    keyboard = [
        [InlineKeyboardButton("Fácil", callback_data='dif_facil')],
        [InlineKeyboardButton("Média", callback_data='dif_media')],
        [InlineKeyboardButton("Difícil", callback_data='dif_dificil')]
    ]
    await update_or_query.message.reply_text("🎯 Escolha a dificuldade:", reply_markup=InlineKeyboardMarkup(keyboard))

# ✅ Confirmação final
async def confirmar_quiz(update_or_query, context: ContextTypes.DEFAULT_TYPE):
    dados = context.user_data
    resumo = (
        f"✅ Tema: {dados['tema']}\n"
        f"📊 Perguntas: {dados['qtd']}\n"
        f"🔢 Alternativas: {dados['opcoes']}\n"
        f"⏱️ Tempo: {dados['tempo']}s\n"
        f"🎯 Dificuldade: {dados['dificuldade']}"
    )
    keyboard = [[InlineKeyboardButton("✅ Gerar Quiz", callback_data='confirmar_quiz')]]
    await update_or_query.message.reply_text(resumo, reply_markup=InlineKeyboardMarkup(keyboard))
