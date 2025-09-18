# handlers/novo_quiz.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def iniciar_fluxo_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧠 Qual será o tema do quiz?")
    context.user_data.clear()
    context.user_data['etapa'] = 'tema'

async def tratar_resposta_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    etapa = context.user_data.get('etapa')

    if etapa == 'tema':
        context.user_data['tema'] = update.message.text
        context.user_data['etapa'] = 'qtd_perguntas'
        await enviar_opcoes_perguntas(update)

    elif etapa == 'qtd_perguntas':
        context.user_data['qtd'] = int(update.message.text)
        context.user_data['etapa'] = 'opcoes'
        await enviar_opcoes_alternativas(update)

    elif etapa == 'opcoes':
        context.user_data['opcoes'] = int(update.message.text)
        context.user_data['etapa'] = 'tempo'
        await enviar_opcoes_tempo(update)

    elif etapa == 'tempo':
        context.user_data['tempo'] = int(update.message.text)
        context.user_data['etapa'] = 'dificuldade'
        await enviar_opcoes_dificuldade(update)

    elif etapa == 'dificuldade':
        context.user_data['dificuldade'] = update.message.text
        context.user_data['etapa'] = 'confirmar'
        await confirmar_quiz(update, context)

# Funções auxiliares para enviar botões
async def enviar_opcoes_perguntas(update):
    keyboard = [
        [InlineKeyboardButton("15", callback_data='qtd_15')],
        [InlineKeyboardButton("20", callback_data='qtd_20')],
        [InlineKeyboardButton("25", callback_data='qtd_25')],
        [InlineKeyboardButton("30", callback_data='qtd_30')]
    ]
    await update.message.reply_text("📊 Quantas perguntas?", reply_markup=InlineKeyboardMarkup(keyboard))

# (Repita para alternativas, tempo, dificuldade...)

async def confirmar_quiz(update, context):
    dados = context.user_data
    resumo = (
        f"✅ Tema: {dados['tema']}\n"
        f"📊 Perguntas: {dados['qtd']}\n"
        f"🔢 Alternativas: {dados['opcoes']}\n"
        f"⏱️ Tempo: {dados['tempo']}s\n"
        f"🎯 Dificuldade: {dados['dificuldade']}"
    )
    keyboard = [[InlineKeyboardButton("✅ Gerar Quiz", callback_data='confirmar_quiz')]]
    await update.message.reply_text(resumo, reply_markup=InlineKeyboardMarkup(keyboard))
