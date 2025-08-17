import pandas as pd
from flask import Flask,redirect,render_template,request
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)
UPLOADS = 'uploads'
app.config['UPLOADS']=UPLOADS
os.makedirs(UPLOADS,exist_ok=True)

@app.route('/',methods=['POST','GET'])
def home():
    if request.method == 'POST':
        arquivo = request.files['arquivo']
        if arquivo:
            caminho = os.path.join(UPLOADS,arquivo.filename)
            arquivo.save(caminho)
            return redirect(f'/analise/{arquivo.filename}')
    return render_template('home.html')

@app.route('/analise/<nome_arquivo>')
def analise(nome_arquivo):
    caminho = os.path.join(UPLOADS, nome_arquivo)
    df = pd.read_csv(caminho)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Normalizar nomes das colunas
    df.columns = df.columns.str.strip().str.lower()

    # Variáveis de análise
    rent_acumulada = None
    volume_medio = None

    # Garantir que as colunas existem
    if 'open' in df.columns and 'close' in df.columns and 'date' in df.columns:
        # Rentabilidade acumulada no período
        rent_acumulada = (df['close'].iloc[-1] / df['open'].iloc[0] - 1) * 100

        # Rentabilidade diária (%)
        df['rent_diaria'] = df['close'].pct_change() * 100

    # Volume médio
    if 'volume' in df.columns:
        volume_medio = df['volume'].mean()

    os.makedirs(os.path.join('static', 'graficos'), exist_ok=True)
    # -------------------------------
    # Gráfico 1 - Evolução do preço
    grafico_preco = os.path.join('static', 'graficos', 'preco_fechamento.png')
    df.plot(x='date', y='close', kind='line', figsize=(8, 5), color='blue')
    plt.title('Evolução do preço de fechamento')
    plt.xlabel('Data')
    plt.ylabel('Preço (R$)')
    plt.tight_layout()
    plt.savefig(grafico_preco)
    plt.clf()

    # Gráfico 2 - Rentabilidade diária
    grafico_rent = os.path.join('static', 'graficos', 'rentabilidade_diaria.png')
    if 'rent_diaria' in df.columns:
        df.plot(x='date', y='rent_diaria', kind='line', figsize=(8, 5), color='green')
        plt.title('Rentabilidade diária (%)')
        plt.xlabel('Data')
        plt.ylabel('Rentabilidade (%)')
        plt.tight_layout()
        plt.savefig(grafico_rent)
        plt.clf()

    # Gráfico 3 - Volume
    grafico_vol = os.path.join('static', 'graficos', 'volume.png')
    if 'volume' in df.columns:
        df.plot(x='date', y='volume', kind='bar', figsize=(10, 5), color='orange')
        plt.title('Volume negociado')
        plt.xlabel('Data')
        plt.ylabel('Volume')
        plt.tight_layout()
        plt.savefig(grafico_vol)
        plt.clf()

    # -------------------------------
    # Tabela completa
    tabela = df.to_html(classes='table table-bordered table-custom', index=False)

    return render_template(
        'analise.html',
        tabela=tabela,
        rent_acumulada=rent_acumulada,
        volume_medio=volume_medio,
        grafico_preco='graficos/preco_fechamento.png',
        grafico_rent='graficos/rentabilidade_diaria.png',
        grafico_vol='graficos/volume.png'
    )
 


    


if __name__ == '__main__':
    app.run(debug=True)