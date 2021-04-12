import cv2

from config.config import CALIBRATION_FILE_PATH, LAPTOP_CAMERA_INDEX
from infra.camera.OpenCvCalibrator import OpenCvCalibrator
from infra.camera.OpenCvWorldCamera import OpenCvWorldCamera

if __name__ == "__main__":
    calibrator = OpenCvCalibrator(CALIBRATION_FILE_PATH)
    camera = OpenCvWorldCamera(LAPTOP_CAMERA_INDEX, calibrator)
    should_continue = True
    images = []

    while should_continue:
        image = camera.take_world_image()
        cv2.imshow("image", image)
        k = cv2.waitKey(0)
        if k == 27:  # Esc key to stop
            break

        images.append(image)
        print(len(images))
        cv2.destroyAllWindows()

    cv2.destroyAllWindows()

    filename = "../../resources/test/puck/puck_configuration_{}.jpg"

    for index, image in enumerate(images):
        print(filename.format(index + 2))
        cv2.imwrite(filename.format(index + 2), image)

    print("Script done ...")
