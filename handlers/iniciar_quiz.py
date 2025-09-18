# core/enviar_quiz.py

import asyncio

async def enviar_quiz(context, chat_id, quiz):
    tempo = context.user_data.get("tempo", 30)  # Tempo por pergunta

    for pergunta in quiz:
        enunciado = pergunta["enunciado"]
        alternativas = pergunta["alternativas"]
        correta = pergunta["correta"]

        # Envia a enquete como tipo "quiz"
        await context.bot.send_poll(
            chat_id=chat_id,
            question=enunciado,
            options=alternativas,
            type="quiz",
            correct_option_id=alternativas.index(correta),
            is_anonymous=False
        )

        await asyncio.sleep(tempo)  # Aguarda o tempo definido antes da próxima pergunta

    await context.bot.send_message(chat_id=chat_id, text="✅ Quiz finalizado! Obrigado por jogar.")
