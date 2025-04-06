import cv2
import os
import argparse
from ultralytics import YOLO

# --- Argumentos desde CLI ---
parser = argparse.ArgumentParser()
parser.add_argument('--weights', type=str, required=True, help="Ruta al modelo YOLO")
parser.add_argument('--source', type=str, required=True, help="Ruta al video de entrada")
parser.add_argument('--save-path', type=str, required=True, help="Ruta de salida para el video")
args = parser.parse_args()

MODEL_PATH = args.weights
VIDEO_PATH = args.source
OUTPUT_PATH = args.save_path

# --- Parámetros de inferencia ---
CONF = 0.05
FRAME_INTERVAL = 1
MAX_FRAMES = 3000

# --- Cargar modelo YOLO ---
print("🚀 Cargando modelo YOLO en CPU...")
model = YOLO(MODEL_PATH).to("cpu")

# --- Abrir video ---
print("🎞️ Abriendo video...")
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise Exception(f"No se pudo abrir el video: {VIDEO_PATH}")

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"📏 Resolución: {width}x{height} | 🎥 FPS: {fps:.2f} | 🧾 Total frames: {total_frames}")

# --- Crear carpeta de salida si no existe ---
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (width, height))

# --- Procesamiento frame por frame ---
frame_id = 0
written = 0
print("🔍 Iniciando procesamiento...")

while frame_id < MAX_FRAMES:
    ret, frame = cap.read()
    if not ret:
        print("✅ Fin del video o lectura.")
        break

    if frame_id % FRAME_INTERVAL == 0:
        print(f"🧠 Frame {frame_id}: corriendo inferencia...")
        results = model.predict(frame, conf=CONF, imgsz=640, verbose=False)[0]

        if results.boxes is not None:
            print(f"📦 {len(results.boxes)} objetos detectados")
            for box in results.boxes:
                cls_id = int(box.cls[0])
                conf_score = float(box.conf[0])
                label = f"{results.names[cls_id]} {conf_score:.2f}"
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            print("📭 Sin detecciones")

    out.write(frame)
    written += 1
    frame_id += 1

cap.release()
out.release()

print(f"✅ Proceso finalizado. 🎥 Video guardado en: {OUTPUT_PATH}")
print(f"📝 Total de frames procesados: {frame_id} | Frames escritos: {written}")
