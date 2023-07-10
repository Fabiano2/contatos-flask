from flask import Flask, render_template, request, redirect, url_for, flash, redirect, url_for, flash
import urllib.request, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contatos.sqlite3'
db = SQLAlchemy(app)
app.secret_key = 'teste@123'

class contatos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    telefone = db.Column(db.Integer)

    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone
        
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/lista')
def lista():
    return render_template('lista.html', contatos=contatos.query.all())

@app.route('/adiciona_contato', methods=["GET", "POST"])
def adiciona_contato():
    nome = request.form.get("nome")
    telefone = request.form.get("telefone")

    if request.method == "POST":
        contato = contatos(nome, telefone)
        if not nome or not telefone:
            flash("Preencha todos os campos", "error")
        else:
            db.session.add(contato)
            db.session.commit()
            return redirect(url_for('lista'))
    return render_template('adiciona_contato.html')

@app.route('/<int:id>/atualiza_lista', methods=["GET","POST"])
def atualiza_lista(id):
    contato = contatos.query.filter_by(id=id).first()

    if request.method == 'POST':
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        if not nome or not telefone:
            flash("Preencha todos os campos", "error")
        else:
            contatos.query.filter_by(id=id).update({"nome":nome, "telefone":telefone})
            db.session.commit()
            return redirect(url_for('lista'))

    return render_template("atualiza_lista.html", contato=contato)

@app.route('/<int:id>/exclui_contato', methods=["GET"])
def exclui_contato(id):
    contato = contatos.query.filter_by(id=id).first()   
    db.session.delete(contato)
    db.session.commit()
    return redirect(url_for('lista'))

if __name__ == "__main__":
    app.run(debug=True)
