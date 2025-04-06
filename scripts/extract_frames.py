# scripts/extract_frames.py
import cv2
import os
import random

VIDEO_PATH = "data/videos/v06.mp4"
OUTPUT_DIR = "data/images/train"
FRAME_COUNT = 50

os.makedirs(OUTPUT_DIR, exist_ok=True)
cap = cv2.VideoCapture(VIDEO_PATH)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
selected = sorted(random.sample(range(total_frames), FRAME_COUNT))

print(f"🎯 Extrayendo {FRAME_COUNT} frames aleatorios de {total_frames} frames...")

for idx, frame_id in enumerate(selected):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(f"{OUTPUT_DIR}/frame_{idx:03}.jpg", frame)

cap.release()
print(f"✅ Frames guardados en {OUTPUT_DIR}")
