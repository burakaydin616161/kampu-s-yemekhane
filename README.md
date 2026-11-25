# Kampüs Yemekhane

## Problem ve hedef kullanıcı

Üniversite öğrencileri yemekhanede o gün ne çıkacağını öğrenmek için duyuru panolarına ya da sosyal medya paylaşımlarına bakmak zorunda kalıyor. Ayrıca ay boyunca yemekhanede yemenin bütçelerine ne kadar yük getireceğini önceden hesaplayamıyorlar.

**Kampüs Yemekhane**, öğrencilerin seçtikleri günün menüsünü kalori bilgisiyle birlikte görmelerini ve aylık yemekhane harcamalarının bütçelerine yetip yetmeyeceğini hesaplamalarını sağlayan basit bir web uygulamasıdır.

## İş takip panosu

Pano: **[GitHub Projects – Kampüs Yemekhane](https://github.com/users/burakaydin616161/projects/5)**

Sütunlar: Yapılacak · Devam Ediyor · Tamamlandı

## Kurulum ve çalıştırma

Gereksinim: Python 3.10+

```bash
git clone https://github.com/burakaydin616161/kampu-s-yemekhane.git
cd kampu-s-yemekhane
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Uygulama http://127.0.0.1:5000 adresinde açılır.

Testleri çalıştırmak için:

```bash
pytest -v
```


## Özellikleri deneme

> Örnek menü verisi 23 Kasım – 31 Aralık 2026 arasındaki hafta içi günleri kapsar (`data/menu.json`).

### Özellik 1 – Günlük menü

- Tarayıcıda http://127.0.0.1:5000/?tarih=2026-12-01 adresini açın: çorba, ana yemek, yan yemek ve tatlı kalorileriyle ve toplam kaloriyle listelenir.
- `?tarih=2026-12-05` (Cumartesi) → "Yemekhane hafta sonu kapalıdır."
- `?tarih=2027-03-01` (veri yok) → "Bu tarih için menü bulunamadı."
- API: http://127.0.0.1:5000/api/menu?tarih=2026-12-01 → JSON döner (veri yoksa 404, hatalı tarih 400).

### Özellik 2 – Aylık bütçe hesaplayıcı

- http://127.0.0.1:5000/butce sayfasında Ay: **Aralık 2026**, Öğün ücreti: **40** (okul yemekhanesi ücreti, formda varsayılan), Bütçe: **1000** girin.
  Beklenen: 23 hafta içi gün, toplam 920.00 TL, kalan 80.00 TL, "Bütçe bu ay için yeterli."
- Bütçeyi **500** yapın → kalan -420.00 TL, 12/23 öğün karşılanır, "Bütçe bu ay için yetersiz."
- API: http://127.0.0.1:5000/api/butce?ay=2026-12&ogun_ucreti=40&butce=1000

## Proje yapısı

```
app.py            Flask uygulaması ve yönlendirmeler
menu.py           Günlük menü mantığı
butce.py          Bütçe hesaplama mantığı
data/menu.json    Örnek menü verisi
templates/        HTML şablonları
tests/            pytest testleri

```
