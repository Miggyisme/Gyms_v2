import os
from datetime import datetime
import re

arquivos_treino = ["TreinoA.txt", "TreinoB.txt", "TreinoC.txt", "TreinoD.txt"]

grupamentos = {
    "Dorsais": ["puxada", "remada", "pulldown", "serrote"],
    "Peitoral": ["supino", "crucifixo", "crossover"],
    "Ombros": ["elevação", "desenvolvimento", "arnold"],
    "Bíceps": ["bíceps","rosca","martelo",],
    "Tríceps": ["tríceps","francês"],
    "Pernas": ["agachamento", "leg", "cadeira", "mesa", "extensora", "flexora", "panturrilha"],
}


# Inicializa dicionário com os totais
totais = {grupo.capitalize(): 0 for grupo in grupamentos}

def identifica_grupo(nome_exercicio):
    nome = nome_exercicio.lower()
    for grupo, palavras in grupamentos.items():
        if any(palavra in nome for palavra in palavras):
            return grupo.capitalize()
    return "Outros"

def parse_carga(valor):
    # Trata valores como "30+30", "100kg cada lado", "—", "59–65kg"
    if "—" in valor or valor.strip() == "":
        return 0
    numeros = re.findall(r"[\d.]+", valor.replace(",", "."))
    if not numeros:
        return 0
    numeros = list(map(float, numeros))
    return sum(numeros) / len(numeros)

# Processa todos os arquivos
for nome_arquivo in arquivos_treino:
    if not os.path.exists(nome_arquivo):
        print(f"Arquivo {nome_arquivo} não encontrado.")
        continue

    with open(nome_arquivo, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    for i in range(2, len(linhas), 4):
        nome_exercicio = linhas[i].strip()
        if not nome_exercicio:
            continue
        grupo = identifica_grupo(nome_exercicio)

        try:
            linha_dados = linhas[i + 1].strip()
            partes = re.findall(r"[\d\.\+]+", linha_dados)

            if len(partes) >= 3:
                series = int(float(partes[0]))
                repeticoes = int(float(partes[1]))
                carga = parse_carga(partes[2])
                total = series * repeticoes * carga
                totais[grupo] += total
        except Exception as e:
            print(f"Erro no exercício '{nome_exercicio}': {e}")

# Gera arquivo de saída
mes_ano = datetime.now().strftime("%m-%Y")
nome_saida = f"Resumo-{mes_ano}.txt"

with open(nome_saida, "w", encoding="utf-8") as f:
    f.write(f"{mes_ano}\n\n")
    for grupo, valor in totais.items():
        f.write(f"{grupo}: {int(valor)}\n")

print(f"{nome_saida}")