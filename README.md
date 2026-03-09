# 🗂️ Záložková anketa – školní projekt

Jednoduchá webová hlasovací aplikace postavená na **Python 3 + Flask + SQLite**.

---

## Struktura projektu

```
voting_app/
├── app.py                # Hlavní aplikace (Flask routy, logika, DB)
├── votes.db              # SQLite databáze (vytvoří se automaticky)
├── templates/
│   ├── base.html         # Základní šablona (header, nav, footer)
│   ├── index.html        # Hlasovací formulář
│   ├── results.html      # Výsledky ankety
│   ├── reset.html        # Reset hlasování (chráněno tokenem)
│   └── about.html        # O anketě
├── static/
│   └── style.css         # Styly (interní CSS)
└── README.md
```

---

## 1. Spuštění lokálně

### Požadavky
- Python 3.8+
- pip

### Instalace

```bash
# 1. Přejdi do složky projektu
cd voting_app

# 2. (Volitelně) vytvoř virtuální prostředí
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Nainstaluj Flask
pip install flask

# 4. Spusť aplikaci
python app.py
```

Aplikace poběží na **http://127.0.0.1:5000**

Databáze `votes.db` se vytvoří automaticky při prvním spuštění.

---

## 2. Nasazení na PythonAnywhere (free plán)

### Krok za krokem

1. **Zaregistruj se** na [www.pythonanywhere.com](https://www.pythonanywhere.com) (free plán stačí).

2. **Nahraj soubory** přes záložku *Files*:
   - Vytvoř složku `/home/<tvůj_username>/voting_app/`
   - Nahraj `app.py`, složky `templates/` a `static/` se všemi soubory.

3. **Nainstaluj Flask** přes *Bash konzoli*:
   ```bash
   pip3 install --user flask
   ```

4. **Nastav webovou aplikaci**:
   - Jdi na záložku **Web** → klikni **Add a new web app**
   - Vyber: *Manual configuration* → *Python 3.10*
   - **Source code**: `/home/<tvůj_username>/voting_app`
   - **Working directory**: `/home/<tvůj_username>/voting_app`

5. **Nastav WSGI soubor**:
   - V záložce *Web* klikni na odkaz WSGI souboru (např. `/var/www/<username>_pythonanywhere_com_wsgi.py`)
   - Nahraď celý obsah tímto kódem:
   ```python
   import sys
   import os

   path = '/home/<tvůj_username>/voting_app'
   if path not in sys.path:
       sys.path.insert(0, path)

   from app import app, init_db
   init_db()        # vytvoří DB při prvním startu
   application = app
   ```
   - Ulož soubor.

6. **Spusť aplikaci**:
   - V záložce *Web* klikni na zelené tlačítko **Reload**.
   - Aplikace je dostupná na `https://<tvůj_username>.pythonanywhere.com`

---

## 3. Jak provést změnu kódu a znovu nasadit

1. Uprav soubor lokálně (např. `app.py` nebo šablonu).

2. Nahraj změněný soubor na PythonAnywhere:
   - Záložka **Files** → najdi soubor → klikni na název → **Upload** (nebo přímo edituj v online editoru).

3. **Restartuj aplikaci**:
   - Záložka **Web** → klikni **Reload**.

4. Změny jsou okamžitě aktivní.

> **Tip:** Větší projekty lze nahrát přes Git:
> ```bash
> # V Bash konzoli na PythonAnywhere:
> cd ~/voting_app
> git pull
> ```

---

## 4. Monitoring přes UptimeRobot

Free plán PythonAnywhere uspí aplikaci, pokud ji nikdo nenavštíví po delší dobu. UptimeRobot ji bude pravidelně pingovat a udržovat ji aktivní.

### Postup nastavení

1. Zaregistruj se na [uptimerobot.com](https://uptimerobot.com) (free plán).

2. Klikni na **+ Add New Monitor**.

3. Vyplň:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: Záložková anketa
   - **URL**: `https://<tvůj_username>.pythonanywhere.com`
   - **Monitoring Interval**: 5 minutes

4. Klikni **Create Monitor**.

UptimeRobot bude každých 5 minut navštěvovat tvoji aplikaci a tím ji udržovat vzhůru. Zároveň dostaneš email, pokud aplikace vypadne.

---

## 5. Reset hlasování

Na stránce `/reset` zadej správný token (nastaven v `app.py` jako `RESET_TOKEN`).
Token se **nikdy** neposílá do HTML šablony – je porovnáván výhradně na serveru.

Výchozí token: `tajny_token_123` – **změň ho před nasazením!**

---

## Použité technologie

| Technologie | Verze | Účel |
|-------------|-------|------|
| Python | 3.8+ | Backend jazyk |
| Flask | 3.x | Webový framework |
| SQLite | vestavěný | Databáze |
| Jinja2 | vestavěný | HTML šablony |
| PythonAnywhere | free | Hosting |
