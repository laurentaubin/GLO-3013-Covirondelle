import cv2

from domain.vision.exception.PuckNotFoundException import PuckNotFoundException
from infra.vision.OpenCvPuckDetector import OpenCvPuckDetector
from infra.vision.OpenCvStartingZoneLineDetector import OpenCvStartingZoneLineDetector

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
        self._capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self._capture.set(cv2.CAP_PROP_BRIGHTNESS, 100)
        self._capture.set(cv2.CAP_PROP_SATURATION, 30)
        self._capture.set(cv2.CAP_PROP_CONTRAST, 20)
        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, EMBEDDED_CAMERA_IMAGE_SIZE[0])
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, EMBEDDED_CAMERA_IMAGE_SIZE[1])

    def _close_capture(self):
        self._capture.release()


if __name__ == "__main__":
    camera = OpenCvEmbeddedCamera(1)
    puck_detector = OpenCvPuckDetector()
    line_detector = OpenCvStartingZoneLineDetector()
    # template_matching_detector = TemplateMatchingPuckDetector()
    should_continue = True
    images = []

    while True:
        # image = camera.take_image()
        # if True:
        #     try:
        #         # letters = command_panel_letters_extractor.extract_letters_from_image(
        #         #     image
        #         # )
        #         # position = corner_detector.detect_inferior_corner(image)
        #         position = puck_detector.detect(image, Color.WHITE)
        #         cv2.circle(
        #             image,
        #             (
        #                 int(position.get_x_coordinate()),
        #                 int(position.get_y_coordinate()),
        #             ),
        #             70,
        #             (0, 255, 0),
        #             2, )
        #         print(position.to_tuple())
        #     except PuckNotFoundException:
        #         print("puck not found")
        #         pass
        # cv2.imshow("fsd", image)
        # k = cv2.waitKey(1)
        # if k == 27:
        #     break

        if True:
            image = camera.take_image()

            try:
                # letters = command_panel_letters_extractor.extract_letters_from_image(
                #     image
                # )
                # position = corner_detector.detect_inferior_corner(image)
                position = line_detector.detect(image)
                cv2.circle(
                    image,
                    (
                        int(position.get_x_coordinate()),
                        int(position.get_y_coordinate()),
                    ),
                    20,
                    (0, 255, 0),
                    2,
                )
                print(position.to_tuple())
            except PuckNotFoundException:
                print("puck not found")
                pass
        cv2.imshow("fsd", image)
        k = cv2.waitKey(1)
        if k == 27:
            break
        elif k == 32:
            images.append(image)
        else:
            continue
        cv2.destroyAllWindows()
    cv2.destroyAllWindows()

    filename = "new_color/image-{}.jpg"

    for index, image in enumerate(images):
        cv2.imwrite(filename.format(index), image)

    print("Script done ...")
