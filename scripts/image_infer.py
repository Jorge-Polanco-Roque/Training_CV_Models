# scripts/image_infer.py
from ultralytics import YOLO
import cv2

print("🚀 Cargando modelo...")
model = YOLO("ultralytics/yolo-world/yolov8s-worldv2.pt").to("cpu")  # también puedes probar sin .to("cpu")

print("🖼️ Cargando imagen...")
img = cv2.imread("data/images/frame0.jpg")

print("🔍 Corriendo inferencia...")
results = model.predict(img, conf=0.3, imgsz=320)[0]

print(f"✅ Detecciones: {len(results.boxes)} objetos encontrados.")
for box in results.boxes:
    cls_id = int(box.cls[0])
    conf = float(box.conf[0])
    print(f"📦 Clase {results.names[cls_id]} con confianza {conf:.2f}")
