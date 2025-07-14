from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils import carregar_dados, salvar_dados

app = Flask(__name__)
app.secret_key = 'minha_chave_secreta'

# Caminho do arquivo JSON com as tarefas
CAMINHO_TAREFAS = 'todo.json'
tarefas = carregar_dados(CAMINHO_TAREFAS)

# ---------------------------
# ROTAS PRINCIPAIS
# ---------------------------

@app.route('/')
def index():
    return render_template(
        'index.html',
        titulo="Meu Site",
        mensagem="Seja bem-vindo!",
        nome_usuario=None
    )

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/formulario')
def formulario():
    return render_template('formulario.html')

@app.route('/contador', methods=['GET', 'POST'])
def contador():
    if 'cliques' not in session:
        session['cliques'] = 0

    if request.method == 'POST':
        if request.form.get('acao') == 'incrementar':
            session['cliques'] += 1
        elif request.form.get('acao') == 'zerar':
            session['cliques'] = 0

    return render_template('contador.html')

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if request.method == 'POST':
        nova_tarefa = request.form.get('tarefa')
        if nova_tarefa:
            tarefas.append(nova_tarefa)
            salvar_dados(CAMINHO_TAREFAS, tarefas)
            flash('Tarefa adicionada com sucesso!', 'success')
        return redirect(url_for('todo'))
    return render_template('todo.html', tarefas=tarefas)

@app.route('/saudacao/<nome>')
def saudacao(nome):
    return render_template('saudacao.html', nome=nome)

@app.route('/calcula', methods=['GET', 'POST'])
def calcula():
    resultado = None
    expressao = ""
    historico = []

    if request.method == 'POST':
        expressao = request.form.get('expressao', '')
        try:
            resultado = eval(expressao, {"__builtins__": None}, {})
        except ZeroDivisionError:
            resultado = "Erro: divisão por zero"
        except:
            resultado = "Erro de expressão inválida"

    return render_template('calcula.html', resultado=resultado, expressao=expressao, historico=historico)

# ---------------------------
# EXECUÇÃO
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5003)
