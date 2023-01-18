import pandas as pd
import numpy as np
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

# Find Optimal Alpha
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

weighted_officers = officers

weighted_officers['Weights'] = 0
weighted_officers['Occurences'] = 1

# groupby beat
weighted_officers_grouped = weighted_officers.groupby('Beat')
# make weights sum to one in each group
for name, group in weighted_officers_grouped:
    weighted_officers.loc[weighted_officers['Beat'] ==
                          name, 'Weights'] = 1 / len(group)

alpha_arr = np.arange(0.1, 1.1, 0.1)
mse_dict = {}
polya_urn_results = {}
# Add runtime
start_time = time.time()
for alpha in alpha_arr:
    perm_df = pd.DataFrame(columns=['Occurences', 'Frequencies'])
    print(alpha)
    temp_weighted_officers = weighted_officers
    ts = 0
    for index, row in df_grouped:
        num_officers = len(row)
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
    # add occurences to polya_urn_results, with alpha being the key
    polya_urn_results[alpha] = occurences
    # get mean squared error between df_vc and occurences
    mse = ((df_vc - occurences)**2).mean()
    mse_dict[alpha] = mse
end_time = time.time()
print("Runtime: " + str(end_time - start_time))

# get the alpha that minimizes the mse
alpha = min(mse_dict, key=mse_dict.get)
# print key and value
print("Alpha: " + str(alpha))
print("MSE: " + str(mse_dict[alpha]))
print(alpha_arr)


# plot polya_urn_results
fig = px.line(polya_urn_results[alpha], x=polya_urn_results[alpha].index, y=polya_urn_results[alpha].values, labels={
    'x': 'Number of Allegations', 'y': 'Number of Officers'})
fig.update_layout(title_text='Polya Urn Model Optmial Alpha: ' + str(alpha))

# # 95% confidence interval for polya urn model using the specific alpha
# polya_conf_intv = pd.concat(polya_urn_results[alpha]).groupby(level=0).quantile(
#     [0.025, 0.975]).unstack()

# # get average
# polya_df_vc = pd.concat(polya_urn_results[alpha]).groupby(level=0).mean()

# plot polya_df_vc, polya_conf_intv
# fig = px.line(polya_df_vc, x=polya_df_vc.index, y=polya_df_vc.values, labels={
#               'x': 'Number of Allegations', 'y': 'Number of Officers'})
# fig.add_scatter(x=polya_conf_intv.index, y=polya_conf_intv[0.025],
#                 mode='lines', name='Polya Urn Model 95% Confidence Interval')
# fig.add_scatter(x=polya_conf_intv.index, y=polya_conf_intv[0.975],
#                 mode='lines', name='Polya Urn Model 95% Confidence Interval')
# fig.update_layout(title_text='Polya Urn Model Results')
fig.show()
