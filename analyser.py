import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("cleaned.csv")

genres = df[df.filter(like="genre_").columns]
years = df[df.filter(like="active_").columns]

genres.columns = [col.replace("genre_", "") for col in genres.columns]
years.columns = [col.replace("active_", "") for col in years.columns]

genres_by_year = years.T.dot(genres)

# Label smaller genres as "Other" in the plot for less clutter
threshold = 50
small_genres = genres_by_year.sum(axis=0) <= threshold

major_genres = genres_by_year.loc[:, ~small_genres].copy()
other = genres_by_year.loc[:, small_genres].sum(axis=1)

major_genres = pd.concat([other.rename("Other"), major_genres], axis=1)

num_genres = major_genres.shape[1]
colours = list(plt.cm.tab20.colors[:num_genres-1])
colours.insert(0, "#c2904f")

ax = major_genres.plot(kind="bar", stacked=True, figsize=(12, 8), color=colours,
                       title="Metal subgenres in Estonia over the years",
                       xlabel="Year", ylabel="Number of active bands")
# Reverse legend order for ease of reading
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], title="Metal subgenres")
plt.savefig("genretimeline.pdf")
plt.show()
