
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)


def ligar_banco():
    banco = psycopg2.connect(
        host="localhost",
        dbname="eventos",
        user="postgres",
        password="senai",
        port="5432"
    )
    return banco

@app.route("/")
def inicial():
    return render_template("index.html")
@app.route("/patrocinador")
def patrocinador():
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute("""SELECT id_patrocinador, nome_empresa, contato,
                      valor_patrocinio FROM patrocinador
                      ORDER BY id_patrocinador""")

    lista = cursor.fetchall()

    banco.close()

    return render_template("patrocinador.html", patrocinadores=lista)


@app.route("/patrocinador/enviar", methods=["POST"])
def enviar_patrocinador():
    nome_empresa = request.form["nome_empresa"]
    contato = request.form["contato"]
    valor_patrocinio = request.form["valor_patrocinio"]

    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute("""INSERT INTO patrocinador
                      (nome_empresa, contato, valor_patrocinio)
                      VALUES (%s, %s, %s)""",
                   (nome_empresa, contato, valor_patrocinio))

    banco.commit()
    banco.close()

    return redirect("/patrocinador")


@app.route("/patrocinador/editar/<int:id>")
def editar_patrocinador(id):
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute("""SELECT id_patrocinador, nome_empresa, contato,
                      valor_patrocinio FROM patrocinador
                      WHERE id_patrocinador = %s""", (id,))

    patrocinador = cursor.fetchone()

    banco.close()

    return render_template("editar_patrocinador.html",
                           patrocinador=patrocinador)


@app.route("/patrocinador/atualizar/<int:id>", methods=["POST"])
def atualizar_patrocinador(id):
    nome_empresa = request.form["nome_empresa"]
    contato = request.form["contato"]
    valor_patrocinio = request.form["valor_patrocinio"]

    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute("""UPDATE patrocinador
                      SET nome_empresa = %s, contato = %s,
                      valor_patrocinio = %s
                      WHERE id_patrocinador = %s""",
                   (nome_empresa, contato, valor_patrocinio, id))

    banco.commit()
    banco.close()

    return redirect("/patrocinador")


@app.route("/patrocinador/excluir/<int:id>", methods=["POST"])
def excluir_patrocinador(id):
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute("""DELETE FROM patrocinador
                      WHERE id_patrocinador = %s""", (id,))

    banco.commit()
    banco.close()

    return redirect("/patrocinador")


@app.route("/palestrantes")
def palestrantes():
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute("""SELECT id_palestrante, nome, assunto,
                      quantidade_minuto, cache
                      FROM palestrante
                      ORDER BY id_palestrante""")

    lista = cursor.fetchall()

    banco.close()

    return render_template("palestrante.html", palestrantes=lista)


@app.route("/palestrantes/enviar", methods=["POST"])
def enviar_palestrante():
    nome = request.form.get("nome")
    assunto = request.form.get("assunto")
    quantidade_minuto = request.form.get("quantidade_minuto")
    cache = request.form.get("cache")

    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute("""INSERT INTO palestrante
                      (nome, assunto, quantidade_minuto, cache)
                      VALUES (%s, %s, %s, %s)""",
                   (nome, assunto, quantidade_minuto, cache))

    banco.commit()
    banco.close()

    return redirect("/palestrantes")


@app.route("/palestrantes/editar/<int:id_palestrante>")
def editar_palestrante(id_palestrante):
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute("""SELECT id_palestrante, nome, assunto,
                      quantidade_minuto, cache
                      FROM palestrante
                      WHERE id_palestrante = %s""",
                   (id_palestrante,))

    palestrante = cursor.fetchone()

    banco.close()

    if palestrante is None:
        return redirect("/palestrantes")

    return render_template("editar_palestrante.html",
                           palestrante=palestrante)


@app.route("/palestrantes/atualizar/<int:id_palestrante>",
           methods=["POST"])
def atualizar_palestrante(id_palestrante):
    nome = request.form.get("nome")
    assunto = request.form.get("assunto")
    quantidade_minuto = request.form.get("quantidade_minuto")
    cache = request.form.get("cache")

    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute("""UPDATE palestrante
                      SET nome = %s, assunto = %s,
                      quantidade_minuto = %s, cache = %s
                      WHERE id_palestrante = %s""",
                   (nome, assunto, quantidade_minuto, cache,
                    id_palestrante))

    banco.commit()
    banco.close()

    return redirect("/palestrantes")


@app.route("/palestrantes/excluir/<int:id_palestrante>",
           methods=["POST"])
def excluir_palestrante(id_palestrante):
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute("""DELETE FROM palestrante
                      WHERE id_palestrante = %s""",
                   (id_palestrante,))

    banco.commit()
    banco.close()

    return redirect("/palestrantes")



@app.route("/eventos")
def eventos():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id_evento, nome, local, quantidade_vaga, data_evento FROM evento ORDER BY id_evento")
    lista = cursor.fetchall()
    banco.close()
    return render_template("evento.html", eventos=lista)

@app.route("/eventos/cadastrar", methods=["POST"])
def criar_evento():
    nome = request.form["nome"]
    local = request.form["local"]
    quantidade_vaga = request.form["quantidade_vaga"]
    data_evento = request.form["data_evento"]

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""INSERT INTO evento (nome, local, quantidade_vaga, data_evento)
                      VALUES (%s, %s, %s, %s)""",
                   (nome, local, quantidade_vaga, data_evento))
    banco.commit()
    banco.close()
    return redirect("/eventos")

@app.route("/eventos/editar/<int:id_evento>")
def editar_evento(id_evento):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id_evento, nome, local, quantidade_vaga, data_evento FROM evento WHERE id_evento = %s", (id_evento,))
    evento = cursor.fetchone()
    banco.close()

    if evento is None:
        return redirect("/eventos")
    return render_template("editar_evento.html", eventos=evento)

@app.route("/eventos/atualizar/<int:id_evento>", methods=["POST"])
def atualizar_evento(id_evento):
    nome = request.form.get("nome")
    local = request.form.get("local")
    quantidade_vaga = request.form.get("quantidade_vaga")
    data_evento = request.form.get("data_evento")

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""UPDATE evento SET nome = %s, local = %s,quantidade_vaga = %s, data_evento = %s
                      WHERE id_evento = %s""",
                   (nome, local, quantidade_vaga, data_evento, id_evento))
    banco.commit()
    banco.close()
    return redirect("/eventos")

@app.route("/eventos/excluir/<int:id_evento>", methods=["POST"])
def excluir_evento(id_evento):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("DELETE FROM evento WHERE id_evento = %s", (id_evento,))
    banco.commit()
    banco.close()
    return redirect("/eventos")

if __name__ == '__main__':
    app.run()
