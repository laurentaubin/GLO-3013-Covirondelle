import cv2

CAMERA_INDEX = 1
EMBEDDED_CAMERA_IMAGE_SIZE = (640, 480)


class OpenCvEmbeddedCamera:
    def __init__(
        self,
        camera_index: int,
    ):
        self._camera_index = camera_index
        self._capture = None
        self._open_capture()

    def take_image(self):
        return self._get_camera_frame()

    def _get_camera_frame(self):
        opened_successfully, current_frame = self._capture.read()
        return current_frame

    def _open_capture(self):
        self._capture = cv2.VideoCapture(self._camera_index)
        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, EMBEDDED_CAMERA_IMAGE_SIZE[0])
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, EMBEDDED_CAMERA_IMAGE_SIZE[1])
        self._capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def _close_capture(self):
        self._capture.release()


if __name__ == "__main__":
    camera = OpenCvEmbeddedCamera(CAMERA_INDEX)
    should_continue = True
    images = []

    while should_continue:
        image = camera.take_image()
        cv2.imshow("image", image)
        k = cv2.waitKey(33)
        if k == 27:  # Esc key to stop
            break
        elif k == 32:
            images.append(image)
        else:
            continue
        cv2.destroyAllWindows()
    cv2.destroyAllWindows()

    filename = "puck-ajustement/image-{}.jpg"

    for index, image in enumerate(images):
        cv2.imwrite(filename.format(index), image)

    print("Script done ...")
