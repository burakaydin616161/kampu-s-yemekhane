from datetime import date

from flask import Flask, jsonify, render_template, request

from butce import aylik_butce_hesapla
from menu import gunun_menusu

app = Flask(__name__)
app.json.ensure_ascii = False  # Turkce karakterler JSON'da okunakli gorunsun


def tarih_oku(metin):
    if not metin:
        return date.today()
    return date.fromisoformat(metin)


# ---------- Görev 1: Günlük menü ----------
@app.get("/")
def menu_sayfasi():
    try:
        tarih = tarih_oku(request.args.get("tarih"))
    except ValueError:
        return render_template("menu.html", sonuc={"durum": "hatali"}, tarih=""), 400
    return render_template("menu.html", sonuc=gunun_menusu(tarih), tarih=tarih.isoformat())


@app.get("/api/menu")
def menu_api():
    try:
        tarih = tarih_oku(request.args.get("tarih"))
    except ValueError:
        return jsonify({"hata": "Tarih YYYY-AA-GG biçiminde olmalı."}), 400
    sonuc = gunun_menusu(tarih)
    return jsonify(sonuc), (404 if sonuc["durum"] == "yok" else 200)


# ---------- Görev 2: Bütçe hesaplayıcı ----------
def butce_parametreleri(kaynak):
    try:
        yil, ay = map(int, kaynak["ay"].split("-"))
        return yil, ay, float(kaynak["ogun_ucreti"]), float(kaynak["butce"])
    except (KeyError, ValueError):
        raise ValueError("Ay (YYYY-AA), öğün ücreti ve bütçe sayı olarak girilmeli.")


@app.route("/butce", methods=["GET", "POST"])
def butce_sayfasi():
    sonuc, hata = None, None
    if request.method == "POST":
        try:
            sonuc = aylik_butce_hesapla(*butce_parametreleri(request.form))
        except (KeyError, ValueError) as e:
            hata = str(e) or "Geçersiz giriş."
    return render_template("butce.html", sonuc=sonuc, hata=hata)


@app.get("/api/butce")
def butce_api():
    try:
        return jsonify(aylik_butce_hesapla(*butce_parametreleri(request.args)))
    except (KeyError, ValueError) as e:
        return jsonify({"hata": str(e) or "Geçersiz giriş."}), 400


if __name__ == "__main__":
    app.run(debug=True)
