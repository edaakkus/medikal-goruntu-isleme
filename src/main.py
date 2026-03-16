
# ==============================
# GORUNTU ISLEME PROJESI
# ==============================

import matplotlib.pyplot as plt
import numpy as np
import math
import os


def resize_nearest(img, new_h, new_w):
    old_h, old_w = img.shape
    resized = np.zeros((new_h, new_w))

    row_scale = old_h / new_h
    col_scale = old_w / new_w

    for i in range(new_h):
        for j in range(new_w):
            src_i = int(i * row_scale)
            src_j = int(j * col_scale)
            resized[i, j] = img[src_i, src_j]

    return resized


# ----------FILTRELER ----------
def median_filter(img, kernel_size=3):
    h, w = img.shape
    pad = kernel_size // 2

    padded = np.pad(img, pad, mode='edge')

    filtered = np.zeros((h, w))

    for i in range(h):
        for j in range(w):
            window = padded[i:i+kernel_size, j:j+kernel_size]
            filtered[i, j] = np.median(window)

    return filtered

def gaussian_kernel(size=3, sigma=1.0):
    kernel = np.zeros((size, size))
    k = size // 2

    for i in range(size):
        for j in range(size):
            x = i - k
            y = j - k
            kernel[i, j] = (1 / (2 * math.pi * sigma**2)) * \
                           math.exp(-(x**2 + y**2) / (2 * sigma**2))

    # Normalize
    kernel = kernel / np.sum(kernel)
    return kernel

def convolution(img, kernel):
    h, w = img.shape
    k = kernel.shape[0] // 2

    padded = np.pad(img, k, mode='edge')
    result = np.zeros((h, w))

    for i in range(h):
        for j in range(w):
            window = padded[i:i+kernel.shape[0], j:j+kernel.shape[1]]
            result[i, j] = np.sum(window * kernel)

    return result


# ---------- HISTOGRAM ----------
def compute_histogram(img):
    hist = np.zeros(256)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            hist[img[i, j]] += 1

    return hist


# ---------- KONTRAST ARTTIRMA ----------
def histogram_equalization(img):
    h, w = img.shape
    hist = compute_histogram(img)

    pdf = hist / (h * w)

    cdf = np.cumsum(pdf)

    eq_img = np.zeros((h, w), dtype=np.uint8)

    for i in range(h):
        for j in range(w):
            eq_img[i, j] = int(cdf[img[i, j]] * 255)

    return eq_img

def gamma_correction(img, gamma):
    img_norm = img / 255.0
    gamma_img = 255 * (img_norm ** gamma)
    return gamma_img.astype(np.uint8)

def clahe(img, tile_size=32, clip_limit=40):
    h, w = img.shape
    out = np.zeros_like(img)

    for y in range(0, h, tile_size):
        for x in range(0, w, tile_size):

            tile = img[y:y+tile_size, x:x+tile_size]

            # Histogram
            hist = compute_histogram(tile)

            # Clip limit uygula
            excess = 0
            for i in range(256):
                if hist[i] > clip_limit:
                    excess += hist[i] - clip_limit
                    hist[i] = clip_limit

            # Fazlalığı eşit dağıt
            hist += excess // 256

            # PDF & CDF
            pdf = hist / np.sum(hist)
            cdf = np.cumsum(pdf)

            # Tile equalization
            tile_eq = np.zeros_like(tile)
            for i in range(tile.shape[0]):
                for j in range(tile.shape[1]):
                    tile_eq[i, j] = int(cdf[tile[i, j]] * 255)

            out[y:y+tile_size, x:x+tile_size] = tile_eq

    return out


# ---------- KENAR ----------
def sobel_edge(img):
    Kx = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]])

    Ky = np.array([[-1, -2, -1],
                   [ 0,  0,  0],
                   [ 1,  2,  1]])

    gx = convolution(img, Kx)
    gy = convolution(img, Ky)

    magnitude = np.sqrt(gx**2 + gy**2)
    magnitude = np.clip(magnitude, 0, 255)

    return magnitude.astype(np.uint8)

def scharr_edge(img):
    Kx = np.array([[-3, 0, 3],
                   [-10, 0, 10],
                   [-3, 0, 3]])

    Ky = np.array([[-3, -10, -3],
                   [ 0,   0,  0],
                   [ 3,  10,  3]])

    gx = convolution(img, Kx)
    gy = convolution(img, Ky)

    magnitude = np.sqrt(gx**2 + gy**2)
    magnitude = np.clip(magnitude, 0, 255)

    return magnitude.astype(np.uint8)

def canny_simple(img, threshold=50):
    gx = sobel_edge(img)
    edges = np.zeros_like(gx)
    edges[gx > threshold] = 255
    return edges


image_paths = [
    "data/benign/benign1.jpg",
    "data/benign/benign2.jpg",
    "data/benign/benign3.jpg",
    "data/benign/benign4.jpg",
    "data/polip/polip1.jpg",
    "data/polip/polip2.jpg",
    "data/polip/polip3.jpg",
    "data/polip/polip4.jpg",
    "data/karsinom/karsinom1.jpg",
    "data/karsinom/karsinom2.jpg",
    "data/karsinom/karsinom3.jpg",
    "data/karsinom/karsinom4.jpg"
]

# ==============================

g_kernel = gaussian_kernel(size=3, sigma=1.0)

plt.figure(figsize=(14, 8))

for idx, image_path in enumerate(image_paths):

    image = plt.imread(image_path)

    # RGB -> Gri
    gray = (
        0.299 * image[:, :, 0] +
        0.587 * image[:, :, 1] +
        0.114 * image[:, :, 2]
    )

    # Resize
    gray_resized = resize_nearest(gray, 256, 256)

    # Filtreler
    median_img = median_filter(gray_resized, 3)
    gaussian_img = convolution(median_img, g_kernel)
    gaussian_uint8 = np.clip(gaussian_img, 0, 255).astype(np.uint8)

    # Kontrast artırma
    he_img = histogram_equalization(gaussian_uint8)
    gamma_img = gamma_correction(gaussian_uint8, gamma=0.7)
    clahe_img = clahe(gaussian_uint8, tile_size=32, clip_limit=40)

    # Histogramlar
    hist_gaussian = compute_histogram(gaussian_uint8)
    hist_he = compute_histogram(he_img)
    hist_clahe = compute_histogram(clahe_img)
    hist_gamma = compute_histogram(gamma_img)

    # Kenarlar
    sobel_he     = sobel_edge(he_img)
    scharr_he    = scharr_edge(he_img)
    canny_he     = canny_simple(he_img)

    sobel_clahe  = sobel_edge(clahe_img)
    scharr_clahe = scharr_edge(clahe_img)
    canny_clahe  = canny_simple(clahe_img)

    sobel_gamma  = sobel_edge(gamma_img)
    scharr_gamma = scharr_edge(gamma_img)
    canny_gamma  = canny_simple(gamma_img)

# =========================

    plt.clf()

    # ===== 1. SATIR: GÖRÜNTÜLER =====
    plt.subplot(3, 4, 1)
    plt.imshow(image)
    plt.title("1) Orijinal (RGB)")
    plt.axis("off")

    plt.subplot(3, 4, 2)
    plt.imshow(gray_resized, cmap="gray")
    plt.title("2) Gri + Resize")
    plt.axis("off")

    plt.subplot(3, 4, 3)
    plt.imshow(gaussian_uint8, cmap="gray")
    plt.title("3) Gaussian")
    plt.axis("off")

    plt.subplot(3, 4, 4)
    plt.imshow(median_img, cmap="gray")
    plt.title("4) Median")
    plt.axis("off")

    # ===== 2. SATIR: KONTRAST =====
    plt.subplot(3, 4, 5)
    plt.imshow(he_img, cmap="gray")
    plt.title("5) HE")
    plt.axis("off")

    plt.subplot(3, 4, 6)
    plt.imshow(clahe_img, cmap="gray")
    plt.title("6) CLAHE")
    plt.axis("off")

    plt.subplot(3, 4, 7)
    plt.imshow(gamma_img, cmap="gray")
    plt.title("7) Gamma")
    plt.axis("off")

    plt.subplot(3, 4, 8)
    plt.axis("off")

    # ===== 3. SATIR: HISTOGRAM =====
    plt.subplot(3, 4, 9)
    plt.plot(hist_gaussian)
    plt.title("Hist Gaussian")

    plt.subplot(3, 4, 10)
    plt.plot(hist_he)
    plt.title("Hist HE")

    plt.subplot(3, 4, 11)
    plt.plot(hist_clahe)
    plt.title("Hist CLAHE")

    plt.subplot(3, 4, 12)
    plt.plot(hist_gamma)
    plt.title("Hist Gamma")


    plt.suptitle(f"Görüntü {idx+1}  (Enter / Tıkla → Sonraki)", fontsize=14)
    plt.tight_layout()
    plt.draw()
    plt.waitforbuttonpress()

    # FIGURE 2: KENAR TESPITI

    plt.clf()
    
    # ---- HE ----
    plt.subplot(3, 4, 1)
    plt.imshow(he_img, cmap="gray")
    plt.title("HE")
    plt.axis("off")
    
    plt.subplot(3, 4, 2)
    plt.imshow(sobel_he, cmap="gray")
    plt.title("Sobel (HE)")
    plt.axis("off")
    
    plt.subplot(3, 4, 3)
    plt.imshow(scharr_he, cmap="gray")
    plt.title("Scharr (HE)")
    plt.axis("off")
    
    plt.subplot(3, 4, 4)
    plt.imshow(canny_he, cmap="gray")
    plt.title("Canny (HE)")
    plt.axis("off")
    
    # ---- CLAHE ----
    plt.subplot(3, 4, 5)
    plt.imshow(clahe_img, cmap="gray")
    plt.title("CLAHE")
    plt.axis("off")
    
    plt.subplot(3, 4, 6)
    plt.imshow(sobel_clahe, cmap="gray")
    plt.title("Sobel (CLAHE)")
    plt.axis("off")
    
    plt.subplot(3, 4, 7)
    plt.imshow(scharr_clahe, cmap="gray")
    plt.title("Scharr (CLAHE)")
    plt.axis("off")
    
    plt.subplot(3, 4, 8)
    plt.imshow(canny_clahe, cmap="gray")
    plt.title("Canny (CLAHE)")
    plt.axis("off")
    
    # ---- GAMMA ----
    plt.subplot(3, 4, 9)
    plt.imshow(gamma_img, cmap="gray")
    plt.title("Gamma")
    plt.axis("off")
    
    plt.subplot(3, 4, 10)
    plt.imshow(sobel_gamma, cmap="gray")
    plt.title("Sobel (Gamma)")
    plt.axis("off")
    
    plt.subplot(3, 4, 11)
    plt.imshow(scharr_gamma, cmap="gray")
    plt.title("Scharr (Gamma)")
    plt.axis("off")
    
    plt.subplot(3, 4, 12)
    plt.imshow(canny_gamma, cmap="gray")
    plt.title("Canny (Gamma)")
    plt.axis("off")
    
    plt.suptitle(f"Kenar Tespiti Sonuclari - Goruntu {idx+1}", fontsize=14)
    plt.tight_layout()
    plt.draw()
    plt.waitforbuttonpress()