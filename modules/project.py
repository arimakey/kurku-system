import math
import cv2
import os

def initialize_project(project_name):
    max_size = (128,128)

    img_path = "./temp.jpg"
    img = cv2.imread(img_path)

    x_size, y_size, _ = img.shape

    amount_x = math.ceil(x_size / max_size[0])
    amount_y = math.ceil(y_size / max_size[1])

    print(x_size, y_size)
    print(amount_x, amount_y)

    cv2.imshow('img', img)
    cv2.waitKey(0)

    cv2.destroyAllWindows()

    create_directories(project_name, amount_x, amount_y)





def create_directories(project_name, amount_x, amount_y):
    if os.path.exists('./' + project_name):
        print("Hubo un error inesperado, el proyecto ya existe")
        return

    os.mkdir('./' + project_name)

    for x in range(amount_x):
        for y in range(amount_y):
            img_current_path = './' + project_name + '/' + str(x) + str(y)
            os.mkdir(img_current_path)



#            img_crop = img[x * max_size[0]: (x + 1) * max_size[0], y * max_size[1]: (y + 1) * max_size[1]]
#            img_current_path = './' + project_name + '/' + str(x) + str(y)
#            os.mkdir(img_current_path)
#            cv2.imwrite(img_current_path + '/imagen.jpg', img_crop)