import os
import shutil

# IDs de las clases que queremos reforzar
target_classes = {"0", "3"}  # ball y referee

# Paths absolutos desde donde estás ejecutando
base_dir = "../data/football_custom"
images_dir = os.path.join(base_dir, "train/images")
labels_dir = os.path.join(base_dir, "train/labels")

# Nuevos paths focalizados
focus_root = "../data/football_custom_focus/train"
focus_img_dir = os.path.join(focus_root, "images")
focus_lbl_dir = os.path.join(focus_root, "labels")
os.makedirs(focus_img_dir, exist_ok=True)
os.makedirs(focus_lbl_dir, exist_ok=True)

for lbl_file in os.listdir(labels_dir):
    lbl_path = os.path.join(labels_dir, lbl_file)

    with open(lbl_path, "r") as f:
        lines = f.readlines()

    # Ver si alguna línea contiene una clase de interés
    if any(line.strip().split()[0] in target_classes for line in lines):
        shutil.copy(lbl_path, os.path.join(focus_lbl_dir, lbl_file))
        img_file = lbl_file.replace(".txt", ".jpg")
        shutil.copy(os.path.join(images_dir, img_file), os.path.join(focus_img_dir, img_file))

print("✅ Dataset focalizado creado.")
