import pandas as pd
import re
from datetime import date
from sklearn.preprocessing import MultiLabelBinarizer

def parse_years(r):
    # Bands are assumed to have been active during years when they released music
    activity = set(r["releases"])
    cleaned = r["years"]

    if cleaned != "N/A" and cleaned != "?":
        # Get rid of text in parentheses
        cleaned = re.sub(r"\s\(.*\)", "", cleaned)
        cleaned = cleaned.split(",")
        # Periods of activity
        for p in cleaned:
            p = p.strip().split("-")
            # Extract years in each period
            if len(p) == 1: # One year
                if p[0].isdigit():
                    activity.add(p[0])
                continue
            elif p[0] == "?" and p[1] == "?":
                continue
            elif p[0] == "?":
                activity.add(p[1])
                continue
            elif p[1] == "?":
                activity.add(p[0])
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
mlb_genre = MultiLabelBinarizer()
genres = mlb_genre.fit_transform(cleandf["genre"])
genres = pd.DataFrame(genres, columns=[f"genre_{g}" for g in mlb_genre.classes_], index=cleandf.index)

cleandf = cleandf.drop("genre",axis = 1)
cleandf = cleandf.join(genres)

# Set year of formation as the year of the first release for bands without a year of formation
cleandf["firstrelease"] = cleandf["releases"].apply(lambda rels: rels[0] if len(rels) > 0 else None)
mask = cleandf["formed"] == "N/A"
cleandf.loc[mask, "formed"] = cleandf.loc[mask, "firstrelease"]
# Drop bands for which there is no information about their period of activity
cleandf = cleandf.dropna(subset=["formed"])

# Clean the years string
cleandf["years"] = cleandf.apply(parse_years, axis=1)

# Vectorize years of activity
mlb_years = MultiLabelBinarizer()
years = mlb_years.fit_transform(cleandf["years"])
years = pd.DataFrame(years, columns=[f"active_{y}" for y in mlb_years.classes_], index=cleandf.index)
cleandf = cleandf.drop("years",axis = 1)
cleandf = cleandf.join(years)

# Vectorize releases
mlb_releases = MultiLabelBinarizer()
releases = mlb_releases.fit_transform(cleandf["releases"])
releases = pd.DataFrame(releases, columns=[f"release_{y}" for y in mlb_releases.classes_], index=cleandf.index)
cleandf = cleandf.drop("releases",axis = 1)
cleandf = cleandf.join(releases)

df.to_csv("cleaned.csv", index=False)