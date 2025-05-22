import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from PIL import ImageGrab

exercicios_iniciais = [
    "Supino reto com barra",
    "Supino inclinado barra",
    "Crucifixo na máquina",
    "Crossover na polia baixa",
    "Desenvolvimento na máquina",
    "Elevação lateral com halteres",
    "Elevação frontal na polia",
    "Tríceps na polia com corda",
    "Tríceps francês com halteres",
    "Tríceps máquina"
]

entradas = []

rep_values = [
    "4 a 6 repetições",
    "6 a 8 repetições",
    "8 a 10 repetições",
    "10 a 12 repetições",
    "12 a 15 repetições",
    "15 a 20 repetições"
]

mapa_reps_para_num = {
    "4 a 6 repetições": "5",
    "6 a 8 repetições": "7",
    "8 a 10 repetições": "9",
    "10 a 12 repetições": "11",
    "12 a 15 repetições": "13",
    "15 a 20 repetições": "17"
}

mapa_num_para_reps = {v: k for k, v in mapa_reps_para_num.items()}

def salvar_dados():
    caminho = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Arquivos de texto", "*.txt")],
        title="Salvar treino como"
    )
    if not caminho:
        return
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write("Série/Repetição Média/Carga\n\n")
            for e in entradas:
                nome = e['nome'].get()
                series = e['series'].get()
                reps_str = e['reps'].get()
                carga = e['carga'].get()
                obs = e['obs'].get()
                reps = mapa_reps_para_num.get(reps_str, reps_str)
                f.write(f"{nome}\n{series}/{reps}/{carga}\nObs: {obs}\n\n")
        messagebox.showinfo("Salvo", f"Dados salvos em:\n{caminho}")
    except Exception as err:
        messagebox.showerror("Erro", f"Não foi possível salvar:\n{err}")

def carregar_dados():
    caminho = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Arquivos de texto", "*.txt")],
        title="Abrir treino"
    )
    if not caminho:
        return
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            linhas = f.read().strip().splitlines()

        blocos = []
        atual = []
        for linha in linhas[2:]:  # começa a ler a partir da 3ª linha
            if linha.strip() == "":
                if atual:
                    blocos.append(atual)
                    atual = []
            else:
                atual.append(linha)
        if atual:
            blocos.append(atual)

        for i, bloco in enumerate(blocos):
            if i >= len(entradas) or len(bloco) < 3:
                continue
            nome, info, obs = bloco[0], bloco[1], bloco[2]
            series, reps_num, carga = info.split("/")
            series = series.strip()
            reps_num = reps_num.strip()
            carga = carga.strip()

            entradas[i]['nome'].delete(0, tk.END)
            entradas[i]['nome'].insert(0, nome)
            entradas[i]['series'].set(series)
            entradas[i]['reps'].set(mapa_num_para_reps.get(reps_num, reps_num))
            entradas[i]['carga'].delete(0, tk.END)
            entradas[i]['carga'].insert(0, carga)
            entradas[i]['obs'].delete(0, tk.END)
            entradas[i]['obs'].insert(0, obs.replace("Obs:", "").strip())
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível carregar:\n{e}")

def gerar_imagem():
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    w = x + root.winfo_width()
    h = y + root.winfo_height()
    img = ImageGrab.grab(bbox=(x, y, w, h))

    caminho_img = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("Arquivo PNG", "*.png")],
        title="Salvar imagem como"
    )
    if not caminho_img:
        return

    try:
        img.save(caminho_img)
        messagebox.showinfo("Imagem salva", f"Imagem salva em:\n{caminho_img}")
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível salvar a imagem:\n{e}")

def reorganizar_blocos(event=None):
    largura_total = blocos_frame.winfo_width()
    largura_bloco = 280
    colunas = max(largura_total // largura_bloco, 1)

    for idx, widget in enumerate(blocos_widgets):
        linha = idx // colunas
        coluna = idx % colunas
        widget.grid(row=linha, column=coluna, padx=10, pady=10, sticky="n")

root = tk.Tk()
root.title("Treino")
root.geometry("900x700")

canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

scrollable_frame = tk.Frame(canvas)
canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
scrollable_frame.bind("<Configure>", on_frame_configure)

def on_canvas_configure(event):
    canvas.itemconfig(canvas_window, width=event.width)
canvas.bind("<Configure>", on_canvas_configure)

blocos_frame = tk.Frame(scrollable_frame)
blocos_frame.grid(row=0, column=0, sticky="nsew")

scrollable_frame.grid_rowconfigure(0, weight=1)
scrollable_frame.grid_columnconfigure(0, weight=1)

blocos_widgets = []

for nome_inicial in exercicios_iniciais:
    frame = tk.Frame(blocos_frame, bd=2, relief="groove", padx=10, pady=5, width=260)
    frame.grid_propagate(False)

    nome_entry = tk.Entry(frame, font=("Arial", 10, "bold"), width=35)
    nome_entry.delete(0, tk.END)
    nome_entry.pack(pady=(0, 5))

    labels_linha = tk.Frame(frame)
    labels_linha.pack(pady=(5, 0))

    tk.Label(labels_linha, text="Séries", font=("Arial", 8)).pack(side="left", padx=15)
    tk.Label(labels_linha, text="Repetições", font=("Arial", 8)).pack(side="left", padx=15)
    tk.Label(labels_linha, text="Carga", font=("Arial", 8)).pack(side="left", padx=15)

    controles_linha = tk.Frame(frame)
    controles_linha.pack(pady=(0, 5))

    series_var = tk.StringVar(value="")
    reps_var = tk.StringVar(value="")
    carga_var = tk.Entry(controles_linha, width=8)
    carga_var.delete(0, tk.END)
    carga_var.insert(0, "")

    ttk.Combobox(controles_linha, textvariable=series_var, values=[str(i) for i in range(1, 11)], width=4).pack(side="left", padx=10)
    ttk.Combobox(controles_linha, textvariable=reps_var, values=rep_values, width=15).pack(side="left", padx=10)
    carga_var.pack(side="left", padx=10)

    obs_entry = tk.Entry(frame, width=40)
    obs_entry.delete(0, tk.END)
    obs_entry.insert(0, "")
    obs_entry.pack(pady=(5, 0))

    entradas.append({
        'nome': nome_entry,
        'series': series_var,
        'reps': reps_var,
        'carga': carga_var,
        'obs': obs_entry
    })

    blocos_widgets.append(frame)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Carregar", command=carregar_dados, bg="orange").pack(side="left", padx=5)
tk.Button(btn_frame, text="Salvar", command=salvar_dados, bg="lightgreen", font=("Arial", 11)).pack(side="left", padx=5)
tk.Button(btn_frame, text="Gerar Imagem", command=gerar_imagem, bg="lightblue", font=("Arial", 11)).pack(side="left", padx=5)

blocos_frame.bind("<Configure>", reorganizar_blocos)
root.bind("<Configure>", reorganizar_blocos)

root.mainloop()
