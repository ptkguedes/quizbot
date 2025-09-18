# core/quiz_engine.py

import random

async def gerar_quiz(tema, qtd, alternativas, dificuldade):
    perguntas = []

    for i in range(qtd):
        enunciado = f"Pergunta {i+1}: Sobre {tema}, nível {dificuldade}. Qual das opções está correta?"

        opcoes = []
        for j in range(alternativas):
            letra = chr(65 + j)  # A, B, C...
            texto = f"{letra}) Alternativa {j+1} sobre {tema}"
            opcoes.append(texto)

        correta = random.choice(opcoes)

        pergunta = {
            "enunciado": enunciado,
            "alternativas": opcoes,
            "correta": correta
        }

        perguntas.append(pergunta)

    return perguntas
