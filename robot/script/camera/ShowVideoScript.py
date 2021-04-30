import cv2

CAMERA_INDEX = 0
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

    def _close_capture(self):
        self._capture.release()


if __name__ == "__main__":
    camera = OpenCvEmbeddedCamera(CAMERA_INDEX)
    while True:
        image = camera.take_image()
        cv2.imshow("image", image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()
