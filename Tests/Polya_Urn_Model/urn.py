import pandas as pd
import time
import plotly.express as px

df = pd.read_csv(
    '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Code/Undergraduate-Thesis/Preprocessing_Code/final/data/proportions.csv', low_memory=False)
officers = pd.read_csv(
    '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Code/Undergraduate-Thesis/Preprocessing_Code/final/data/perm_unique_officers.csv', low_memory=False)

# group by CRID
df_grouped = df.groupby('CRID')

# ----------- Start of Polya Urn Model -----------
weighted_officers = officers

weighted_officers['Weights'] = 0
weighted_officers['Occurences'] = 1

# groupby beat
weighted_officers_grouped = weighted_officers.groupby('Beat')
# make weights sum to one in each group
for name, group in weighted_officers_grouped:
    weighted_officers.loc[weighted_officers['Beat'] ==
                          name, 'Weights'] = 1 / len(group)

weighted_df = pd.DataFrame(
    columns=['OfficerID', 'Beat'])

polya_urn_results = []
# Add runtime
start_time = time.time()
for i in range(1):
    alpha = 0.1
    print(i)
    temp_weighted_officers = weighted_officers
    ts = 0
    for index, row in df_grouped:
        # get num officers in group
        num_officers = len(row)
        # get beat of group
        beat = row['Beat'].iloc[0]
        if beat not in weighted_officers_grouped.groups:
            continue
        # polya urn model, rich get richer
        weights = temp_weighted_officers.loc[temp_weighted_officers['Beat']
                                             == beat, 'Weights']
        # if num_officers > officers in beat print error
        if num_officers > len(weights):
            ts += 1
            print(ts)
            continue
        # sample officers from the beat using the weights in the Weights column
        officers_sample = weighted_officers_grouped.get_group(
            beat).sample(n=num_officers, replace=False, weights=weights)
        # add officers to new dataframe
        for index, row in officers_sample.iterrows():
            # pd concat
            weighted_df = pd.concat([weighted_df, pd.DataFrame(
                [[row['OfficerID'], row['Beat']]], columns=['OfficerID', 'Beat'])])
            # Update officer occurences in weighted_officers
            temp_weighted_officers.loc[temp_weighted_officers['OfficerID'] ==
                                       row['OfficerID'], 'Occurences'] += 1
            # update officer weights in weighted_officers
            temp_weighted_officers.loc[temp_weighted_officers['OfficerID'] ==
                                       row['OfficerID'], 'Weights'] += alpha
    # if number of occurences > 35, make them equal to 35
    temp_weighted_officers['Occurences'] = temp_weighted_officers['Occurences'].apply(
        lambda x: 35 if x > 35 else x)
    occurences = temp_weighted_officers['Occurences'].value_counts()
    # save value counts to polya_urn_results
    # if number of occurences suprassed 35, make them into same category

    polya_urn_results = occurences
end_time = time.time()
print("Runtime: " + str(end_time - start_time))
print(polya_urn_results)
# ----------- End of Polya Urn Model -----------
