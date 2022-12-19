import pandas as pd
import numpy as np
import time
import plotly.express as px

df = pd.read_csv(
    '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/2000-2016/allegations.csv', low_memory=False)
df["Beat Count"] = 0
df = df.dropna(subset=['Beat'])
# Drop all allegations that are not Use Of Force
df = df[df['Category'] == 'Use Of Force']
# Count how many times each beat appears throughout the dataset, and add that count to the Beat Count column, for each row, matching the beat
# use value counts on beat column
beat_counts = df['Beat'].value_counts()
# match beat to beat count
for index, row in df.iterrows():
    df.loc[index, 'Beat Count'] = beat_counts[row['Beat']]
# calculate proportion of beat count to total number of allegations
# normalize beat count with sum of all beat counts
df['Beat Count'] = df['Beat Count'] / df['Beat Count'].sum()
# get list of unique officers in the dataset
officer_list = pd.unique(df['OfficerID'])
# group by CRID
df_grouped = df.groupby('CRID')
# permutation test
# probabilities are in df["Beat Count"]
officers = pd.read_csv(
    '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/2000-2016/officer_profile.csv', low_memory=False)
# map beat of offcers in officer_list to officers dataframe
officers['Beat'] = 0
for index, row in officers.iterrows():
    if row['OfficerID'] in officer_list:
        officers.loc[index, 'Beat'] = df.loc[df['OfficerID']
                                             == row['OfficerID'], 'Beat'].iloc[0]
# if beat is 0, drop
officers = officers[officers['Beat'] != 0]
# officers.to_csv('/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/Processed/2000-2016/officers_plus_beat.csv')
officers["Probability"] = 0
# groupby beat
officers_grouped = officers.groupby('Beat')
# make probabilities add to one in each group
for name, group in officers_grouped:
    officers.loc[officers['Beat'] == name, 'Probability'] = 1 / len(group)
new_df = pd.DataFrame(
    columns=['OfficerID', 'Beat', 'Occurences', 'Probability'])
original = pd.read_csv(
    "/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Code/Undergraduate-Thesis/Tests/Results/original.csv")
# calculate probability of each officer in the original dataframe
original['Probability'] = original['Number of Officers'] / \
    original['Number of Officers'].sum()
# Polya Urn Model, Rich get Richer
# alpha is a numpy array of the values from 0.01 to 1, incrementing by 0.01
alpha_arr = np.arange(0.00, 1.01, 0.1)
# alpha_arr = [0.1]
mse_dict = {}
# get runtime of whole for loop
start_time = time.time()
for alpha in alpha_arr:
    print(alpha)
    for index, row in df_grouped:
        # get num officers in group
        num_officers = len(row)
        # get beat of group
        beat = row['Beat'].iloc[0]
        # Get num_officers number of officers from officers_grouped
        if beat not in officers_grouped.groups:
            continue
        probs = officers_grouped.get_group(beat)['Probability']
        # print(probs)
        officers_in_group = officers_grouped.get_group(beat).sample(
            n=num_officers, replace=False, weights=probs)
        # add officers_in_group and their 'OfficerID', 'Beat', 'Probability' to new_df and increment 'Occurences' by 1, and update probabilities by adding 0.001
        for index2, row2 in officers_in_group.iterrows():
            if row2['OfficerID'] not in new_df['OfficerID'].values:
                new_df = pd.concat([new_df, pd.DataFrame([[row2['OfficerID'], row2['Beat'], 1, row2['Probability']]], columns=[
                    'OfficerID', 'Beat', 'Occurences', 'Probability'])])
            else:
                new_df.loc[new_df['OfficerID'] ==
                           row2['OfficerID'], 'Occurences'] += 1
                new_df.loc[new_df['OfficerID'] ==
                           row2['OfficerID'], 'Probability'] += alpha
                # update probabilities in officers_grouped
                officers.loc[officers['OfficerID'] ==
                             row2['OfficerID'], 'Probability'] += alpha
    # get mse between original and new_df
    # get value counts of occurences in new_df
    occurences = new_df['Occurences'].value_counts()
    # get mse between original and occurences
    mse = ((original['Number of Officers'] - occurences)**2).mean()
    mse_dict[alpha] = mse
    # reset new_df
    new_df = pd.DataFrame(
        columns=['OfficerID', 'Beat', 'Occurences', 'Probability'])
end_time = time.time()
print("Runtime: " + str(end_time - start_time))
# get alpha with lowest mse
alpha = min(mse_dict, key=mse_dict.get)
# print key and value
print("Alpha: " + str(alpha))
print("MSE: " + str(mse_dict[alpha]))
for index, row in df_grouped:
    # get num officers in group
    num_officers = len(row)
    # get beat of group
    beat = row['Beat'].iloc[0]
    # Get num_officers number of officers from officers_grouped
    if beat not in officers_grouped.groups:
        continue
    probs = officers_grouped.get_group(beat)['Probability']
    # print(probs)
    officers_in_group = officers_grouped.get_group(beat).sample(
        n=num_officers, replace=False, weights=probs)
    # add officers_in_group and their 'OfficerID', 'Beat', 'Probability' to new_df and increment 'Occurences' by 1, and update probabilities by adding 0.001
    for index2, row2 in officers_in_group.iterrows():
        if row2['OfficerID'] not in new_df['OfficerID'].values:
            new_df = pd.concat([new_df, pd.DataFrame([[row2['OfficerID'], row2['Beat'], 1, row2['Probability']]], columns=[
                               'OfficerID', 'Beat', 'Occurences', 'Probability'])])
        else:
            new_df.loc[new_df['OfficerID'] ==
                       row2['OfficerID'], 'Occurences'] += 1
            new_df.loc[new_df['OfficerID'] ==
                       row2['OfficerID'], 'Probability'] += alpha
            # update probabilities in officers_grouped
            officers.loc[officers['OfficerID'] ==
                         row2['OfficerID'], 'Probability'] += alpha
# get top 10 rows of highest probability in officers dataframe
top_10 = officers.sort_values(by=['Probability'], ascending=False).head(10)
# get bottom 10 rows of lowest probability in officers dataframe
bottom_10 = officers.sort_values(by=['Probability'], ascending=True).head(10)
print(top_10)
print(bottom_10)
# value counts
new_df_vc = new_df['Occurences'].value_counts()
new_df_vc.index.name = 'Number of Allegations'
new_df_vc.name = 'Number of Officers'
# sort new_df_vc by ascending index
new_df_vc = new_df_vc.sort_index(ascending=True)
perm = pd.read_csv(
    "/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Code/Undergraduate-Thesis/Tests/Results/permutation_test.csv")
# Plot original, perm, and new_df_vc using px
# create empty fig, with alpha value in title
fig = px.line(
    title="Original vs Permutation Test vs Polya Urn Model, alpha = " + str(alpha))
# add name to original
fig.add_scatter(x=original['Number of Allegations'],
                y=original['Number of Officers'], name='Original')
fig.add_scatter(x=perm['Number of Allegations'],
                y=perm['Number of Officers'], mode='lines', name='Permutation Test')
fig.add_scatter(x=new_df_vc.index, y=new_df_vc,
                mode='lines', name='Polya Urn Model')
# add x and y axis titles
fig.update_xaxes(title_text='Number of Allegations')
fig.update_yaxes(title_text='Number of Officers')
fig.show()
