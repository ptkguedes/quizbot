import random

# 🎯 Gera uma lista de perguntas simuladas para o quiz
async def gerar_quiz(tema: str, qtd: int, alternativas: int, dificuldade: str) -> list:
    perguntas = []

    for i in range(qtd):
        enunciado = (
            f"Pergunta {i+1}: Sobre {tema}, nível {dificuldade}. "
            "Qual das opções está correta?"
        )

        opcoes = []
        for j in range(alternativas):
            letra = chr(65 + j)  # A, B, C...
            texto = f"{letra}) Alternativa {j+1} sobre {tema}"
            opcoes.append(texto)

        correta = random.choice(opcoes) if opcoes else None

        pergunta = {
            "enunciado": enunciado,
            "alternativas": opcoes,
            "correta": correta
        }

        perguntas.append(pergunta)

    return perguntas
