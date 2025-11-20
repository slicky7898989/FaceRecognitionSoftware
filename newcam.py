import argparse
import numpy as np
import cv2 as cv

def str2bool(v):
    if v.lower() in ['on', 'yes', 'true', 'y', 't']:
        return True
    elif v.lower() in ['off', 'no', 'false', 'n', 'f']:
        return False
    else:
        raise NotImplementedError

parser = argparse.ArgumentParser()
parser.add_argument('--video', '-v', type=str, help='Path to the input video.')
parser.add_argument('--scale', '-sc', type=float, default=1.0)
parser.add_argument('--face_detection_model', '-fd', type=str, default='face_detection_yunet_2021dec.onnx')
parser.add_argument('--score_threshold', type=float, default=0.9)
parser.add_argument('--nms_threshold', type=float, default=0.3)
parser.add_argument('--top_k', type=int, default=5000)
parser.add_argument('--save', '-s', type=str2bool, default=False)
args = parser.parse_args()


# ----------------------------------------------------------------------
# SIMPLE YES/NO WEALTH DECISION
# ----------------------------------------------------------------------
def classify_wealth_face(face):
    coords = face[:-1].astype(np.int32)

    x, y, w, h = coords[0], coords[1], coords[2], coords[3]
    rx, ry = coords[4], coords[5]
    lx, ly = coords[6], coords[7]
    mrx, mry = coords[10], coords[11]
    mlx, mly = coords[12], coords[13]

    # Very simple "Feng Shui" rules:
    forehead_height = min(ry, ly) - y
    cheek_width = w
    mouth_width = abs(mrx - mlx)

    # RULES FOR YES/NO
    good_forehead = forehead_height > 0.22 * h
    good_cheeks = cheek_width > 0.9 * h
    good_mouth = mouth_width < 0.6 * w

    if good_forehead and good_cheeks and good_mouth:
        return "Wealth House"
    else:
        return "Not Wealth House"


def visualize(frame, faces, fps, thickness=2):
    if faces[1] is not None:
        for idx, face in enumerate(faces[1]):
            coords = face[:-1].astype(np.int32)

            x, y, w, h = coords[0], coords[1], coords[2], coords[3]

            # Classification only
            label = classify_wealth_face(face)

            # Show ONLY the label.
            cv.putText(frame, label, (x, y - 10),
                       cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)



# ----------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------
if __name__ == '__main__':
    detector = cv.FaceDetectorYN.create(
        model=r"C:\Users\Samba Angeles\Downloads\face_detection_yunet_2023mar.onnx",
        config="",
        input_size=(320, 320),
        score_threshold=args.score_threshold,
        nms_threshold=args.nms_threshold,
        top_k=args.top_k
    )

    tm = cv.TickMeter()

    deviceId = args.video if args.video else 0
    cap = cv.VideoCapture(deviceId)
    frameWidth = int(cap.get(cv.CAP_PROP_FRAME_WIDTH) * args.scale)
    frameHeight = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT) * args.scale)
    detector.setInputSize([frameWidth, frameHeight])

    while cv.waitKey(1) < 0:
        hasFrame, frame = cap.read()
        if not hasFrame:
            print("No frames grabbed!")
            break

        frame = cv.resize(frame, (frameWidth, frameHeight))

        tm.start()
        faces = detector.detect(frame)
        tm.stop()

        visualize(frame, faces, tm.getFPS())
        cv.imshow("Live", frame)

    cv.destroyAllWindows()
