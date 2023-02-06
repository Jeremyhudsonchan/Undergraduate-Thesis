import pandas as pd
import time
import numpy as np
import plotly.graph_objs as go

df = pd.read_csv(
    '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Code/Undergraduate-Thesis/Preprocessing_Code/final/data/proportions.csv', low_memory=False)
officers = pd.read_csv(
    '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Code/Undergraduate-Thesis/Preprocessing_Code/final/data/perm_unique_officers.csv', low_memory=False)

# df = pd.read_csv('/content/gdrive/MyDrive/Thesis_Data/proportions.csv')
# officers = pd.read_csv('/content/gdrive/MyDrive/Thesis_Data/perm_unique_officers.csv')

print(df.columns)
print(df.head())
print(officers.columns)

# choose only OfficerID and Beat columns
prep_df = df[['OfficerID', 'Beat', 'Beat Count', 'Beat Proportion']]
prep_officers = officers[['OfficerID', 'Beat']]
# group by CRID
df_grouped = df[['CRID', 'OfficerID', 'Beat',
                 'Beat Count', 'Beat Proportion']].groupby('CRID')
# make df_grouped into a numpy array
np_grouped = df_grouped.apply(lambda x: x.to_numpy())
# make np_grouped into a numpy array
np_grouped = np_grouped.to_numpy()

# make df into numpy
np_df = prep_df.to_numpy()
np_officers = prep_officers.to_numpy()
# make array dtype object float
np_df = np_df.astype(float)
np_officers = np_officers.astype(float)

# Column 0 is OfficerID, Column 1 is Beat
# ----------- Start of Original -----------
# get value counts of OfficerID
officer_counts = np.unique(np_df[:, 0], return_counts=True)
# get number of times each value appears in officer_counts
# sort in descending order
officer_counts = np.unique(officer_counts[1], return_counts=True)
# if number of complaints exceed 20, make all of the counts into a single bin
# make a copy of the original array to save for reference
officer_counts_copy = np.copy(officer_counts)
# this is to prevent the graph from being too stretched
for i in range(len(officer_counts[0])):
    if officer_counts[0][i] > 10:
        officer_counts[0][i] = 10
# plot density curve
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=officer_counts[0], y=officer_counts[1], mode='lines', name='Data'))
fig.update_layout(title_text='Original Data')
fig.show()

# print sum of counts
print('Sum of Counts: ', np.sum(officer_counts[1]))

num_simulations = 1000

# ----------- Start of Permutation Test -----------
# permutation test loop 1000 simulations
start_time = time.time()
# perm_test_results to be a 3d array
perm_test_results = []
for i in range(num_simulations):
    print(i)
    # make 1d array of 0s, length of np_officers
    perm_test = np.array([])
    # for each element in np_grouped, get length of each individual element
    for incident in np_grouped:
        # get length of each individual element
        num_officers = len(incident)
        # get beat of group
        beat = incident[0][2]
        if beat not in np_officers[:, 1]:
            continue
        # get officers in beat
        officers_in_beat = np_officers[np_officers[:, 1] == beat]
        if len(officers_in_beat) < num_officers:
            continue
        # randomly sample officers without replacement from officers in beat
        sample_officers = np.random.choice(
            officers_in_beat[:, 0], num_officers, replace=False)
        # add sample officers to perm_test
        perm_test = np.append(perm_test, sample_officers)
    # get value counts of OfficerID in perm_test
    perm_test_counts = np.unique(perm_test, return_counts=True)
    # print(perm_test_counts)
    # get number of times each value appears in perm_test_counts
    # sort in descending order
    perm_test_counts = np.unique(perm_test_counts[1], return_counts=True)
    # add perm_test_counts to perm_test_results
    perm_test_results.append(perm_test_counts)
end_time = time.time()

print(end_time - start_time)
# print(perm_test_results)

# make perm_test_results into a pandas df
perm_test_results = pd.DataFrame(perm_test_results)
# rename columns
perm_test_results.columns = ['Number of Complaints', 'Counts']
# get proportion of each number of complaints by going through each value of number of complaints one by one

perm_test_results.head(10)

# add 0 to each datapoint in Number of Complaints
perm_test_results['Number of Complaints'] = perm_test_results['Number of Complaints'].apply(
    lambda x: np.concatenate(([0], x)))
# and insert the np.sum(officer_counts[1]) - np.sum(polya_urn_results['Counts']) into the second column
perm_test_results['Counts'] = perm_test_results['Counts'].apply(
    lambda x: np.concatenate(([np.sum(officer_counts[1]) - np.sum(x)], x)))
# add 1 to all the counts to perm_test_results
perm_test_results['Number of Complaints'] = perm_test_results['Number of Complaints'].apply(
    lambda x: x + 1)

perm_test_results.head(10)

# for each row in pem_test_results, print out sum of counts column
perm_sum = []
for i in range(len(perm_test_results)):
    perm_sum.append(sum(perm_test_results.iloc[i, 1]))

print(np.mean(perm_sum))

# explode the number of complaints column, then get max value
max_complaints = max(perm_test_results['Number of Complaints'].explode())
print(max_complaints)
# create dictionary of number of complaints and counts, key is number of complaints, value is counts
# keys should range from 1 to max_complaints
complaints_dict = {}
for i in range(1, 11):
    complaints_dict[i] = []
# for each row in perm_test_results, get the list of Number of Complaints, then get the list of Counts, then map them to the dictionary
for index, row in perm_test_results.iterrows():
    # get list of number of complaints
    complaints = row['Number of Complaints']
    # get list of counts
    counts = row['Counts']
    # map them to the dictionary
    for i in range(len(complaints)):
        if complaints[i] < 10:
            complaints_dict[complaints[i]].append(counts[i])
        else:
            complaints_dict[10].append(counts[i])

# if the list length is not equal to num_simulations, then add 0s to the list until it is equal to num_simulations
for key in complaints_dict:
    if len(complaints_dict[key]) != num_simulations:
        complaints_dict[key] = complaints_dict[key] + [0] * \
            (num_simulations - len(complaints_dict[key]))

# get the average of each list in the dictionary
perm_avg_complaints_dict = {}
for key in complaints_dict:
    perm_avg_complaints_dict[key] = sum(complaints_dict[key])/num_simulations

# get the 95% confidence interval of each list in the dictionary
upper_perm_ci_complaints_dict = {}
lower_perm_ci_complaints_dict = {}
for key in complaints_dict:
    # 95% confidence interval using quantile
    upper_perm_ci_complaints_dict[key] = np.quantile(
        complaints_dict[key], 0.975)
    lower_perm_ci_complaints_dict[key] = np.quantile(
        complaints_dict[key], 0.025)

# plot curve
# Number of Complaints are on the x-axis, Counts are on the y-axis
fig = go.Figure()
fig.add_trace(go.Scatter(x=list(perm_avg_complaints_dict.keys()), y=list(
    perm_avg_complaints_dict.values()), mode='lines', name='Permutation Test Results'))
# add line with color
fig.add_trace(go.Scatter(x=list(upper_perm_ci_complaints_dict.keys()), y=list(upper_perm_ci_complaints_dict.values(
)), mode='lines', name='Permutation Test 95% Confidence Interval', line=dict(color='rgb(235, 52, 58)', dash='dash')))
fig.add_trace(go.Scatter(x=list(lower_perm_ci_complaints_dict.keys()), y=list(lower_perm_ci_complaints_dict.values()), mode='lines',
              name='Permutation Test 95% Confidence Interval', line=dict(color='rgb(235, 52, 58)', dash='dash'), fill='tonexty', fillcolor='rgba(235, 52, 58,0.2)'))
fig.add_trace(go.Scatter(
    x=officer_counts[0], y=officer_counts[1], mode='lines', name='Data'))
fig.update_layout(title_text='Permutation Test Results')
fig.show()

# ----------- Start of Polya Urn Model -----------
weighted_np_officers = np_officers
# add 0 column to weighted_np_officers
weighted_np_officers = np.insert(weighted_np_officers, 2, 0, axis=1)
weighted_np_officers = np.insert(weighted_np_officers, 3, 1, axis=1)
# sort weighted_np_officers by values in second column
weighted_np_officers = weighted_np_officers[weighted_np_officers[:, 1].argsort(
)]
# for each unique value in the second column, get the number of times it appears
unique_beats, beat_counts = np.unique(
    weighted_np_officers[:, 1], return_counts=True)
# for each unique beat, make the sum of the third column equal to 1
for beat in unique_beats:
    # get indices of beat
    beat_indices = np.where(weighted_np_officers[:, 1] == beat)
    # get number of officers in beat
    num_officers = beat_counts[np.where(unique_beats == beat)]
    # get weights for officers in beat
    weighted_np_officers[beat_indices, 2] = 1 / num_officers

polya_urn_results = []
start_time = time.time()
alpha = 0.1
for i in range(num_simulations):
    print(i)
    # make 1d array of 0s, length of np_officers
    polya_urn = np.array([])
    temp_weighted_np_officers = weighted_np_officers.copy()
    # for each element in np_grouped, get length of each individual element
    for incident in np_grouped:
        # get length of each individual element
        num_officers = len(incident)
        # get beat of group
        beat = incident[0][2]
        if beat not in weighted_np_officers[:, 1]:
            continue
        # get officers in beat
        officers_in_beat = temp_weighted_np_officers[temp_weighted_np_officers[:, 1] == beat]
        if len(officers_in_beat) < num_officers:
            continue
        # randomly sample officers without replacement from officers in beat
        p = officers_in_beat[:, 2] / sum(officers_in_beat[:, 2])
        sample_officers = np.random.choice(
            officers_in_beat[:, 0], num_officers, replace=False, p=p)
        # add sample officers to polya_urn
        polya_urn = np.append(polya_urn, sample_officers)
        # print(sample_officers)
        # selected officers weights go up by alpha
        for officer in sample_officers:
            temp_weighted_np_officers[temp_weighted_np_officers[:, 0]
                                      == officer, 2] += alpha
            temp_weighted_np_officers[temp_weighted_np_officers[:, 0]
                                      == officer, 3] += 1
        # if officer allegations go above 35, set weight to 0
        # temp_weighted_np_officers[temp_weighted_np_officers[:, 3] > 35, 2] = 0.000000001
    # get value counts of OfficerID in polya_urn
    polya_urn_counts = np.unique(polya_urn, return_counts=True)
    # get number of times each value appears in polya_urn_counts
    # sort in descending order
    polya_urn_counts = np.unique(polya_urn_counts[1], return_counts=True)
    # add polya_urn_counts to polya_urn_results
    polya_urn_results.append(polya_urn_counts)
end_time = time.time()
print(end_time - start_time)

polya_urn_results = pd.DataFrame(polya_urn_results)
polya_urn_results.columns = ['Number of Complaints', 'Counts']

# add 0 to each datapoint in Number of Complaints
polya_urn_results['Number of Complaints'] = polya_urn_results['Number of Complaints'].apply(
    lambda x: np.concatenate(([0], x)))
# and insert the np.sum(officer_counts[1]) - np.sum(polya_urn_results['Counts']) into the second column
polya_urn_results['Counts'] = polya_urn_results['Counts'].apply(
    lambda x: np.concatenate(([np.sum(officer_counts[1]) - np.sum(x)], x)))
# add 1 to all the counts to match
polya_urn_results['Number of Complaints'] = polya_urn_results['Number of Complaints'].apply(
    lambda x: x + 1)

# Remark, Data here is ascending, number of complaints seems like it gets capped, will need to look into this
polya_urn_results.head(50)

# explode the number of complaints column, then get max value
urn_max_complaints = max(polya_urn_results['Number of Complaints'].explode())
print(urn_max_complaints)
# create dictionary of number of complaints and counts, key is number of complaints, value is counts
urn_complaints_dict = {}
for i in range(1, 11):
    urn_complaints_dict[i] = []
# for each row in polya_urn_results, get the list of Number of Complaints, then get the list of Counts, then map them to the dictionary
for index, row in polya_urn_results.iterrows():
    # get list of number of complaints
    complaints = row['Number of Complaints']
    # get list of counts
    counts = row['Counts']
    # map them to the dictionary
    for i in range(len(complaints)):
        if complaints[i] < 10:
            urn_complaints_dict[complaints[i]].append(counts[i])
        else:
            urn_complaints_dict[10].append(counts[i])

# if the list length is not equal to num_simulations, then add 0s to the list until it is equal to num_simulations
for key in urn_complaints_dict:
    if len(urn_complaints_dict[key]) != num_simulations:
        urn_complaints_dict[key] = urn_complaints_dict[key] + \
            [0] * (num_simulations - len(urn_complaints_dict[key]))

# get the average of each list in the dictionary
urn_avg_complaints_dict = {}
for key in urn_complaints_dict:
    urn_avg_complaints_dict[key] = np.mean(urn_complaints_dict[key])

# get the 95% confidence interval of each list in the dictionary
upper_urn_ci_complaints_dict = {}
lower_urn_ci_complaints_dict = {}
for key in urn_complaints_dict:
    # 95% confidence interval using quantile
    upper_urn_ci_complaints_dict[key] = np.quantile(
        urn_complaints_dict[key], 0.975)
    lower_urn_ci_complaints_dict[key] = np.quantile(
        urn_complaints_dict[key], 0.025)

# plot curve
# Number of Complaints are on the x-axis, Counts are on the y-axis
fig = go.Figure()
fig.add_trace(go.Scatter(x=list(urn_avg_complaints_dict.keys()), y=list(
    urn_avg_complaints_dict.values()), mode='lines', name='Polya Urn Model Results'))
# add line with color
fig.add_trace(go.Scatter(x=list(upper_urn_ci_complaints_dict.keys()), y=list(upper_urn_ci_complaints_dict.values(
)), mode='lines', name='Polya Urn Model 95% Confidence Interval', line=dict(color='rgb(66, 81, 245)', dash='dash')))
fig.add_trace(go.Scatter(x=list(lower_urn_ci_complaints_dict.keys()), y=list(lower_urn_ci_complaints_dict.values()), mode='lines',
              name='Polya Urn Model 95% Confidence Interval', line=dict(color='rgb(66, 81, 245)', dash='dash'), fill='tonexty', fillcolor='rgba(66, 81, 245,0.2)'))
fig.add_trace(go.Scatter(
    x=officer_counts[0], y=officer_counts[1], mode='lines', name='Data'))
fig.update_layout(title_text='Polya Urn Model Results')
fig.show()

# plot curve
# Number of Complaints are on the x-axis, Counts are on the y-axis
fig = go.Figure()
fig.add_trace(go.Scatter(x=list(perm_avg_complaints_dict.keys()), y=list(
    perm_avg_complaints_dict.values()), mode='lines', name='Permutation Test Results'))
# add line with color
fig.add_trace(go.Scatter(x=list(upper_perm_ci_complaints_dict.keys()), y=list(upper_perm_ci_complaints_dict.values(
)), mode='lines', name='Permutation Test 95% Confidence Interval', line=dict(color='rgb(235, 52, 58)', dash='dash')))
fig.add_trace(go.Scatter(x=list(lower_perm_ci_complaints_dict.keys()), y=list(lower_perm_ci_complaints_dict.values()), mode='lines',
              name='Permutation Test 95% Confidence Interval', line=dict(color='rgb(235, 52, 58)', dash='dash'), fill='tonexty', fillcolor='rgba(235, 52, 58,0.2)'))
fig.add_trace(go.Scatter(x=list(urn_avg_complaints_dict.keys()), y=list(
    urn_avg_complaints_dict.values()), mode='lines', name='Polya Urn Model Results'))
# add line with color
fig.add_trace(go.Scatter(x=list(upper_urn_ci_complaints_dict.keys()), y=list(upper_urn_ci_complaints_dict.values(
)), mode='lines', name='Polya Urn Model 95% Confidence Interval', line=dict(color='rgb(66, 81, 245)', dash='dash')))
fig.add_trace(go.Scatter(x=list(lower_urn_ci_complaints_dict.keys()), y=list(lower_urn_ci_complaints_dict.values()), mode='lines',
              name='Polya Urn Model 95% Confidence Interval', line=dict(color='rgb(66, 81, 245)', dash='dash'), fill='tonexty', fillcolor='rgba(66, 81, 245,0.2)'))
fig.add_trace(go.Scatter(
    x=officer_counts[0], y=officer_counts[1], mode='lines', name='Data'))
fig.update_layout(title_text='Combined Results')
fig.show()


# make the perm_avg_complaints_dict into a dataframe, then export to csv
perm_avg_complaints_df = pd.DataFrame.from_dict(
    perm_avg_complaints_dict, orient='index')
perm_avg_complaints_df.to_csv('perm_avg_complaints_df.csv')

# make the urn_avg_complaints_dict into a dataframe, then export to csv
urn_avg_complaints_df = pd.DataFrame.from_dict(
    urn_avg_complaints_dict, orient='index')
urn_avg_complaints_df.to_csv('urn_avg_complaints_df.csv')
