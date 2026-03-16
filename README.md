# Medikal Görüntü İşleme Projesi

Bu projede medikal görüntüler üzerinde temel **görüntü işleme ve kenar tespiti algoritmaları** Python kullanılarak uygulanmıştır.

Amaç, görüntüler üzerinde **ön işleme, filtreleme, kontrast artırma ve kenar tespiti** yöntemlerini analiz etmektir.

---

# Kullanılan Teknikler

Projede aşağıdaki görüntü işleme yöntemleri uygulanmıştır:

## Ön İşleme
- RGB → Gri dönüşümü
- Yeniden boyutlandırma (Nearest Neighbor)

## Filtreleme
- Median Filter
- Gaussian Filter (Convolution)

## Kontrast Artırma
- Histogram Equalization (HE)
- CLAHE (Contrast Limited Adaptive Histogram Equalization)
- Gamma Correction

## Kenar Tespiti
- Sobel Edge Detection
- Scharr Edge Detection
- Basit Canny Threshold yöntemi

---

# Kullanılan Teknolojiler

- Python
- NumPy
- Matplotlib

---

# Klasör Yapısı

```
medikal-goruntu-isleme
│
├── data/              # Örnek giriş görüntüleri
│   ├── benign
│   ├── polip
│   └── karsinom
│
├── src/
│   └── main.py        # Projenin ana kodu
│
├── .gitignore
└── README.md
```

---

# Kurulum

Python 3.x gereklidir.

Gerekli kütüphaneleri yüklemek için:

```bash
pip install numpy matplotlib
```

---

# Çalıştırma

Proje aşağıdaki komut ile çalıştırılabilir:

```bash
python src/main.py
```

Program her görüntü için:

- Ön işleme sonuçlarını  
- Kontrast artırma yöntemlerini  
- Histogram analizlerini  
- Kenar tespiti sonuçlarını  

ekranda görsel olarak gösterir.

Bir sonraki görüntüye geçmek için **Enter tuşuna basabilir veya pencereye tıklayabilirsiniz.**

---

# Projenin Amacı

Bu proje aşağıdaki konuları uygulamalı olarak incelemek için geliştirilmiştir:

- Görüntü iyileştirme yöntemleri
- Histogram tabanlı kontrast artırma
- Kenar tespiti algoritmaları
- Medikal görüntüler üzerinde görüntü işleme teknikleri
