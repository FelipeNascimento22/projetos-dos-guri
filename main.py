from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "chave_secreta_buytaku_super_segura"

class Produto:
    def __init__(self, nome: str, preco: float, tipo: str):
        self.nome = nome
        self.preco = preco
        self.tipo = tipo

class Camiseta(Produto):
    def __init__(self, nome: str, preco: float, cor: str):
        super().__init__(nome, preco, "Camisetas")
        self.cor = cor

class ActionFigure(Produto):
    def __init__(self, nome: str, preco: float, tamanho: str, personagem: str):
        super().__init__(nome, preco, "Action Figures")
        self.tamanho = tamanho
        self.personagem = personagem

class Roupa(Produto):
    def __init__(self, nome: str, preco: float, tamanho: str):
        super().__init__(nome, preco, "Roupas")
        self.tamanho = tamanho


MEUS_PRODUTOS = [
    Camiseta("Hatsune Miku T-Shirt", 50.00, "Branca, Preta"),
    Camiseta("Camiseta Jujutsu Kaisen - Gojo", 60.00, "Preta, Roxa"),
    Camiseta("Camiseta One Piece - Luffy", 55.00, "Vermelha, Branca"),
    Camiseta("Camiseta Attack on Titan", 65.00, "Verde, Preta"),
    ActionFigure("Action Figure Naruto", 120.00, "15cm", "Naruto Uzumaki"),
    ActionFigure("Action Figure Roronoa Zoro", 180.00, "20cm", "Zoro (Wano)"),
    ActionFigure("Action Figure Nezuko Kamado", 140.00, "12cm", "Nezuko"),
    ActionFigure("Action Figure Goku SSJ", 200.00, "18cm", "Goku"),
    ActionFigure("Action Figure Levi Ackerman", 160.00, "16cm", "Levi"),
    Roupa("Moletom Akatsuki", 150.00, "M, G, GG"),
    Roupa("Jaqueta Tokyo Revengers", 170.00, "P, M, G"),
    Roupa("Moletom Cyberpunk Edgerunners", 190.00, "M, G")
]

CATALOGO_DICT = {}
for prod in MEUS_PRODUTOS:
    if prod.tipo not in CATALOGO_DICT:
        CATALOGO_DICT[prod.tipo] = {}
    CATALOGO_DICT[prod.tipo][prod.nome] = prod.preco


def obter_carrinho():
    """Retorna o carrinho da sessão formatado com itens e subtotais."""
    carrinho_raw = session.get("carrinho", {})
    itens = []
    total = 0.0

    for item_nome, item_data in carrinho_raw.items():
        subtotal = item_data["preco"] * item_data["quantidade"]
        total += subtotal
        itens.append({
            "nome": item_nome,
            "preco": item_data["preco"],
            "quantidade": item_data["quantidade"],
            "subtotal": subtotal
        })

    return {"itens": itens}, total



@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nome = request.form.get("nome", "")
        email = request.form.get("email", "")
        senha = request.form.get("senha", "")
        
        if nome == "admin" and email == "admin@admin.com" and senha == "admin":
            return render_template("login.html", nome=nome, email=email, senha=senha)
        else:
            return render_template("login.html", nome=nome, email=email, senha=senha, erro=True)

    return render_template("login.html")


@app.route("/admin")
def admin():
    return redirect(url_for("home"))


@app.route("/loja", methods=["GET"])
def home():
    mensagem = request.args.get("mensagem")
    return render_template("index.html", produtos=MEUS_PRODUTOS, mensagem=mensagem)


@app.route("/pagamento", methods=["GET"])
def pagamento():
    nome_prod = request.args.get("nome")
    preco_prod = request.args.get("preco")

    if "carrinho" not in session:
        session["carrinho"] = {}

    if nome_prod and preco_prod:
        carrinho = session["carrinho"]
        try:
            preco_float = float(preco_prod)
            if nome_prod in carrinho:
                carrinho[nome_prod]["quantidade"] += 1
            else:
                carrinho[nome_prod] = {"preco": preco_float, "quantidade": 1}
            session.modified = True
        except ValueError:
            pass

    carrinho_obj, total = obter_carrinho()
    mensagem = request.args.get("mensagem")

    return render_template(
        "pagamento.html",
        catalogo=CATALOGO_DICT,
        carrinho=carrinho_obj,
        total=total,
        mensagem=mensagem
    )


@app.route("/add-item", methods=["POST"])
def add_item():
    produto_nome = request.form.get("produto")
    quantidade = int(request.form.get("quantidade", 1))

    preco = 0.0
    for categoria in CATALOGO_DICT.values():
        if produto_nome in categoria:
            preco = categoria[produto_nome]
            break

    if "carrinho" not in session:
        session["carrinho"] = {}

    carrinho = session["carrinho"]
    if produto_nome in carrinho:
        carrinho[produto_nome]["quantidade"] += quantidade
    else:
        carrinho[produto_nome] = {"preco": preco, "quantidade": quantidade}

    session.modified = True
    return redirect(url_for("pagamento"))


@app.route("/remover-item", methods=["POST"])
def remover_item():
    item_nome = request.form.get("nome_item")
    carrinho = session.get("carrinho", {})

    if item_nome in carrinho:
        del carrinho[item_nome]
        session.modified = True

    return redirect(url_for("pagamento"))


@app.route("/pagar", methods=["POST"])
def pagar():
    metodo = request.form.get("metodo-pagamento", "Pix")
    session["carrinho"] = {}
    mensagem = f"Pagamento realizado com sucesso via {metodo.upper()}! A BUYTAKU agradece."
    return redirect(url_for("home", mensagem=mensagem))


@app.route("/contato", methods=["POST"])
def contato():
    return render_template("index.html", produtos=MEUS_PRODUTOS, mensagem="Sua mensagem foi enviada com sucesso!")


if __name__ == "__main__":
    app.run(debug=True)