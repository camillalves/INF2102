# Instalação e Execução

## Requisitos Prévios:

Python 3.6 ou superior instalado.

Bibliotecas necessárias instaladas.

## Passos:
1. Faça o download ou clone o repositório para o seu ambiente local.
2. Instale as dependências:
```python
pip install -r requirements.txt
```
3. Acesse o diretório principal do projeto.
4. Execute o script da interface da aplicação:
```python
python anomaly_detection_ui.py
```
# Manual

## Carregar uma série temporal
1. Clique no botão "Carregar série temporal".
2. Selecione um arquivo CSV que contenha a série temporal de interesse (o arquivo deve ter uma única coluna com os valores da série temporal).

## Selecionar e configurar os métodos de detecção
3. Após carregar a série temporal, uma nova seção será exibida para seleção e configuração dos métodos.
4. Selecione os métodos desejados e ajuste os parâmetros conforme necessário. Os parâmetros padrão são:
  - **Z-Score**: threshold = 3
  - **Média Móvel**: window = 5, threshold = 2
  - **LOF**: n_neighbors = 20, threshold = 1.5
  - **Decomposição Sazonal**: model = 'additive', period = 12
  - **K-Means**: n_clusters = 2, threshold = 1.5

## Detectar anomalias
5. Após selecionar os métodos e configurar os parâmetros, clique no botão "Detectar anomalias".
6. Uma janela de comparação será exibida, mostrando os resultados dos diferentes métodos em uma tabela.

## Visualizar e exportar resultados detalhados
7. Selecione um método na lista suspensa para visualizar as anomalias detectadas.
8. Clique no botão "Plotar Anomalias" para visualizar o gráfico da série temporal com as anomalias destacadas.
9. As anomalias detectadas serão exibidas em uma nova janela, juntamente com uma tabela listando os índices e valores das anomalias.

# Contato
E-mail: ccarvalho@inf.puc-rio.br
