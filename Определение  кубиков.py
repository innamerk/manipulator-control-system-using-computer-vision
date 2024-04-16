import sys
import glob
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

# матрица для вывода нескольких рисунков   
fig, axs = plt.subplots(3, 6, figsize=(9, 3)) 
strok = 0
stolb = 0

# file = 'WIN_20230407_10_19_28_Pro.jpg' # имя файла, который будем анализировать
# img = cv.imread(file)

for file in glob.glob("D:/University/Maks/ABB120PythonScript/*.jpg"):
    img = cv.imread(file)

    # hsv - Hue, Saturation, Value — тон, насыщенность, значение
    # меняем цветовую модель с BGR на HSV
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)        # меняем цветовую модель с BGR на HSV

    # Создание маски на изображение, чтобы исключить ложные объекты
    hsv_min = np.array((55, 5, 100), np.uint8)        # нижняя граница 
    hsv_max = np.array((167, 90, 220), np.uint8)    # верхняя граница
    mask = cv.inRange(hsv, hsv_min, hsv_max)        # применяем цветовой фильтр

    # меняем цветовую модель с BGR на RGB для привычного отображения
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    # ищем все контуры
    contours, hierarchy = cv.findContours(mask.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # перебираем все найденные контуры в цикле и ищем прямоугольники
    for cnt in contours:
        
        # нахождение прямоугольника минимальной площади
        # на выход - ( center (x,y), (width, height), angle of rotation )
        rect = cv.minAreaRect(cnt)

        # проверка на нахождение прямоугольника в рабочем поле
        if rect[0][0] < 620 and rect[0][0] > 70 and rect[0][1] < 420 and rect[0][0] > 20: # можно положить бумагу на все поле видимости камеры чтобы исключить фон 

            # проверка на длины сторон (чтобы был только квадрат)
            if 0.8*rect[1][1] < rect[1][0] < 1.2*rect[1][1]: 
                box = cv.boxPoints(rect)            # поиск четырех вершин прямоугольника
                box = np.int0(box)                  # округление координат вершин
                area = int(rect[1][0]*rect[1][1])   # вычисление площади

                # отфильтровываем прямоугольники по площади
                if 1000 > area > 500:
                    cv.drawContours(img,[box],0,(255,0,0),2)

                    # Определение координат центра кубика
                    X = int(rect[0][0])
                    Y = int(rect[0][1])
                    print(box)                      # вывод массива координат углов
                    print("Square:", area)          # вывод площади
                    print("Center of Cube:", X, Y)  # вывод центра
                    print("Angle:", int(rect[2]))
                    print("")  
    
    if stolb == 6:
        strok += 1
        stolb = 0
    elif stolb < 6:
        axs[strok,stolb].imshow(img)
        axs[strok,stolb].set_title(str(file[38:]))
        stolb += 1
        axs[strok,stolb].imshow(mask)
        stolb += 1

# with open('example.txt', 'w') as f:
#     f.write("X_center: " + str(X) + " " + "Y_center: " + str(Y))

plt.show()