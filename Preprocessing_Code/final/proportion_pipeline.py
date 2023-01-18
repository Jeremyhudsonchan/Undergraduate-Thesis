import pandas as pd

df = pd.read_csv(
    "/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/2000-2016/allegations.csv", low_memory=False)
profile_df = pd.read_csv(
    "/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/2000-2016/officer_profile.csv", low_memory=False)
# Drop all allegations that are not Use Of Force, Excessive Force
df = df[(df['Category'] == 'Use Of Force') |
        (df['Category'] == 'Excessive Force')]
# Drop unused columns
df = df.drop(["AllegationCode", "Latitude", "Longitude", "Location", "Add1", "Add2", "City", "RecommendedFinding", "RecommendedOutcome",
             "FinalFinding", "FinalOutcome", "Finding", "Outcome", "InvestigatorName", "InvestigatorRank", "StartDate", "EndDate"], axis=1)
# Drop all allegations that are NaN in the Beat column
df = df.dropna(subset=['Beat'])
# Add beat count and beat proportion columns
df["Beat Count"] = 0
df["Beat Proportion"] = 0

# Count how many times each beat appears throughout the dataset, and add that count to the Beat Count column, for each row, matching the beat
# Use value counts on beat column
beat_counts = df['Beat'].value_counts()

# match beat to beat count
for index, row in df.iterrows():
    # print(index)
    # print(row['Beat'])
    df.loc[index, 'Beat Count'] = beat_counts[row['Beat']]

# calculate proportion of beat count to total number of allegations
# normalize beat count with sum of all beat counts
df['Beat Proportion'] = df['Beat Count'] / df['Beat Count'].sum()

# make df_grouped into a csv
df.to_csv("/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Code/Undergraduate-Thesis/Preprocessing_Code/final/data/proportions.csv", index=False)

# Here ends the code for creating a csv file that contains the proportion of which a beat appears in the dataset
