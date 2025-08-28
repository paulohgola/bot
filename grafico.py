import matplotlib.pyplot as plt

def gerar_grafico(despesas):
    if not despesas:
        return None
    categorias = {}
    for d in despesas:
        categorias[d['categoria']] = categorias.get(d['categoria'], 0) + d['valor']
    labels = list(categorias.keys())
    valores = list(categorias.values())

    plt.figure(figsize=(6,6))
    plt.pie(valores, labels=labels, autopct='%1.1f%%')
    plt.title('Distribuição das Despesas por Categoria')
    caminho_arquivo = 'grafico_despesas.png'
    plt.savefig(caminho_arquivo)
    plt.close()
    return caminho_arquivo
