import argparse
import numpy as np
import cv2 as cv


parser = argparse.ArgumentParser(description='Traditional Chinese Face Reading')
parser.add_argument('--video', '-v', type=str, default=0)
parser.add_argument('--scale', '-sc', type=float, default=1.0)
parser.add_argument('--face_detection_model', '-fd', type=str,
                    default=r"C:\Users\em\face_detection_yunet_2023mar.onnx")
parser.add_argument('--score_threshold', type=float, default=0.9)
parser.add_argument('--nms_threshold', type=float, default=0.3)
parser.add_argument('--top_k', type=int, default=5000)
args = parser.parse_args()


def get_brightness(crop, y1, y2, x1=0.3, x2=0.7):
    h, w = crop.shape[:2]
    roi = crop[int(h*y1):int(h*y2), int(w*x1):int(w*x2)]
    if roi.size == 0: return 128
    return np.mean(cv.cvtColor(roi, cv.COLOR_BGR2GRAY))


def wealth_house_scan(crop):
    b = get_brightness(crop, 0.48, 0.68)
    if b > 160:
        return ("Your nose is bright and full — the true mark of the Wealth Palace. You possess natural magnetism for money, "
                "decisiveness, courage, and bold talent. Your treasury (nose wings) is strong, and you both earn and keep wealth with ease. "
                "Age 41–50 will be your golden period. You are destined to rise high and live comfortably.")
    elif b > 130:
        return ("Your nose shows generous energy and warm heart. You spend freely and enjoy life, yet fortune returns to you. "
                "People trust and help you. Though you give much, you never truly lack — your path is blessed with flow and recovery.")
    elif b > 100:
        return ("You have a practical and thrifty nature. Your nostrils are hidden — a sign of one who knows how to save and protect wealth. "
                "You think deeply, plan wisely, and build slowly but surely. Middle age will reward your patience.")
    elif b > 80:
        return ("Your wealth flow is moderate. There may be worries or leaks between age 41–50. Avoid standing guarantee for others. "
                "Focus on stability, careful saving, and avoiding impulsive risks. With discipline, comfort is still possible.")
    else:
        return ("Your nose suggests current challenges in gathering and keeping wealth. Health may also need attention, especially the bridge. "
                "Avoid rash investments or helping others financially. This is a time for caution, healing, and quiet rebuilding.")


def career_house_scan(crop):
    b = get_brightness(crop, 0.05, 0.25)
    if b > 160:
        return ("Your forehead is high, broad, and luminous — the mark of a born leader. Heaven favors you with sharp intelligence, "
                "adaptability, and noble destiny. Success comes naturally in any field. Even if other features are modest, "
                "your career will shine brightly and bring both wealth and respect.")
    elif b > 130:
        return ("You have the strong, clear forehead of responsibility and achievement. Your thinking is structured and powerful. "
                "You are trusted in business and leadership. Your path is one of steady rise, honor, and lasting success.")
    elif b > 100:
        return ("Your forehead is kind and creative — rounded or M-shaped. You are artistic, supported by others, and blessed with helpful connections. "
                "Your success comes through talent, warmth, and noble friends. Longevity and happiness follow you.")
    elif b > 80:
        return ("Early life may have been difficult — low or uneven hairline suggests challenges from family or superiors. "
                "But after age 35, your fortune improves greatly. Patience now brings comfort later.")
    else:
        return ("Your forehead shows current obstacles in career and youth luck. There may be friction with authority or unstable beginnings. "
                "Avoid conflict. Focus on inner growth. With time and wisdom, difficulties will pass.")


def fortune_house_scan(crop):
    l = get_brightness(crop, 0.18, 0.30, 0.18, 0.45)
    r = get_brightness(crop, 0.18, 0.30, 0.55, 0.82)
    b = (l + r) / 2
    if b > 160:
        return ("Your eyebrows are thick, glossy, and beautifully shaped — the highest sign of the Palace of Longevity. "
                "You are loyal, intelligent, and surrounded by noble help. Middle age brings rank, wealth, and deep respect. "
                "Your relationships are harmonious and lasting.")
    elif b > 130:
        return ("Your eyebrows are strong and heroic — flat, dashing, or well-formed. You are righteous, courageous, and destined for recognition. "
                "Family is harmonious, marriage enduring, and your life path is one of power, honor, and long life.")
    elif b > 100:
        return ("You have gentle, kind, and artistic eyebrows — crescent, willow, or upward. People love and help you. "
                "Your heart is warm, your connections many. Happiness in love and friendship follows you naturally.")
    elif b > 80:
        return ("Your social luck has ups and downs. Eyebrows may be joined or irregular — showing strong will but some isolation. "
                "Success comes through perseverance. Choose friends carefully. In time, your effort will be rewarded.")
    else:
        return ("Currently, relationships or reputation face strain. Eyebrows appear sparse or scattered — suggesting loneliness or conflict. "
                "Avoid toxic company. Protect your health and peace. With awareness, this phase will pass.")


# ==================== Main ====================
def main():
    detector = cv.FaceDetectorYN.create(
        model=r"C:\Users\em\face_detection_yunet_2023mar.onnx",
        config="",
        input_size=(320, 320),
        score_threshold=args.score_threshold,
        nms_threshold=args.nms_threshold,
        top_k=args.top_k
    )


    cap = cv.VideoCapture(0 if str(args.video) == '0' else args.video)
    fw = int(cap.get(cv.CAP_PROP_FRAME_WIDTH) * args.scale)
    fh = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT) * args.scale)
    detector.setInputSize((fw, fh))


    print("\n" + "═"*70)
    print("        TRADITIONAL CHINESE FACE READING 相面大师")
    print("═"*70)
    print("Align the colored dots on your nose, forehead, and eyebrows")
    print("→ Press SPACEBAR to receive your complete reading\n")


    while True:
        ret, frame = cap.read()
        if not ret: break
        frame = cv.resize(frame, (fw, fh))
        faces = detector.detect(frame)
        faces = faces[1] if faces is not None else None


        if faces is not None and len(faces) > 0:
            x, y, w, h = map(int, faces[0][:4])


            #markers
            cv.circle(frame, (x + w//2, y + int(h*0.60)), 11, (90, 90, 255), -1)
            cv.putText(frame, "Wealth", (x + w//2 + 15, y + int(h*0.60) + 8),
                       cv.FONT_HERSHEY_SIMPLEX, 0.6, (130, 130, 255), 1)


            cv.circle(frame, (x + w//2, y + int(h*0.10)), 11, (100, 255, 255), -1)
            cv.putText(frame, "Career", (x + w//2 + 15, y + int(h*0.10) + 8),
                       cv.FONT_HERSHEY_SIMPLEX, 0.6, (140, 255, 255), 1)


            cv.circle(frame, (x + int(w*0.32), y + int(h*0.23)), 11, (80, 180, 255), -1)
            cv.circle(frame, (x + int(w*0.68), y + int(h*0.23)), 11, (80, 180, 255), -1)
            cv.putText(frame, "Fortune", (x + w//2 - 60, y + int(h*0.23) - 15),
                       cv.FONT_HERSHEY_SIMPLEX, 0.65, (110, 200, 255), 1)


            if cv.waitKey(1) & 0xFF == 32:  # SPACEBAR
                crop = frame[y:y+h, x:x+w]
                if crop.size > 0:
                    print("\n" + "═"*80)
                    print("                    YOUR FACE READING")
                    print("═"*80)
                    print("\n【 WEALTH HOUSE – NOSE 】")
                    print(wealth_house_scan(crop))
                    print("\n【 CAREER HOUSE – FOREHEAD 】")
                    print(career_house_scan(crop))
                    print("\n【 FORTUNE HOUSE – EYEBROWS 】")
                    print(fortune_house_scan(crop))
                    print("\n" + "═"*80 + "\n")


        cv.putText(frame, "Align markers || Press SPACE for your reading || q = quit",
                   (15, frame.shape[0]-18), cv.FONT_HERSHEY_SIMPLEX, 0.62, (220, 220, 220), 2)
        cv.imshow("Chinese Face Reading AI", frame)


        if cv.waitKey(1) == ord('q'):
            break


    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
