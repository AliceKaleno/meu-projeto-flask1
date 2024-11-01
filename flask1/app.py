import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "animaldatabase.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class Animal(db.Model):
    titulo = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Título: {}>".format(self.titulo)








@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            animal = Animal(titulo=request.form.get("title"))
            db.session.add(animal)
            db.session.commit()
        except Exception as e:
            print("Falha ao adicionar o animal")

    animais = Animal.query.all()
    return render_template("index.html", animais=animais)








@app.route("/update", methods=["GET", "POST"])
def update():
    animais = Animal.query.all()
    if request.method == "POST":
        try:
            titulo_antigo = request.form.get("oldtitle")
            novo_titulo = request.form.get("newtitle")
            animal = Animal.query.filter_by(titulo=titulo_antigo).first()
            if animal:
                animal.titulo = novo_titulo
                db.session.commit()
                mensagem = "O título do animal foi atualizado com sucesso!"
            else:
                mensagem = "Animal não encontrado."
        except Exception as e:
            print("Erro ao atualizar o título do animal:", e)
            mensagem = "Erro ao atualizar o animal."
        return render_template("update.html", animais=animais, mensagem=mensagem)

    return render_template("update.html", animais=animais)










@app.route("/delete", methods=["GET", "POST"])
def delete():
    animais = Animal.query.all()
    if request.method == "POST":
        titulo = request.form.get("title")
        animal = Animal.query.filter_by(titulo=titulo).first()
        
        if animal:
            db.session.delete(animal)
            db.session.commit()
            mensagem = "O animal foi deletado com sucesso!"
        else:
            mensagem = "Animal não encontrado."
        
        return render_template("delete.html", animais=animais, mensagem=mensagem)

    return render_template("delete.html", animais=animais)

if __name__ == "__main__":
    app.run(debug=True)
