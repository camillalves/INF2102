import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
from anomaly_detection import AnomalyDetection
import matplotlib.pyplot as plt
from pandastable import Table

# Inicializa os parâmetros padrão para cada método de detecção de anomalias
default_params = {
    "IQR": {},
    "Z-Score": {"threshold": 3},
    "Média Móvel": {"window": 5, "threshold": 2},
    "LOF": {"n_neighbors": 20, "threshold": 1.5},
    "Decomposição Sazonal": {"model": "additive", "period": 12},
    "K-Means": {"n_clusters": 2, "threshold": 1.5}
}

# Descrições dos parâmetros para exibição na interface
param_descriptions = {
    "Z-Score": "threshold: Limite de desvio padrão.",
    "Média Móvel": "window: Tamanho da janela.\nthreshold: Limite de desvio padrão.",
    "LOF": "n_neighbors: Número de vizinhos.\nthreshold: Limite de distância local.",
    "Decomposição Sazonal": "model: Tipo de modelo (additive/multiplicative).\nperiod: Período da sazonalidade.",
    "K-Means": "n_clusters: Número de clusters.\nthreshold: Limite de distância ao centro."
}

# Função para carregar o arquivo CSV com a série temporal


def load_csv():
    global time_series, time_series_data
    # Abre o diálogo para seleção de arquivo
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        # Lê o arquivo CSV e converte a coluna de valores para float
        time_series_data = pd.read_csv(file_path, header=0)
        time_series = time_series_data.iloc[:, 0].astype(float).values
        # Atualiza o botão de carregamento e habilita o botão de detectar anomalias
        load_button.config(text="Série temporal carregada",
                           bg="#4CAF50", activebackground="#45a049")
        method_selector_frame.pack(pady=10)
        detect_button.pack(pady=10)
        detect_button.config(state=tk.NORMAL, bg="#4CAF50",
                             activebackground="#45a049")

# Função para detectar anomalias usando os métodos selecionados


def detect_anomalies():
    global detector, comparison_results
    # Obtém os métodos selecionados e seus parâmetros
    selected_methods = [method for method,
                        var in methods_vars.items() if var.get()]
    params = {method: {param: entries[method][param].get(
    ) for param in entries[method]} for method in selected_methods}

    # Inicializa a detecção de anomalias com a série temporal e os parâmetros
    detector = AnomalyDetection(time_series, params)
    # Compara os métodos selecionados
    comparison_results = detector.compare_methods(selected_methods)

    # Exibe os resultados da comparação em uma nova janela
    comparison_window = tk.Toplevel(root)
    comparison_window.title("Resultados da Comparação")
    comparison_window.geometry("600x400")

    frame = tk.Frame(comparison_window)
    frame.pack(fill=tk.BOTH, expand=1)

    # Exibe a tabela de resultados da comparação
    pt = Table(frame, dataframe=comparison_results)
    pt.show()

    # Atualiza o selector de métodos para plotar anomalias
    method_selector['values'] = comparison_results['Método'].tolist()
    method_selector.current(0)
    method_selector.config(state=tk.NORMAL)
    method_selector.pack(pady=10)
    plot_button.pack(pady=10)
    plot_button.config(state=tk.NORMAL, bg="#4CAF50",
                       activebackground="#45a049")

# Função para plotar as anomalias detectadas


def plot_anomalies():
    # Obtém o método selecionado
    method = method_selector.get()
    anomalies = detector.detect_method(method)

    # Plota as anomalias na série temporal
    detector.plot_anomalies(anomalies)

    # Cria um DataFrame com os índices e valores originais das anomalias detectadas
    anomalies_df = pd.DataFrame(anomalies, columns=['Index', 'Valor'])

    # Exibe as anomalias em uma nova janela
    anomalies_window = tk.Toplevel(root)
    anomalies_window.title("Índice e Valores das Anomalias")
    anomalies_window.geometry("600x400")

    frame = tk.Frame(anomalies_window)
    frame.pack(fill=tk.BOTH, expand=1)

    pt = Table(frame, dataframe=anomalies_df)
    pt.show()

# Função para criar a interface de seleção e configuração dos métodos


def create_method_param_interface():
    for method, params in default_params.items():
        method_frame = ttk.Frame(methods_frame)
        method_frame.pack(fill=tk.X, pady=5)
        method_check = tk.Checkbutton(
            method_frame, text=method, variable=methods_vars[method], font=("Helvetica", 10))
        method_check.pack(side=tk.LEFT, padx=5)

        param_frame = ttk.Frame(methods_frame)
        param_frame.pack(fill=tk.X, padx=10, pady=5)

        # Adiciona os parâmetros dos métodos à interface
        for param, value in params.items():
            param_label = ttk.Label(
                param_frame, text=param, font=("Helvetica", 10))
            param_label.pack(side=tk.LEFT)
            param_entry = ttk.Entry(
                param_frame, width=10, font=("Helvetica", 10))
            param_entry.insert(0, str(value))
            param_entry.pack(side=tk.LEFT, padx=5)
            entries[method][param] = param_entry

        # Adiciona a descrição dos parâmetros, se houver
        if method in param_descriptions:
            param_description = ttk.Label(param_frame, text=param_descriptions[method], font=(
                "Helvetica", 8), background="white")
            param_description.pack(side=tk.LEFT, padx=5)


# Configuração da janela principal da aplicação
root = tk.Tk()
root.title("Detecção de Anomalias em Séries Temporais")
root.geometry("800x600")
root.configure(bg="white")

# Inicializa variáveis para os métodos e entradas de parâmetros
methods_vars = {method: tk.BooleanVar() for method in default_params}
entries = {method: {} for method in default_params}

# Estilo dos componentes da interface
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 10), padding=10)
style.configure("TLabel", font=("Helvetica", 12), padding=10)
style.configure("TCombobox", font=("Helvetica", 10), padding=10)

# Título da aplicação
title_label = ttk.Label(root, text="Detecção de Anomalias em Séries Temporais", font=(
    "Helvetica", 14, "bold"), background="white")
title_label.pack(pady=10)

# Descrição para carregar a série temporal
description_label = ttk.Label(root, text="Clique em 'Carregar série temporal' e selecione o arquivo CSV contendo a série temporal.", font=(
    "Helvetica", 10), background="white")
description_label.pack(pady=5)

# Botão para carregar a série temporal
load_button = tk.Button(root, text="Carregar série temporal", command=load_csv, font=(
    "Helvetica", 10), bg="#4CAF50", fg="white", activebackground="#45a049", activeforeground="white")
load_button.pack(pady=10)

# Frame para seleção e configuração dos métodos
method_selector_frame = ttk.Frame(root)
method_selector_frame.pack_forget()

# Texto de instrução para seleção dos métodos e configuração dos parâmetros
methods_label = ttk.Label(method_selector_frame, text="Selecione os métodos estatísticos/comútacionais de interesse, configure os parâmetros e clique em 'Detectar anomalias':", font=(
    "Helvetica", 10), background="white")
methods_label.pack(pady=5)

# Canvas e scrollbar para a área de seleção dos métodos
scroll_canvas = tk.Canvas(method_selector_frame)
scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

scrollbar = ttk.Scrollbar(method_selector_frame,
                          orient="vertical", command=scroll_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")

scroll_canvas.configure(yscrollcommand=scrollbar.set)
scroll_canvas.bind('<Configure>', lambda e: scroll_canvas.configure(
    scrollregion=scroll_canvas.bbox("all")))

methods_frame = ttk.Frame(scroll_canvas)
scroll_canvas.create_window((0, 0), window=methods_frame, anchor="nw")

# Cria a interface de seleção e configuração dos métodos
create_method_param_interface()

# Botão para detectar anomalias (inicialmente desabilitado)
detect_button = tk.Button(root, text="Detectar anomalias", command=detect_anomalies, state=tk.DISABLED, font=(
    "Helvetica", 10), bg="#d3d3d3", fg="white", activebackground="#d3d3d3", activeforeground="white")
detect_button.pack_forget()

# Combobox para seleção do método de plotagem (inicialmente desabilitado)
method_selector = ttk.Combobox(root, state=tk.DISABLED)
method_selector.pack_forget()

# Botão para plotar anomalias (inicialmente desabilitado)
plot_button = tk.Button(root, text="Plotar Anomalias", command=plot_anomalies, state=tk.DISABLED, font=(
    "Helvetica", 10), bg="#4CAF50", fg="white", activebackground="#45a049", activeforeground="white")
plot_button.pack_forget()

# Inicia o loop principal da interface
root.mainloop()
