import pandas as pd
from flask import Flask,redirect,render_template,request
import os

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
def analise (nome_arquivo):
    caminho = os.path.join(UPLOADS,nome_arquivo)
    df = pd.read_csv(caminho)
    colunas = df.columns.str.lower()
    
    


if __name__ == '__main__':
    app.run(debug=True)