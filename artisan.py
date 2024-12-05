import cv2
import numpy as np
def pixelate(image, pixel_size):
    height, width = image.shape[:2]
    temp = cv2.resize(image, (width // pixel_size, height // pixel_size), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
def watercolor(image):
    for _ in range(3):
        image = cv2.bilateralFilter(image, 15, 80, 80)
    edges = cv2.Canny(image, 100, 200)
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return cv2.addWeighted(image, 0.8, edges, 0.2, 0)
def vintage(image):
    rows, cols = image.shape[:2]
    x = cv2.getGaussianKernel(cols, 200)
    y = cv2.getGaussianKernel(rows, 200)
    mask = y * x.T
    mask = mask / mask.max()
    vintage_filter = np.zeros_like(image, dtype=np.float32)
    for i in range(3):
        vintage_filter[:, :, i] = mask
    return (image * vintage_filter).astype(np.uint8)
def apply_filter(image_path, filter_name):
    image = cv2.imread(image_path)
    if image is None:
        print("Image not found!")
        return
    
    if filter_name == "pixelate":
        result = pixelate(image, 10)
    elif filter_name == "watercolor":
        result = watercolor(image)
    elif filter_name == "vintage":
        result = vintage(image)
    else:
        print("Invalid filter name!")
        return
    cv2.imshow(f"{filter_name.capitalize()} Filter", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Available filters: pixelate, watercolor, vintage")
    image_path = input("Enter the path to the image: ")
    filter_name = input("Enter the filter name: ").lower()
    apply_filter(image_path, filter_name)