import random

from flask import Flask, redirect, render_template, request

app = Flask(__name__)

cartas = {
    "serjao" : {
                    "nome" : "Serjão Berranteiro",
                    "img" : "serjao berranteiro.jpeg",
                    "raridade" : "lendaria",
                    "viralidade" : 95,
                    "zoeira" : 85,
                    "nostalgia" : 60
                },
    "alegria" : {
                    "nome" : "Para nossa alegria",
                    "img" : "para nossa alegria.png",
                    "raridade" : "comum",
                    "viralidade" : 80,
                    "zoeira" : 70,
                    "nostalgia" : 90
                },
    
        
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/regras")
def regras():
    return render_template("regras.html")


# Pacotinho: sorteia uma carta e vai direto para o duelo
@app.route("/pacotinho")
def pacotinho():
    carta = random.choice(list(cartas))
    return redirect("/duelo/" + carta)


# Duelo, passo 1: escolher o atributo
@app.route("/duelo/<carta>")
def escolher_atributo(carta):
    if carta not in cartas:          # apelido errado? volta para a coleção
        return redirect("/")
    return render_template("atributo.html", carta=carta, minha=cartas[carta])


# Duelo, passo 2: comparar com uma carta sorteada
@app.route("/duelo/<carta>/<atributo>")
def resultado(carta, atributo):
    if carta not in cartas:
        return redirect("/")
    minha = cartas[carta]
    if atributo not in minha:        # atributo errado? volta para a escolha
        return redirect("/duelo/" + carta)

    outras = [c for c in cartas if c != carta]
    if len(outras) == 0:             # só tem uma carta? duela com ela mesma
        outras = [carta]
    adversaria = cartas[random.choice(outras)]

    if minha[atributo] > adversaria[atributo]:
        resultado = "Você venceu!"
    elif minha[atributo] < adversaria[atributo]:
        resultado = "Você perdeu!"
    else:
        resultado = "Empate!"

    poder_total = minha["viralidade"] + minha["zoeira"] + minha["nostalgia"]

    return render_template("resultado.html",
                           atributo=atributo,
                           minha=minha,
                           adversaria=adversaria,
                           resultado=resultado,
                           poder_total=poder_total)


# Rota para criar carta
@app.route("/criar")
def criar():
    return render_template("criar.html")

@app.route("/carta_criada", methods=["POST"])
def carta_criada():
    nome = request.form["nome"]
    imagem = request.form["imagem"]
    raridade = request.form["raridade"]
    viralidade = int(request.form["viralidade"])
    zoeira = int(request.form["zoeira"])
    nostalgia = int(request.form["nostalgia"])

    # A carta nova também entra no duelo (até o servidor reiniciar!)
    chave = nome.lower().replace(" ", "-")
    cartas[chave] = {"nome": nome, "img": imagem, "raridade": raridade,
                     "viralidade": viralidade, "zoeira": zoeira, "nostalgia": nostalgia}

    poder_total = viralidade + zoeira + nostalgia
    return render_template("carta_criada.html",
                           chave=chave, nome=nome, imagem=imagem, raridade=raridade,
                           viralidade=viralidade, zoeira=zoeira, nostalgia=nostalgia,
                           poder_total=poder_total)


if __name__ == "__main__":
    app.run(debug=True)