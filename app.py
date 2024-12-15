from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import matplotlib.pyplot as plt
import io
import base64
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, accuracy_score
import pandas as pd


# Configuração básica do Flask
app = Flask(__name__)
app.secret_key = "4c3a6b2ef8c2435797a93f5d867dc1bf2841239b63a1d2b5c8e243c913b4a2d5"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de exemplo
class Dados(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faixa_etaria = db.Column(db.String(50), nullable=False)
    km_percorridos = db.Column(db.Integer, nullable=False)
    gasto_diario = db.Column(db.Float, nullable=False)
    tempo = db.Column(db.Integer, nullable=False)
    acesso_internet = db.Column(db.String(10), nullable=False)
    local_acesso = db.Column(db.String(50), nullable=False)

# Página inicial
@app.route("/")
def index():
    return render_template("index.html")

# Página de Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "HZD4M" and password == "H@ss@n99zeidam":
            session["logged_in"] = True
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("admin_panel"))
        else:
            flash("Usuário ou senha inválidos.", "danger")
    return render_template("login.html")

    

# Página de Formulário
@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        # Coletar dados do formulário
        faixa_etaria = request.form.get("faixa_etaria")
        km_percorridos = request.form.get("km_percorridos")
        gasto_diario = request.form.get("gasto_diario")
        tempo = request.form.get("tempo")
        acesso_internet = request.form.get("acesso_internet")
        local_acesso = request.form.get("local_acesso")
        
        # Criar um novo registro no banco
        novo_dado = Dados(
            faixa_etaria=faixa_etaria,
            km_percorridos=km_percorridos,
            gasto_diario=gasto_diario,
            tempo=tempo,
            acesso_internet=acesso_internet,
            local_acesso=local_acesso,
        )
        db.session.add(novo_dado)
        db.session.commit()
        flash("Dados enviados com sucesso!", "success")
        return redirect(url_for("results"))
    
    return render_template("form.html")

@app.route("/process", methods=["POST"])
def process():
    # Código para processar os dados do formulário
    return redirect(url_for("results"))

# Página de Resultados
@app.route("/results")
def results():
    # Consulta todos os dados no banco
    dados = Dados.query.all()
    if not dados:
        flash("Nenhum dado encontrado. Contribua com o formulário antes de acessar os resultados.", "info")
        return redirect(url_for("form"))
    
    # Transformar os dados em um DataFrame
    data_list = [{
        "Faixa Etária": dado.faixa_etaria,
        "Km Percorridos": dado.km_percorridos,
        "Gasto Diário (R$)": dado.gasto_diario,
        "Tempo (min)": dado.tempo,
        "Acesso à Internet": dado.acesso_internet,
        "Local de Acesso": dado.local_acesso
    } for dado in dados]
    
    df = pd.DataFrame(data_list)
    
    # --- Análise descritiva ---
    stats = df[["Km Percorridos", "Gasto Diário (R$)", "Tempo (min)"]].describe().T
    stats["Moda"] = df[["Km Percorridos", "Gasto Diário (R$)", "Tempo (min)"]].mode().iloc[0]
    stats["Mediana"] = df[["Km Percorridos", "Gasto Diário (R$)", "Tempo (min)"]].median()
    stats["Variância"] = df[["Km Percorridos", "Gasto Diário (R$)", "Tempo (min)"]].var()
    stats["Desvio Padrão"] = df[["Km Percorridos", "Gasto Diário (R$)", "Tempo (min)"]].std()
     
    stats = stats.applymap(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)
    
    # --- Regressão Linear Simples ---
    X_linear = df[["Km Percorridos"]].values.reshape(-1, 1)  # Questão 02
    y_linear = df["Gasto Diário (R$)"].values  # Questão 03
    
    model_simple = LinearRegression()
    model_simple.fit(X_linear, y_linear)
    y_pred_simple = model_simple.predict(X_linear)
    
    # Gráfico de regressão linear simples
    plt.figure()
    plt.scatter(X_linear, y_linear, label="Dados Reais", color="blue")
    plt.plot(X_linear, y_pred_simple, label="Regressão Linear", color="red")
    plt.title("Regressão Linear Simples")
    plt.xlabel("Km Percorridos")
    plt.ylabel("Gasto Diário (R$)")
    plt.ylim(0, max(y_linear.max(), 50))  # Define um limite no eixo Y apropriado (ex.: 0 a 50 reais)
    plt.legend()
    img_simple = io.BytesIO()
    plt.savefig(img_simple, format="png")
    img_simple.seek(0)
    plot_simple_url = base64.b64encode(img_simple.getvalue()).decode()
    plt.close()

    
    # --- Regressão Linear Multivariada ---
    X_multi = df[["Km Percorridos", "Tempo (min)"]]  # Questões 02, 03 e 04
    y_multi = df["Gasto Diário (R$)"]
    
    model_multi = LinearRegression()
    model_multi.fit(X_multi, y_multi)
    y_pred_multi = model_multi.predict(X_multi)
    
    # Gráfico de regressão linear multivariada
    # Gráfico de regressão linear multivariada
    plt.figure()
    plt.scatter(y_multi, y_pred_multi, color="purple", alpha=0.7)
    plt.plot(
    [y_multi.min(), y_multi.max()],
    [y_multi.min(), y_multi.max()],
    color="red", linestyle="--", label="Linha Ideal"
)
    plt.title("Regressão Linear Multivariada")
    plt.xlabel("Valores Reais")
    plt.ylabel("Valores Preditos")
    plt.ylim(0, max(y_multi.max(), 50))  # Define um limite no eixo Y (ex.: até 50 reais)
    plt.legend()
    img_multi = io.BytesIO()
    plt.savefig(img_multi, format="png")
    img_multi.seek(0)
    plot_multi_url = base64.b64encode(img_multi.getvalue()).decode()
    plt.close()

    
    # --- Regressão Logística ---
    X_log = df[["Km Percorridos", "Tempo (min)"]]  # Questões 05 e 06
    y_log = (df["Acesso à Internet"] == "Sim").astype(int)  # Transformar em binário
    
    if len(y_log.unique()) > 1:  # Garantir que temos classes diferentes para a regressão logística
        model_log = LogisticRegression()
        model_log.fit(X_log, y_log)
        y_pred_log = model_log.predict(X_log)
        accuracy = accuracy_score(y_log, y_pred_log)
        
        # Gráfico de regressão logística
        plt.figure()
        plt.scatter(y_log, y_pred_log, color="green")
        plt.title(f"Regressão Logística (Acurácia: {accuracy:.2f})")
        plt.xlabel("Valores Reais")
        plt.ylabel("Valores Preditos")
        img_log = io.BytesIO()
        plt.savefig(img_log, format="png")
        img_log.seek(0)
        plot_log_url = base64.b64encode(img_log.getvalue()).decode()
        plt.close()
    else:
        plot_log_url = None
    
    # Renderizar a página com os resultados
    return render_template(
        "results.html",
        stats=stats.to_html(classes="table"),
        plot_simple_url=plot_simple_url,
        plot_multi_url=plot_multi_url,
        plot_log_url=plot_log_url
    )

# Painel Administrativo
@app.route("/admin_panel")
def admin_panel():
    if not session.get("logged_in"):
        flash("Por favor, faça login para acessar o painel.", "warning")
        return redirect(url_for("login"))
    return render_template("admin_panel.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Você saiu com sucesso.", "info")
    return redirect(url_for("login"))

# Configuração do Painel Administrativo com Flask-Admin
admin = Admin(app, template_mode="bootstrap4")
admin.add_view(ModelView(Dados, db.session)) 




# Inicializar o banco de dados
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Banco de dados criado com sucesso!")
    app.run(debug=True)
