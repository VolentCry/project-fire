from PIL import Image
import os

def crop_and_split_image(input_image_path, output_folder):
    # Открываем изображение
    image = Image.open(input_image_path)
    
    # Обрезаем изображение до размеров 1000x1000
    cropped_image = image.crop((0, 0, 500, 500))
    
    # Создаем папку для сохранения изображений, если она не существует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cropped_image.save(output_folder)

    # # Разбиваем изображение на блоки 10x10
    # block_size = 10
    # for i in range(0, 1000, block_size):
    #     for j in range(0, 1000, block_size):
    #         # Определяем границы блока
    #         box = (j, i, j + block_size, i + block_size)
    #         # Обрезаем блок
    #         block = cropped_image.crop(box)
    #         # Сохраняем блок
    #         block.save(os.path.join(output_folder, f'block_{i//block_size}_{j//block_size}.png'))

# Пример использования
input_image_path = 'images\\kotik.jpg'  # Укажите путь к вашему изображению
output_folder = 'images\\test'  # Укажите папку для сохранения блоков
crop_and_split_image(input_image_path, output_folder)

