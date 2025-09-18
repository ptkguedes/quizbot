import asyncio

async def enviar_quiz(context, chat_id, quiz):
    tempo = int(context.user_data.get("tempo", 30))  # Tempo por pergunta

    for pergunta in quiz:
        enunciado = pergunta["enunciado"]
        alternativas = pergunta["alternativas"]
        correta = pergunta["correta"]

        if correta not in alternativas:
            correta = alternativas[0]  # fallback seguro

        await context.bot.send_poll(
            chat_id=chat_id,
            question=enunciado,
            options=alternativas,
            type="quiz",
            correct_option_id=alternativas.index(correta),
            is_anonymous=False
        )

        await asyncio.sleep(tempo)

    await context.bot.send_message(chat_id=chat_id, text="✅ Quiz finalizado! Obrigado por jogar.")
