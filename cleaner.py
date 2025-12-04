import pandas as pd
import sklearn
from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer


filename = "bandsEE.jsonl"

df = pd.read_json(filename, lines=True)
cleandf = df.copy()

# Clean the genre column
cleandf["genre"] = cleandf["genre"].str.replace(" Metal", "")
cleandf["genre"] = cleandf["genre"].str.replace(" (early)", "")
cleandf["genre"] = cleandf["genre"].str.replace(" (later)", "")
cleandf["genre"] = cleandf["genre"].str.replace(";", "/")

cleandf["genre"] = cleandf["genre"].str.split(r"\s*/\s*")

# Vectorize genres
mlb = MultiLabelBinarizer()
genres = mlb.fit_transform(cleandf['genre'])
genres = pd.DataFrame(genres, columns=mlb.classes_, index=cleandf.index)

cleandf = cleandf.drop('genre',axis = 1)
cleandf = cleandf.join(genres)

# Set year of formation as the year of the first release for bands without a year of formation
cleandf["firstrelease"] = cleandf["releases"].apply(lambda rels: rels[0] if len(rels) > 0 else None)
mask = cleandf["formed"] == "N/A"
cleandf.loc[mask, "formed"] = cleandf.loc[mask, "firstrelease"]