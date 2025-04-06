from tensorboardX import SummaryWriter
import pandas as pd

log_dir = "runs/detect/train7_tensorboard"
csv_path = "runs/detect/train7/results.csv"

writer = SummaryWriter(log_dir)
df = pd.read_csv(csv_path)

for epoch, row in df.iterrows():
    for col in df.columns[1:]:  # skip 'epoch' column
        writer.add_scalar(col, row[col], epoch)

writer.close()
