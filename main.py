#Código produzido pelo Aluno Felipe Nascimento
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('cadastro.html')

@app.route('/submit', methods=['POST'])
def submit():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    if not nome or not email or not senha:
        return "Todos os campos são obrigatórios!"
    
    print(f"Usuário cadastrado com sucesso! Nome: {nome}, Email: {email}, Senha: {senha}")
    return render_template('cadastro.html', nome=nome, email=email, senha=senha)

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True) 