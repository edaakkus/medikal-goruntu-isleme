# Görüntü İşleme Projesi

Bu projede örnek görüntüler üzerinde şu adımlar uygulanır:

- **Ön işleme**: griye çevirme, yeniden boyutlandırma (nearest)
- **Filtreleme**: median, gaussian (konvolüsyon)
- **Kontrast artırma**: histogram equalization (HE), CLAHE, gamma correction
- **Kenar tespiti**: Sobel, Scharr, basit Canny eşiği

## Klasör yapısı

- `src/main.py`: çalıştırılabilir kod
- `data/`: örnek giriş görüntüleri (benign/polip/karsinom)
- `ciktilar/`: üretilen çıktı görselleri (git'e dahil edilmez)

## Kurulum

Python 3.x gerekli.

```bash
pip install numpy matplotlib
```

## Çalıştırma

```bash
python src/main.py
```

Kod, her görsel için ekran üzerinde sonuçları gösterir. Devam etmek için pencere üzerinde **Enter** veya **tıklama** bekler.
