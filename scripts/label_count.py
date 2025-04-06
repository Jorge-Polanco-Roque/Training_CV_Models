import os
from collections import Counter

# Cambia esta ruta si quieres analizar 'valid' o 'test'
label_dir = "/home/jupyter/yolo_football/data/football_custom/train/labels"

# Asegúrate que existe
if not os.path.exists(label_dir):
    raise Exception(f"Ruta no encontrada: {label_dir}")

# Contar clases
class_counts = Counter()

for file in os.listdir(label_dir):
    if file.endswith(".txt"):
        with open(os.path.join(label_dir, file), "r") as f:
            for line in f:
                if line.strip():  # evitar líneas vacías
                    class_id = int(line.strip().split()[0])
                    class_counts[class_id] += 1

# Etiquetas
names = ['ball', 'goalkeeper', 'player', 'referee']

# Mostrar resultados
print("\nDistribución de clases en 'train':")
for class_id, count in sorted(class_counts.items()):
    label_name = names[class_id] if class_id < len(names) else f"class_{class_id}"
    print(f"  {label_name:<12}: {count} instancias")
