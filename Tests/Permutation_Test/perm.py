import pandas as pd
import plotly.express as px

df = pd.read_csv(
    '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Code/Undergraduate-Thesis/Preprocessing_Code/final/data/proportions.csv', low_memory=False)
officers = pd.read_csv(
    '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Code/Undergraduate-Thesis/Preprocessing_Code/final/data/perm_unique_officers.csv', low_memory=False)

# group by CRID
df_grouped = df.groupby('CRID')

# find number of groups that have more than one officer
print(len(df_grouped.filter(lambda x: len(x) > 1)))

# permutation test loop 1000 simulations
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
        officers_sample = officers.sample(n=num_officers, replace=False)
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

# plot new_df_vc using plotly, also include 95% confidence interval
# title is Perumtation Test Results
fig = px.line(new_df_vc, x=new_df_vc.index, y=new_df_vc.values, labels={
              'x': 'Number of Allegations', 'y': 'Number of Officers'})
fig.add_scatter(x=conf_intv.index, y=conf_intv[0.025],
                mode='lines', name='95% Confidence Interval')
fig.add_scatter(x=conf_intv.index, y=conf_intv[0.975],
                mode='lines', name='95% Confidence Interval')
fig.update_layout(title_text='Permutation Test Results')
fig.show()

# plot both on same graph
fig = px.line(df_vc, x=df_vc.index, y=df_vc.values, labels={
    'x': 'Number of Allegations', 'y': 'Number of Officers'})
fig.add_scatter(x=new_df_vc.index, y=new_df_vc.values,
                mode='lines', name='Permutation Test Results')
fig.add_scatter(x=conf_intv.index, y=conf_intv[0.025],
                mode='lines', name='95% Confidence Interval')
fig.add_scatter(x=conf_intv.index, y=conf_intv[0.975],
                mode='lines', name='95% Confidence Interval')
fig.update_layout(title_text='Original vs Permutation Test Results')
fig.show()


# df_vc.to_csv('/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Code/Undergraduate-Thesis/Tests/Results/original.csv')
# new_df_vc.to_csv(
# '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Code/Undergraduate-Thesis/Tests/Results/permutation_test.csv')
