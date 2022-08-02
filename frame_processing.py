from start_data import *
import cv2
class FrameProccessing():
    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.faceCascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')
        path1 = "models/ESPCN_x2.pb"
        self.sr = cv2.dnn_superres.DnnSuperResImpl_create()
        self.sr.readModel(path1)
        self.sr.setModel("espcn", 2)
        self.segments = []

    def get_camera_frame(self):
        _r_, frame = self.cap.read()
        return frame

    def image_sizing(self, frame):
        frame = cv2.resize(frame, (1200, 900))
        return frame

    def image_filtering(self, frame):
        kernel = np.array([[0, -1, 0],
                          [-1, 5, -1],
                          [0, -1, 0]])
        frame = cv2.filter2D(src=frame, ddepth=-5, kernel=kernel)

        look_up_table = np.empty((1, 256), np.uint8)
        for i in range(256):
            look_up_table[0, i] = np.clip(pow(i / 255.0, 1.7) * 255.0, 0, 255)
        frame = cv2.LUT(frame, look_up_table)

        cv2.normalize(frame, frame, 255, 0, cv2.NORM_MINMAX, cv2.CV_8U)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame

    def face_detection(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(20, 20)
        )
        return faces


    def face_segmentation(self, faces, segment_size):
        _w_ = 0
        _h_ = 0
        self.segments.clear()
        for (y, x, w, h) in faces:
            for i in [4, 3, 2, 1]:
                print(i)
                if w > (segment_size * i) or h > (segment_size * i):
                    _w_ = w // i
                    _h_ = h // i

                    self.segments.append((x, y, w // i, h // i))
                    if i >= 2:
                        self.segments.append((x, y + _h_, _w_, _h_))
                        self.segments.append((x + _w_, y + _h_, _w_, _h_))
                        self.segments.append((x + _w_, y, _w_, _h_))
                    if i >= 3:
                        self.segments.append((x, y + _h_ * 2, _w_, _h_))
                        self.segments.append((x + _w_, y + _h_ * 2, _w_, _h_))
                        self.segments.append((x + _w_ * 2, y + _h_ * 2, _w_, _h_))
                        self.segments.append((x + _w_ * 2, y + _h_, _w_, _h_))
                        self.segments.append((x + _w_ * 2, y, _w_, _h_))
                    if i == 4:
                        self.segments.append((x, y + _h_ * 3, _w_, _h_))
                        self.segments.append((x + _w_, y + _h_ * 3, _w_, _h_))
                        self.segments.append((x + _w_ * 2, y + _h_ * 3, _w_, _h_))
                        self.segments.append((x + _w_ * 3, y + _h_ * 3, _w_, _h_))
                        self.segments.append((x + _w_ * 3, y + _h_ * 2, _w_, _h_))
                        self.segments.append((x + _w_ * 3, y + _h_, _w_, _h_))
                        self.segments.append((x + _w_ * 3, y, _w_, _h_))
                    break
        return self.segments

    def face_upscale(self, frame, segments, iterations):
        if len(segments) > 0:
            for (x, y, w, h) in segments:
                frame_face = frame[x:x + w, y:y + h]

                if len(frame_face) > 0:
                    for i in range(iterations):

                        frame_face = self.sr.upsample(frame_face)
                        frame_face = cv2.medianBlur(frame_face, 3)
                        frame_face = cv2.resize(frame_face, (frame_face.shape[1] // 2, frame_face.shape[0] // 2), cv2.INTER_AREA)
                    frame[x:x + w, y:y + h] = frame_face
        return frame
