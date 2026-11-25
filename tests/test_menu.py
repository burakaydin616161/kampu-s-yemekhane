from datetime import date

from app import app
from menu import gunun_menusu

ORNEK = {"2026-12-01": [{"ad": "Mercimek Çorbası", "kalori": 180},
                        {"ad": "Tavuk Sote", "kalori": 380}]}


def test_menu_var():
    sonuc = gunun_menusu(date(2026, 12, 1), ORNEK)
    assert sonuc["durum"] == "ok"
    assert sonuc["toplam_kalori"] == 560


def test_menu_yok():
    assert gunun_menusu(date(2026, 12, 2), ORNEK)["durum"] == "yok"


def test_hafta_sonu():
    assert gunun_menusu(date(2026, 12, 5), ORNEK)["durum"] == "hafta_sonu"


def test_menu_api():
    c = app.test_client()
    r = c.get("/api/menu?tarih=2026-12-01")
    assert r.status_code == 200
    assert len(r.get_json()["yemekler"]) == 4
    assert c.get("/api/menu?tarih=2030-01-01").status_code == 404
    assert c.get("/api/menu?tarih=yanlis").status_code == 400


def test_menu_sayfasi():
    r = app.test_client().get("/?tarih=2026-12-05")
    assert "hafta sonu kapalıdır" in r.get_data(as_text=True)
