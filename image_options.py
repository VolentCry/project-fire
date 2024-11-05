import cv2

# Открываем изображение карты
img = cv2.imread('map.png')

# Преобразуем изображение в формат HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

low_vegetation = cv2.inRange(hsv, (40, 100, 100), (80, 255, 255))  # зеленый цвет с низкой насыщенностью
forests = cv2.inRange(hsv, (40, 200, 100), (80, 255, 255))  # зеленый цвет с высокой насыщенностью
mountains = cv2.inRange(hsv, (10, 100, 100), (30, 255, 255))  # коричневый цвет
water = cv2.inRange(hsv, (100, 100, 100), (140, 255, 255))  # голубой цвет

result = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

result[low_vegetation > 0] = (128, 255, 128)  # светло-зеленый цвет
result[forests > 0] = (0, 128, 0)  # темно-зеленый цвет
result[mountains > 0] = (165, 42, 42)  # коричневый цвет
result[water > 0] = (0, 0, 255)  # голубой цвет

cv2.imwrite('result.png', result)