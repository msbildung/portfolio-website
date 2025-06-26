# app.py
from flask import Flask, render_template, request, flash, redirect, url_for
import datetime

# Die Flask-Anwendung initialisieren
app = Flask(__name__)

# Sicherheitsschlüssel (einmal ganz oben definieren)
app.config['SECRET_KEY'] = 'ein-sehr-geheimer-schluessel-den-niemand-erraten-kann'

# === DATEN ===
# Definiere die Projektliste hier, damit alle Funktionen darauf zugreifen können
meine_projekte = [
    {
        'slug': 'projekt-a',
        'titel': 'Projekt A - Datenvisualisierer',
        'beschreibung': 'Eine coole Web-App zur Datenvisualisierung mit Chart.js.',
        'technologien': ['Python', 'Flask', 'Chart.js'],
        'link': 'https://github.com/deinname/projekt-a',
        'details': 'In diesem Projekt habe ich gelernt, wie man Backend-Daten von Flask an ein Frontend-JavaScript-Framework übergibt. Die größte Herausforderung war die asynchrone Aktualisierung der Charts.'
    },
    {
        'slug': 'projekt-b-discord-bot',
        'titel': 'Projekt B - Discord Bot',
        'beschreibung': 'Ein interaktiver Bot für die Chat-Plattform Discord.',
        'technologien': ['Python', 'Discord.py', 'APIs'],
        'link': 'https://github.com/deinname/projekt-b',
        'details': 'Hier lag der Fokus auf der Arbeit mit externen APIs und der ereignisbasierten Programmierung. Der Bot reagiert auf Befehle der Nutzer in Echtzeit.'
    },
]


# === ROUTEN ===

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projekte')
def projekte():
    # Die Funktion greift jetzt einfach auf die globale Variable zu
    return render_template('projekte.html', projekte=meine_projekte)

# Korrekt auf der obersten Ebene platziert
@app.route('/projekt/<slug>')
def projekt_detail(slug):
    # Finde das Projekt mit dem passenden Slug in der globalen Liste
    projekt = next((p for p in meine_projekte if p['slug'] == slug), None)
    
    if projekt is None:
        # Wenn kein Projekt gefunden wird, wird der 404-Handler ausgelöst
        return page_not_found(404)
        
    return render_template('projekt_detail.html', projekt=projekt)

@app.route('/ueber-mich')
def ueber_mich():
    return render_template('ueber-mich.html')

@app.route('/kontakt', methods=['GET', 'POST'])
def kontakt():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        if not name or not email or not message:
            flash('Bitte alle Felder ausfüllen!', 'danger')
            return redirect(url_for('kontakt'))

        with open('kontaktnachrichten.txt', 'a', encoding='utf-8') as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"--- Neue Nachricht vom {timestamp} ---\n")
            f.write(f"Name: {name}\n")
            f.write(f"E-Mail: {email}\n")
            f.write(f"Nachricht: {message}\n\n")

        flash('Vielen Dank für deine Nachricht! Ich melde mich bald.', 'success')
        return redirect(url_for('kontakt'))

    return render_template('kontakt.html')

# === FEHLER-HANDLER ===

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# === SERVER START ===

if __name__ == '__main__':
    app.run(debug=True)