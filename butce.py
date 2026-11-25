"""Görev 2: Aylık yemekhane bütçe hesaplayıcı."""
import calendar
import math


def hafta_ici_gun_sayisi(yil: int, ay: int) -> int:
    _, gun_sayisi = calendar.monthrange(yil, ay)
    return sum(
        1 for gun in range(1, gun_sayisi + 1)
        if calendar.weekday(yil, ay, gun) < 5
    )


def aylik_butce_hesapla(yil: int, ay: int, ogun_ucreti: float, butce: float) -> dict:
    """Ayın tüm hafta içi günlerinde yemekhanede yemenin maliyetini hesaplar."""
    if not (math.isfinite(ogun_ucreti) and math.isfinite(butce)):
        raise ValueError("Öğün ücreti ve bütçe geçerli bir sayı olmalı.")
    if not 1 <= ay <= 12:
        raise ValueError("Ay 1 ile 12 arasında olmalı.")
    if ogun_ucreti <= 0:
        raise ValueError("Öğün ücreti 0'dan büyük olmalı.")
    if butce < 0:
        raise ValueError("Bütçe negatif olamaz.")

    gun = hafta_ici_gun_sayisi(yil, ay)
    toplam = round(gun * ogun_ucreti, 2)
    kalan = round(butce - toplam, 2)
    return {
        "yil": yil,
        "ay": ay,
        "hafta_ici_gun": gun,
        "ogun_ucreti": ogun_ucreti,
        "butce": butce,
        "toplam_maliyet": toplam,
        "kalan": kalan,
        "yeterli_mi": kalan >= 0,
        "karsilanabilen_ogun": min(gun, int(butce // ogun_ucreti)),
    }
