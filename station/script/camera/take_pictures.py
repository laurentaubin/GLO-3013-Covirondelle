import cv2

from config.config import CALIBRATION_FILE_PATH, LAPTOP_CAMERA_INDEX
from infra.camera.OpenCvCalibrator import OpenCvCalibrator
from infra.camera.OpenCvWorldCamera import OpenCvWorldCamera

if __name__ == "__main__":
    calibrator = OpenCvCalibrator(CALIBRATION_FILE_PATH)
    camera = OpenCvWorldCamera(0, calibrator)
    should_continue = True
    images = []

    while should_continue:
        image = camera.take_world_image()
        cv2.imshow("image", image)
        k = cv2.waitKey(1)
        if k == 32:
            images.append(image)
            print("take pic")

        if k == 27:  # Esc key to stop
            break

    cv2.destroyAllWindows()

    filename = "../../resources/camera-config/image_{}.jpg"

    for index, image in enumerate(images):
        print(filename.format(index))
        cv2.imwrite(filename.format(index), image)

    print("Script done ...")
