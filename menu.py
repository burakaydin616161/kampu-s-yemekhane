"""Görev 1: Günlük menü görüntüleme."""
import json
from datetime import date
from pathlib import Path

VERI_DOSYASI = Path(__file__).parent / "data" / "menu.json"


def menuleri_yukle(dosya=VERI_DOSYASI):
    with open(dosya, encoding="utf-8") as f:
        return json.load(f)


def gunun_menusu(tarih: date, menuler=None):
    """Verilen tarihin menüsünü döndürür.

    Dönüş: {"durum": "ok", "menu": {...}} | {"durum": "hafta_sonu"} | {"durum": "yok"}
    """
    if menuler is None:
        menuler = menuleri_yukle()
    if tarih.weekday() >= 5:
        return {"durum": "hafta_sonu", "tarih": tarih.isoformat()}
    menu = menuler.get(tarih.isoformat())
    if menu is None:
        return {"durum": "yok", "tarih": tarih.isoformat()}
    toplam_kalori = sum(y["kalori"] for y in menu)
    return {
        "durum": "ok",
        "tarih": tarih.isoformat(),
        "yemekler": menu,
        "toplam_kalori": toplam_kalori,
    }
