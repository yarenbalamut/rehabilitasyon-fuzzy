# Yoğun Bakım Stabilite Değerlendirme Sistemi

Bu proje, yoğun bakımdaki hastaların hayati belirtilerine göre aciliyet seviyesini ve stabilizasyon süresini bulan bir bulanık mantık sistemidir. Girdi olarak kalp atış hızı, solunum hızı, oksijen doygunluğu, sistolik tansiyon ve vücut sıcaklığı alır. Çıktı olarak ise hastanın aciliyet skoru ve tahmini stabilizasyon süresi hesaplanır.

## Özellikler

- Kullanıcı dostu arayüz (Tkinter tabanlı)
- Girdi verilerine göre grafiksel çıktı
- Gelişmiş bulanık mantık sistemi (skfuzzy kullanılarak oluşturulmuş)
- 70'ten fazla bulanık kural

## Kurulum

Projeyi klonlamak için terminalde aşağıdaki komutu kullanabilirsiniz:

```bash
git clone https://github.com/yarenbalamut/rehabilitasyon-fuzzy.git


``` bash
cd rehabilitasyon-fuzzy
```


```bash
pip install -r requirements.txt

```

``` bash
python main.py
```
