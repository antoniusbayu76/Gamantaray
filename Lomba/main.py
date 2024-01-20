import cv2
import numpy as np

# Fungsi untuk melakukan segmentasi warna pada citra
def segment_color(image, lower_bound, upper_bound):
    lower = np.array(lower_bound, dtype=np.uint8)
    upper = np.array(upper_bound, dtype=np.uint8)
    mask = cv2.inRange(image, lower, upper)
    result = cv2.bitwise_and(image, image, mask=mask)
    return result

# Alamat gambar yang akan di-segmentasi
image_path = "D:\GAMANTARAY\Vision\Lomba/bola.jpg"

# Baca gambar
image = cv2.imread(image_path)

if image is not None:
    # Segmentasi warna merah
    lower_red = [0, 0, 100]
    upper_red = [200, 100, 255]
    red_segmented = segment_color(image, lower_red, upper_red)

    # Segmentasi warna hijau
    lower_green = [0, 100, 0]
    upper_green = [250, 255, 100]
    green_segmented = segment_color(image, lower_green, upper_green)

    # Tampilkan citra asli dan hasil segmentasi
    cv2.imshow("Original Image", image)
    cv2.imshow("Red Segmented Image", red_segmented)
    cv2.imshow("Green Segmented Image", green_segmented)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Gagal membaca gambar")



