# Side Notes:
# Since the distribution is skewed to the right, I will plan to change up the Polya Urn Model to better match the distribution.
# Theory is similar to tf-dif, or maybe like a upside down parabola
# The chances that a police officer commits a crime increases initially, then decreases again.
# In real life, the chances of a police officer committing a crime might decrease as they get older.
# Might face restrictions and consequences for committing a crime, and might be more careful.
# Might be more restricted in their actions as they are recieving a lot of complaints (they might be moved to different divisions etc)

import pandas as pd
import time
import plotly.express as px

df = pd.read_csv(
    '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Code/Undergraduate-Thesis/Preprocessing_Code/final/data/proportions.csv', low_memory=False)
officers = pd.read_csv(
    '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Code/Undergraduate-Thesis/Preprocessing_Code/final/data/perm_unique_officers.csv', low_memory=False)

# group by CRID
df_grouped = df.groupby('CRID')

# find number of groups that have more than one officer
print(len(df_grouped.filter(lambda x: len(x) > 1)))

# ----------- Start of Original -----------
# original
df_vc = df['OfficerID'].value_counts()

# get number of times each value appears in df_vc
df_vc = df_vc.value_counts()

# change index title to number of allegations, value to number of officers
df_vc.index.name = 'Number of Allegations'
df_vc.name = 'Number of Officers'

# plot density curve of df_vc using plotly
fig = px.line(df_vc, x=df_vc.index, y=df_vc.values, labels={
              'x': 'Number of Allegations', 'y': 'Number of Officers'})
fig.update_layout(title_text='Original')
fig.show()
# ----------- End of Original -----------


# ----------- Start of Permutation Test -----------
# permutation test loop 20 simulations
perm_test_results = []
for i in range(20):
    print(i)
    # probabilities are in df_grouped["Beat Count"]
    # new_df to store permutation test results
    new_df = pd.DataFrame(columns=['OfficerID', 'Beat'])
    for index, row in df_grouped:
        # get num officers in group
        num_officers = len(row)
        # get beat of group
        beat = row['Beat'].iloc[0]
        # get beat count of group
        # beat_count = row['Beat'].iloc[0]
        # print(beat_count)
        officers_in_beat = officers.loc[officers['Beat'] == beat]
        if num_officers > len(officers_in_beat):
            # ts += 1
            # print("troubleshoot", ts)
            continue
        # randomly sample officers without replacement from officers dataframe
        officers_sample = officers.sample(n=num_officers)
        # add officers to new dataframe
        for index, row in officers_sample.iterrows():
            # pd concat
            new_df = pd.concat([new_df, pd.DataFrame(
                [[row['OfficerID'], row['Beat']]], columns=['OfficerID', 'Beat'])])

    # value counts of officers appearing in new_df
    new_df_vc = new_df['OfficerID'].value_counts()

    # get number of times each value appears in new_df_vc
    new_df_vc = new_df_vc.value_counts()
    # change index title to number of allegations, value to number of officers
    new_df_vc.index.name = 'Number of Allegations'
    new_df_vc.name = 'Number of Officers'

    perm_test_results.append(new_df_vc)

# get 95% confidence interval
conf_intv = pd.concat(perm_test_results).groupby(level=0).quantile(
    [0.025, 0.975]).unstack()

# get average of perm_test_results
new_df_vc = pd.concat(perm_test_results).groupby(level=0).mean()

# Plot
# plot new_df_vc using plotly, also include 95% confidence interval
# title is Perumtation Test Results
fig = px.line(new_df_vc, x=new_df_vc.index, y=new_df_vc.values, labels={
              'x': 'Number of Allegations', 'y': 'Number of Officers'})
fig.add_scatter(x=conf_intv.index, y=conf_intv[0.025],
                mode='lines', name='Permutation Test 95% Confidence Interval')
fig.add_scatter(x=conf_intv.index, y=conf_intv[0.975],
                mode='lines', name='Permutation Test 95% Confidence Interval')
fig.update_layout(title_text='Permutation Test Results')
fig.show()
# ----------- End of Permutation Test -----------

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
for i in range(20):
    alpha = 0.1
    perm_df = pd.DataFrame(columns=['Occurences', 'Frequencies'])
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
            # ts += 1
            # print("troubleshoot", ts)
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
    # add occurences to perm_df
    occurences.index.name = 'Number of Allegations'
    occurences.name = 'Number of Officers'
    # save it to polya_urn_results
    polya_urn_results.append(occurences)
end_time = time.time()
print("Runtime: " + str(end_time - start_time))

# 95% confidence interval for polya urn model
polya_conf_intv = pd.concat(polya_urn_results).groupby(level=0).quantile(
    [0.025, 0.975]).unstack()

# get average
polya_df_vc = pd.concat(polya_urn_results).groupby(level=0).mean()

# plot polya_df_vc, polya_conf_intv
fig = px.line(polya_df_vc, x=polya_df_vc.index, y=polya_df_vc.values, labels={
              'x': 'Number of Allegations', 'y': 'Number of Officers'})
fig.add_scatter(x=polya_conf_intv.index, y=polya_conf_intv[0.025],
                mode='lines', name='Polya Urn Model 95% Confidence Interval')
fig.add_scatter(x=polya_conf_intv.index, y=polya_conf_intv[0.975],
                mode='lines', name='Polya Urn Model 95% Confidence Interval')
fig.update_layout(title_text='Polya Urn Model Results')
fig.show()

# plot all on same graph, add names to legend
# create empty px figure with x and y labels
fig = px.line(labels={
    'x': 'Number of Allegations', 'y': 'Number of Officers'})

fig.add_scatter(x=df_vc.index, y=df_vc.values,
                mode='lines', name='Original Results')

fig.add_scatter(x=conf_intv.index, y=conf_intv[0.025],
                mode='lines', name='Permutation Test 95% Confidence Interval')

fig.add_scatter(x=conf_intv.index, y=conf_intv[0.975],
                mode='lines', name='Permutation Test 95% Confidence Interval')

fig.add_scatter(x=new_df_vc.index, y=new_df_vc.values,
                mode='lines', name='Permutation Test Results')

fig.add_scatter(x=polya_conf_intv.index, y=polya_conf_intv[0.025],
                mode='lines', name='Polya Urn Model 95% Confidence Interval')

fig.add_scatter(x=polya_conf_intv.index, y=polya_conf_intv[0.975],
                mode='lines', name='Polya Urn Model 95% Confidence Interval')

fig.add_scatter(x=polya_df_vc.index, y=polya_df_vc.values,
                mode='lines', name='Polya Urn Model Results')

fig.update_layout(title_text='Combined Results')
# add label to legend
fig['data'][0]['name'] = 'Original Results'
fig.update_layout(showlegend=True)
fig.show()
