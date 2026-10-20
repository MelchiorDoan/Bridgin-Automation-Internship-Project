
# **Steps:** 1 Load and check - 2 Explore - 3 One row per home - 4 Same scale - 5 Try 1 to 8 segments - 6 Fit the final model - 7 Describe segments

# ---- SETUP: load the toolboxes ("import" = bring in ready-made tools written by other people) ----
import warnings                                    # a tool for controlling warning messages
import numpy as np                                 # numpy: tools for numbers and maths ("np" is its nickname)
import pandas as pd                                # pandas: tools for tables, like Excel ("pd" is its nickname)
import matplotlib.pyplot as plt                    # matplotlib: tools for drawing charts ("plt" is its nickname)
from sklearn.preprocessing import StandardScaler   # from the scikit-learn library, take the tool that rescales columns
from sklearn.mixture import GaussianMixture        # ...take the tool that fits the GMM (our clustering model)
from sklearn.metrics import silhouette_score, adjusted_rand_score   # ...take two scoring tools: "how well separated" and "how much two groupings agree"
from sklearn.decomposition import PCA              # ...take the tool that squeezes many columns down to 2 for a chart
from sklearn.exceptions import ConvergenceWarning  # ...take the name of a harmless warning that we want to hide

# Tell Python to hide that one kind of harmless warning so the output stays clean
warnings.filterwarnings("ignore", category=ConvergenceWarning)

# Two settings used throughout. (Capital letters are a habit for "settings you might change".)
DATA_FILE = "smart_home_energy_consumption_large.csv"   # the name of your data file. Text always goes in quotes.
SEED = 42    # a starting number for the computer's random choices. Same seed = same results every time.

# ## Step 1 - Load and check the data

# Read the CSV file into a table, and store the table in a box called df
df = pd.read_csv(DATA_FILE)

# Rename columns to shorter names. 
df = df.rename(columns={
    "Home ID": "home",                          # "Home ID" becomes "home"
    "Appliance Type": "appliance",              # "Appliance Type" becomes "appliance"
    "Energy Consumption (kWh)": "kwh",          # the energy column becomes "kwh"
    "Time": "time",                             # time of the reading
    "Date": "date",                             # date of the reading
    "Outdoor Temperature (°C)": "temp",         # outdoor temperature
    "Season": "season",                         # season label
    "Household Size": "household_size",         # number of people in the home
})

print("Rows, columns:", df.shape)                                   # .shape gives (number of rows, number of columns)
print("Number of homes:", df["home"].nunique())                     # pick the home column; .nunique() counts how many different values it has
print("Appliance types:", df["appliance"].nunique(), "->", sorted(df["appliance"].unique()))   # .unique() lists each different value once; sorted() puts them A to Z
print("Missing values per column:")                                 # a heading line
print(df.isna().sum())                                              # .isna() marks empty cells; .sum() counts them for each column
print("Duplicate rows:", df.duplicated().sum())                     # .duplicated() marks rows that repeat an earlier row; .sum() counts them
df.head()                                                           # show the first 5 rows, as a quick look

#  2 - Explore the data

# **In the meeting:** "We checked what drives energy use before choosing a model."

print("Average kWh per reading, by appliance:")     # a heading line
# Put rows into groups by appliance; look at the kwh column; average it; round to 2 decimals; sort from low to high. "\n" adds a blank line after.
print(df.groupby("appliance")["kwh"].mean().round(2).sort_values(), "\n")

print("Average kWh per reading, by season:")        # heading
print(df.groupby("season")["kwh"].mean().round(3), "\n")           # same idea, grouped by season, rounded to 3 decimals

print("Average kWh per reading, by household size:") # heading
print(df.groupby("household_size")["kwh"].mean().round(3), "\n")   # same idea, grouped by household size

# For each home, count how many DIFFERENT household sizes it reports
sizes_per_home = df.groupby("home")["household_size"].nunique()
# (sizes_per_home > 1) is True for homes reporting more than one size; .sum() counts the Trues; int() makes it a whole number; len() counts all homes
print("Homes that report more than one household size:", int((sizes_per_home > 1).sum()), "of", len(sizes_per_home))

# Draw a horizontal bar chart of average kWh for each appliance, sorted. "#0072B2" is a colour code (blue).
df.groupby("appliance")["kwh"].mean().sort_values().plot(kind="barh", color="#0072B2")   # barh = horizontal bars
plt.xlabel("Average kWh per reading")                    # label under the chart
plt.title("Average kWh per reading, by appliance")       # chart title
plt.tight_layout()                                       # tidy the spacing so nothing is cut off
plt.show()                                               # display the chart

# 3 - Build one row per home
# **What this does:** the file has one row per reading (about 200 per home). Clustering needs one row per home, so we summarise each home with:
# - `avg_<appliance>`: the average kWh per reading for each appliance (10 columns, one per appliance)
#
# `make_features` is a small reusable recipe. We reuse it in the quality checks later.
#
# **In the meeting:** "Each home is now described by how much each appliance uses per reading."

# %%
# "def" starts a recipe called make_features. It takes a table (we call it "data") and will give back a new table.
def make_features(data):
    # For every (home, appliance) pair, work out the AVERAGE kWh per reading.
    # .unstack(...) turns the appliances into columns, so each home becomes one row.
    # If a home has no readings for an appliance, fill_value=0 puts a 0 there (it never used it).
    avg = data.groupby(["home", "appliance"])["kwh"].mean().unstack(fill_value=0)
    # Put "avg_" in front of every column name, e.g. Fridge becomes avg_Fridge.
    avg.columns = ["avg_" + name for name in avg.columns]
    # Hand the finished table back to whoever used the recipe
    return avg

# Use the recipe on our data, and keep the result in a box called features
features = make_features(df)
print("Table size (homes x features):", features.shape)   # rows = homes, columns = features (should be 500 x 10)
features.round(3).head()                                  # show the first 5 homes, numbers rounded to 3 decimals

# 4 - Put the features on the same scale

scaler = StandardScaler()                # create the rescaling tool (it has not done anything yet)
X = scaler.fit_transform(features)       # "fit" = learn each column's average and spread; "transform" = apply the rescaling. X is the rescaled table.
print("Scaled table size:", X.shape)                                                 # same number of rows and columns as before
print("Column averages (should be about 0):", X.mean(axis=0).round(2)[:4], "...")    # axis=0 means "down each column"; [:4] means "just the first four"
print("Column spreads  (should be about 1):", X.std(axis=0).round(2)[:4], "...")     # the spread of each column

# 5 - Try 1 to 8 segments and compare BIC
# **What this does:** a GMM looks for overlapping "clouds" of homes. We do not know how many clouds there are, so we try 1 to 8 and score each with **BIC**. BIC rewards a good fit but penalises extra clouds. **Lower BIC is better.**
#
# **What to look for:** a clear dip at some number of segments means that number fits best. A line that only rises means one group fits best.
#
# **In the meeting:** "We let the data suggest the number of segments instead of picking one ourselves."

K_MAX = 8                 # the biggest number of segments to try
bic_scores = {}           # an empty "dictionary": a list of label -> value pairs. We fill it in below.

# A LOOP: repeat the indented lines once for each k = 1, 2, ... 8 (range(1, 9) means 1 up to 8)
for k in range(1, K_MAX + 1):
    # Build a GMM with k clouds, then train it on our table. The lines inside ( ) are its settings.
    model = GaussianMixture(
        n_components=k,            # how many clouds (segments) to look for
        covariance_type="full",    # clouds may be stretched and tilted, not just round
        n_init=5,                  # try 5 different random starting points and keep the best
        reg_covar=1e-4,            # a tiny safety margin so the maths never breaks (1e-4 = 0.0001)
        max_iter=500,              # stop refining after 500 rounds
        random_state=SEED,         # use our fixed starting number so results repeat
    ).fit(X)                       # .fit(X) means "learn the clouds from table X"
    bic_scores[k] = model.bic(X)   # work out the BIC score for this model and store it in the dictionary under the label k

print("BIC for each number of segments (lower is better):")   # heading line
print(pd.Series(bic_scores).round(0))                         # turn the dictionary into a one-column table, round it, show it
print("Lowest BIC overall is at k =", min(bic_scores, key=bic_scores.get))   # find the k whose score is smallest
plt.plot(list(bic_scores.keys()), list(bic_scores.values()), "o-", color="#0072B2")
plt.xlabel("Number of segments (k)")
plt.ylabel("BIC (lower is better)")
plt.title("GMM: BIC by number of segments")
plt.tight_layout()
plt.show()


# 6 - Choose the number of segments and fit the final model
K_OVERRIDE = None

K = K_OVERRIDE or min(range(2, K_MAX + 1), key=lambda k: bic_scores[k])

# Train the final model with K clouds (same settings as Step 5)
final_model = GaussianMixture(
    n_components=K, covariance_type="full", n_init=5,
    reg_covar=1e-4, max_iter=500, random_state=SEED,
).fit(X)

raw_labels = final_model.predict(X)         # for each home: which cloud fits it best (0, 1, 2...)
raw_probs = final_model.predict_proba(X)    # for each home: the probability of belonging to EACH cloud

# The next four lines renumber the clouds so that Segment 1 is the biggest (easier to read)
order = np.argsort(-np.bincount(raw_labels, minlength=K))   # count the homes in each cloud, then list the clouds from biggest to smallest
new_id = np.empty(K, dtype=int)             # make an empty list of K whole numbers
new_id[order] = np.arange(K)                # fill it in: the biggest cloud gets 0, the next gets 1. Order = [1, 0] means: team 1 gets the number 0 (biggest), team 0 gets the number 1.  So new_id = [1, 0]   (read it as: "team 0 -> 1, team 1 -> 0")

# Give every house its NEW team number. Look up each house's old team on the board,
# then add 1 so we count from 1 instead of 0 (humans say "Segment 1", not "Segment 0").
#   raw_labels  [0, 1, 1, 0, 1, 1]
#   new_id says  0->1,  1->0   so the houses become [1, 0, 0, 1, 0, 0]
#   add 1                      so the final result is [2, 1, 1, 2, 1, 1]
#   Check: the 4 houses from the big team are now "Segment 1". It worked.
segment = new_id[raw_labels] + 1          


probs = raw_probs[:, order]                 # reorder the probability columns the same way (":" means "all rows")

results = features.copy()                                  # make a copy of the features table to add our results to
results["segment"] = segment                               # add a column holding each home's segment
results["membership_prob"] = probs.max(axis=1).round(3)    # add a column: the highest probability for each home (how sure the model is)
for j in range(K):                                         # repeat for each segment: j = 0, 1, ...
    results[f"prob_segment_{j + 1}"] = probs[:, j].round(3)   # add one probability column per segment; f"..." slips the number into the name

real_sil = silhouette_score(X, segment)     # score how clearly separated the segments are (-1 to 1)

print("Number of segments:", K)
print("Homes per segment:")
print(results["segment"].value_counts().sort_index())        # count homes in each segment, listed in order
print("Average membership probability:", results["membership_prob"].mean().round(3))   # average confidence across all homes
print("Homes with probability below 0.6 (borderline):", int((probs.max(axis=1) < 0.6).sum()))   # count homes whose best probability is under 0.6
print("Silhouette score:", round(real_sil, 3), "(above 0.5 is clear, below 0.25 is little structure)")
results.head()                                               # show the first 5 homes with their segment and probabilities

# Step 7 - Describe the segments
profile = features.groupby(segment).mean()                       # for each segment, the average of every feature
overall_mean, overall_spread = features.mean(), features.std()   # the average and spread of every feature across ALL homes

for seg in profile.index:                                        # repeat for each segment number
    z = (profile.loc[seg] - overall_mean) / overall_spread       # how far this segment is from the overall average, in units of spread
    top3 = z.reindex(z.abs().sort_values(ascending=False).index)[:3]   # sort by size of difference (ignoring +/-), keep the biggest 3
    words = [("higher " if v > 0 else "lower ") + name for name, v in top3.items()]   # for each: write "higher" if above average, else "lower", plus the feature name
    print(f"Segment {seg} ({int((segment == seg).sum())} homes): " + ", ".join(words))   # show the segment, its size, and the 3 phrases joined by commas

# Make a 2D picture of all homes
xy = PCA(n_components=2, random_state=0).fit_transform(X)        # squeeze the 10 columns down to 2 so we can plot them
colours = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00", "#F0E442", "#7F7F7F"]   # a list of colour codes, one per segment
for seg in sorted(set(segment)):                                 # repeat for each segment
    mask = segment == seg                                        # True for homes in this segment, False for the others
    plt.scatter(xy[mask, 0], xy[mask, 1], s=14, alpha=0.75, color=colours[(seg - 1) % 8], label=f"Segment {seg}")   # draw those homes as dots (s = dot size, alpha = see-through level)
plt.xlabel("PC1"); plt.ylabel("PC2")                             # axis labels ("PC" = the 2 new squeezed-down dimensions)
plt.title("Homes in 2D, coloured by segment")                    # chart title
plt.legend()                                                     # show which colour is which segment
plt.tight_layout()                                               # tidy the spacing
plt.show()                                                       # display the chart

profile.round(3)                                                 # show the segment averages table, rounded
