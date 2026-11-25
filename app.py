from datetime import date

from flask import Flask, jsonify, render_template, request

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


if __name__ == "__main__":
    app.run(debug=True)
