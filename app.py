"""
Webová aplikace pro hlasování – školní projekt
Autor: student
Framework: Flask, databáze: SQLite
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
# Tajný klíč pro flash zprávy (sessions)
app.secret_key = "skolni_projekt_tajny_klic_2024"


# ─────────────────────────────────────────
# BEZPEČNOSTNÍ HLAVIČKY
# ─────────────────────────────────────────

@app.after_request
def set_security_headers(response):
    """Přidá bezpečnostní HTTP hlavičky ke každé odpovědi."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "script-src 'none';"
    )
    return response


@app.before_request
def redirect_https():
    """Přesměruje HTTP požadavky na HTTPS (pro PythonAnywhere)."""
    if request.headers.get('X-Forwarded-Proto') == 'http':
        return redirect(request.url.replace('http://', 'https://'), code=301)

# ─────────────────────────────────────────
# KONFIGURACE
# ─────────────────────────────────────────

# Token pro reset hlasování – NIKDY ho neposílej do šablony přímo!
RESET_TOKEN = "tajny_token_123"

# Cesta k databázovému souboru
DB_PATH = os.path.join(os.path.dirname(__file__), "votes.db")

# Možnosti hlasování
CHOICES = {
    1: "1–5",
    2: "6–15",
    3: "16–30",
    4: "30+"
}

# ─────────────────────────────────────────
# DATABÁZE
# ─────────────────────────────────────────

def get_db():
    """Vrátí připojení k SQLite databázi."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Vytvoří tabulku hlasů, pokud ještě neexistuje."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                choice  INTEGER NOT NULL,
                voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def get_results():
    """Vrátí slovník {choice_id: počet_hlasů} pro všechny možnosti."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT choice, COUNT(*) AS cnt FROM votes GROUP BY choice"
        ).fetchall()

    results = {cid: 0 for cid in CHOICES}   # inicializuj nulami
    for row in rows:
        if row["choice"] in results:
            results[row["choice"]] = row["cnt"]
    return results


def get_total():
    """Vrátí celkový počet hlasů."""
    with get_db() as conn:
        row = conn.execute("SELECT COUNT(*) AS cnt FROM votes").fetchone()
    return row["cnt"] if row else 0


# ─────────────────────────────────────────
# ROUTY
# ─────────────────────────────────────────

@app.route("/", methods=["GET", "POST"])
def index():
    """Hlavní stránka s hlasovacím formulářem."""
    if request.method == "POST":
        choice_raw = request.form.get("choice")

        # Ošetření chyby – uživatel nevybral možnost
        if not choice_raw:
            flash("Prosím vyber jednu z možností před odesláním.", "error")
            return redirect(url_for("index"))

        try:
            choice = int(choice_raw)
        except ValueError:
            flash("Neplatná hodnota. Zkus to znovu.", "error")
            return redirect(url_for("index"))

        # Ošetření neplatné volby
        if choice not in CHOICES:
            flash("Vybraná možnost neexistuje.", "error")
            return redirect(url_for("index"))

        # Uložení hlasu do databáze
        with get_db() as conn:
            conn.execute("INSERT INTO votes (choice) VALUES (?)", (choice,))
            conn.commit()

        return redirect(url_for("results"))

    return render_template("index.html", choices=CHOICES)


@app.route("/results")
def results():
    """Stránka s výsledky hlasování."""
    data = get_results()
    total = get_total()

    # Vypočítej procenta pro každou možnost
    percentages = {}
    for cid, cnt in data.items():
        percentages[cid] = round((cnt / total * 100) if total > 0 else 0, 1)

    return render_template(
        "results.html",
        choices=CHOICES,
        results=data,
        total=total,
        percentages=percentages
    )


@app.route("/reset", methods=["GET", "POST"])
def reset():
    """Stránka pro reset hlasování chráněná tokenem."""
    if request.method == "POST":
        token = request.form.get("token", "")

        if token == RESET_TOKEN:
            # Token správný → smaž všechny hlasy
            with get_db() as conn:
                conn.execute("DELETE FROM votes")
                conn.commit()
            flash("Všechny hlasy byly úspěšně smazány.", "success")
            return redirect(url_for("results"))
        else:
            # Token špatný → zobraz chybu, ale nevyzrazuj správný token
            flash("Zadaný token je nesprávný. Zkus to znovu.", "error")
            return redirect(url_for("reset"))

    return render_template("reset.html")


@app.route("/about")
def about():
    """Stránka O anketě."""
    return render_template("about.html")


# ─────────────────────────────────────────
# SPUŠTĚNÍ
# ─────────────────────────────────────────

if __name__ == "__main__":
    init_db()           # Vytvoř DB při prvním spuštění
    app.run(debug=True) # debug=True jen lokálně!
