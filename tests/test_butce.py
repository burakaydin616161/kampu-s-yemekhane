import pytest

from app import app
from butce import aylik_butce_hesapla, hafta_ici_gun_sayisi


def test_hafta_ici_gun_sayisi():
    assert hafta_ici_gun_sayisi(2026, 12) == 23
    assert hafta_ici_gun_sayisi(2026, 2) == 20


def test_butce_yeterli():
    s = aylik_butce_hesapla(2026, 12, 40, 1000)
    assert s["toplam_maliyet"] == 920
    assert s["kalan"] == 80
    assert s["yeterli_mi"] is True
    assert s["karsilanabilen_ogun"] == 23


def test_butce_yetersiz():
    s = aylik_butce_hesapla(2026, 12, 40, 500)
    assert s["yeterli_mi"] is False
    assert s["kalan"] == -420
    assert s["karsilanabilen_ogun"] == 12


@pytest.mark.parametrize("ay,ucret,butce", [(13, 40, 100), (12, 0, 100), (12, 40, -1)])
def test_gecersiz_giris(ay, ucret, butce):
    with pytest.raises(ValueError):
        aylik_butce_hesapla(2026, ay, ucret, butce)


def test_butce_api():
    c = app.test_client()
    r = c.get("/api/butce?ay=2026-12&ogun_ucreti=40&butce=1000")
    assert r.status_code == 200 and r.get_json()["kalan"] == 80
    assert c.get("/api/butce?ay=2026-12&ogun_ucreti=0&butce=1000").status_code == 400
    assert c.get("/api/butce?ay=2026-12").status_code == 400
    assert c.get("/api/butce?ay=2026-12&ogun_ucreti=inf&butce=1000").status_code == 400
    r = c.get("/api/butce?ay=2026&ogun_ucreti=abc&butce=1000")
    assert r.status_code == 400 and "sayı olarak" in r.get_json()["hata"]


def test_butce_formu():
    r = app.test_client().post("/butce", data={"ay": "2026-12", "ogun_ucreti": "40", "butce": "500"})
    assert "yetersiz" in r.get_data(as_text=True)
