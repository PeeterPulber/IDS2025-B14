import pandas as pd
import sklearn
from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer


filename = "bandsEE.jsonl"

df = pd.read_json(filename, lines=True)
cleandf = df.copy()

#for r in cleandf["genre"]:

cleandf["genre"] = cleandf["genre"].str.replace(" Metal", "")
cleandf["genre"] = cleandf["genre"].str.replace("(early)", "")
cleandf["genre"] = cleandf["genre"].str.replace("(later)", "")
cleandf["genre"] = cleandf["genre"].str.replace(";", "/")

cleandf["genre"] = cleandf["genre"].str.split("/")

mlb = MultiLabelBinarizer()
genres = mlb.fit_transform(cleandf['genre'])

print(genres)
