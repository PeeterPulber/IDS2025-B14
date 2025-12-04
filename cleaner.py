import pandas as pd
import sklearn
import re
from datetime import date
from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer

def parse_years(r):
    # Bands are assumed to have been active during years when they released music
    activity = set(r["releases"])
    cleaned = r["years"]

    if cleaned != "N/A" and cleaned != "?":
        # Get rid of text in parentheses
        cleaned = re.sub(r"\s\(.*\)", "", cleaned)
        cleaned = cleaned.replace("?", "").split(",")
        # Periods of activity

        for p in cleaned:
            p = p.strip().split("-")
            # Extract years in each period
            if len(p) == 1: # One year
                if p[0].isdigit():
                    activity.add(int(p[0]))
                continue
            elif p[0] == "" and p[1] == "":
                continue
            elif p[0] == "":
                activity.add(int(p[1]))
                continue
            elif p[1] == "":
                activity.add(int(p[0]))
                continue
            elif p[1] == "present":
                end = date.today().year
                start = int(p[0])
            else:
                end = int(p[1])
                start = int(p[0])
            # Add years to activity set
            for year in range(start, end+1):
                activity.add(str(year))

    return activity

filename = "bandsEE.jsonl"

df = pd.read_json(filename, lines=True)
cleandf = df.copy()

# Clean the genre column
cleandf["genre"] = cleandf["genre"].str.replace(" Metal", "")
cleandf["genre"] = cleandf["genre"].str.replace(" (early)", "")
cleandf["genre"] = cleandf["genre"].str.replace(" (later)", "")
cleandf["genre"] = cleandf["genre"].str.replace(";", "/")
# Split genres at "/" and remove any neighbouring spaces
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
# Drop bands for which there is no information about their period of activity
cleandf = cleandf.dropna(subset=["formed"])

# Clean the years string
cleandf["years"] = cleandf.apply(parse_years, axis=1)

print(cleandf["years"])