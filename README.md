# Notas

## Mejor modelo hasta ahora: /home/jupyter/yolo_football/data/runs/detect/train_ball_augmented
## Ruta de outputs: outputs/v06_output_ball_augmented.mp4
## GPUs tracking: watch -n 1 nvidia-smi

## JTBD:

## Siguientes pasos inmediatos:
* Reentrenar con los nuevos datos X_321 - No fue perfecto
* Reentrenar con data augmentation con enfoque al balón
* Probar de los otros proyectos descargados si funcionan los .pt files

### Limpiar proyecto:
* Limpiar los outputs, los tengo en varios lados: "outputs", "runs", "data/runs"
* Limpiar datasets, los tengo en varios lados: "data", "datasets"
* Los modelos base los tengo en varios lados: "data", "ultralytics

### Next Steps:
* Que detecte correctamente: balón, referi, jugador, y portero
* Que distinga entre los diferentes equipos
* Que detecte en qué zona de la cancha están
* Estadísticas como: conteo de pases por equipo, % de posesión del balón
* Mapas de calor


## Cómo usar el proyecto?:
* Llamado desde terminal (acá se probó con el modelo world, pero no tuvo ta buenos resultados): 
yolo predict task=detect model=ultralytics/yolo-world/yolov8m-world.pt \
    conf=0.3 source=data/videos/v06.mp4 classes="soccer player, referee, football"

* Reentrenamiento (desde yolo_football):
yolo task=detect mode=train \
  model=data/yolo11l.pt \
  data=data/football_custom/data.yaml \
  epochs=200 \
  imgsz=640 \
  batch=6 \
  workers=2 \
  amp=False \
  cls=2.0 \
  project=data/runs/detect \
  name=train_cls_weighted

* Reentrenamiento aumentado en la clase "balón" (acá se entrenó sobre un modelo ya fine-tunneado):
yolo task=detect mode=train \
  model=/home/jupyter/yolo_football/data/runs/detect/train_focus_finetune_ball_ref/weights/best.pt \
  data=/home/jupyter/yolo_football/data/football_custom_focus/data.yaml \
  epochs=100 imgsz=640 batch=6 workers=2 amp=False \
  project=/home/jupyter/yolo_football/data/runs/detect \
  name=train_ball_augmented \
  hsv_h=0.1 hsv_s=0.8 hsv_v=0.4 translate=0.2 scale=0.8 shear=5 flipud=0.2 fliplr=0.8 \
  mosaic=1.0 mixup=0.3 erasing=0.5


* Tensorboard: tensorboard --logdir runs/detect/train7_tensorboard --port=6006

* Probar el modelo (mejor usar el siguiente): 
#yolo predict model=runs/detect/train_tb2/weights/best.pt source=football_custom/videos/v06.mp4 save=True

#yolo predict \
  #model=data/runs/detect/train_tb2/weights/best.pt \
  #source=data/football_custom/videos/v06.mp4 \
  #save=True

* Probar modelo (modificar parámetros al modelo más reciente): 
python scripts/video_infer.py \
  --weights data/runs/detect/train_ball_augmented/weights/best.pt \
  --source data/football_custom/videos/v06.mp4 \
  --save-path outputs/v06_output_ball_augmented.mp4

----

* Último reentrenamiento:
(.venv) (base) jupyter@cv-maz-v2:~/yolo_football$ yolo task=detect mode=train   model=/home/jupyter/yolo_football/data/runs/detect/train_X321_yolo11l_optimized/weights/best.pt   data=/home/jupyter/yolo_football/data/X_321/data.yaml   epochs=50 imgsz=512 batch=4 workers=4   amp=False cache=True   hsv_h=0.05 hsv_s=0.9 hsv_v=0.6   degrees=10 translate=0.3 scale=0.9 shear=2.0 flipud=0.1 fliplr=0.8   mosaic=0.3 auto_augment=randaugment erasing=0.4 copy_paste=0.1 mixup=0.1   project=/home/jupyter/yolo_football/data/runs/detect   name=train_ball_aggressive_aug


* Crear video con los modelos:
python scripts/video_infer.py \
  --weights data/runs/detect/train_ball_aggressive_aug/weights/best.pt \
  --source data/football_custom/videos/v06.mp4 \
  --save-path outputs/v06_output_ball_aggressive_aug.mp4
