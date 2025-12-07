import pandas as pd
import re
from datetime import date
from sklearn.preprocessing import MultiLabelBinarizer

def parse_years(r):
    # Bands are assumed to have been active during years when they released music
    activity = set(r["releases"])
    cleaned = r["years"]

    if cleaned != "N/A" and cleaned != "?":
        cleaned = cleaned.split(",")

        # Periods of activity
        for p in cleaned:
            # Periods during which the band used a different name are excluded
            if "(" in p:
                continue
            p = p.strip().split("-")
            # Extract years in each period
            if len(p) == 1: # One year
                if p[0].isdigit():
                    activity.add(p[0])
                continue
            elif p[0] == "?" and p[1] == "?": # Unknown years
                continue
            elif p[0] == "?": # Unknown start year
                activity.add(p[1])
                continue
            elif p[1] == "?": # Unknown end year
                activity.add(p[0])
                continue
            elif p[1] == "present": # Band still active
                end = date.today().year
                start = int(p[0])
            else: # Start and end year are known
                end = int(p[1])
                start = int(p[0])
            # Add years to activity set
            for year in range(start, end+1):
                activity.add(str(year))

    return activity

filenames = ["bandsEE.jsonl", "bandsLV.jsonl", "bandsFI.jsonl"]

for filename in filenames:
    df = pd.read_json(filename, lines=True)
    cleandf = df.copy()

    # Clean the genre column
    cleandf["genre"] = cleandf["genre"].str.replace(" Metal", "")
    cleandf["genre"] = cleandf["genre"].str.replace(r"\s\([^)]*\)", "", regex=True) # Remove parentheses
    cleandf["genre"] = cleandf["genre"].str.replace(" with ", "/")
    cleandf["genre"] = cleandf["genre"].str.replace(" influences", "")
    cleandf["genre"] = cleandf["genre"].str.replace(",", "/")
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

    # Save to csv
    csvname = filename.replace(".jsonl", ".csv")
    cleandf.to_csv(csvname, index=False)