from pandas import DataFrame
from os.path import join, exists
from os import makedirs, listdir
import pandas as pd

df_all = DataFrame()


root_dir = r"D:\calisma\projeler\tripadvisor\data\Bathroom"

classess = ["good", "bad"]

for cls in classess:
    folder = join(root_dir, cls)

    files = listdir(folder)  # all files in root folder

    pictures = [join(folder, file) for file in files if file.endswith(".jpg")] # images

    label = 1 if cls == "good" else 0

    labels = [label for _ in range(len(pictures))]

    df = DataFrame({"Image":pictures, "Label": labels}, columns=["Image", "Label"])

    df.shape

    df.head()

    df_all = pd.concat([df_all, df])

    # df_all.to_excel(join(root_dir, "Bothroom_data.xlsx"))
    df_all.to_feather(join(root_dir, "Bothroom_data.feather"))

a = 5


