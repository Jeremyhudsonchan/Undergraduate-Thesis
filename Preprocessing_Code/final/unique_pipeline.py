import pandas as pd
import time

df = pd.read_csv(
    "/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Code/Undergraduate-Thesis/Preprocessing_Code/final/data/proportions.csv", low_memory=False)
profile_df = pd.read_csv(
    "/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/2000-2016/officer_profile.csv", low_memory=False)

# print(df.head())

# print(df.columns)

# df_grouped = df.groupby("CRID")

# print(profile_df.columns)

# drop Star column
profile_df = profile_df.drop(["Unit", "Star"], axis=1)

# get list of unique officers from df
officer_list = pd.unique(df["OfficerID"])

start_time = time.time()
# drop officers who are not in df
profile_df = profile_df[profile_df["OfficerID"].isin(officer_list)]

# Add Beat to each officer in profile_df
profile_df["Beat"] = 0
for index, row in profile_df.iterrows():
    if row["OfficerID"] in officer_list:
        profile_df.loc[index, "Beat"] = df.loc[df["OfficerID"]
                                               == row["OfficerID"], "Beat"].iloc[0]

# remove duplicates
profile_df = profile_df.drop_duplicates(subset="OfficerID")

profile_df.to_csv(
    "/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Code/Undergraduate-Thesis/Preprocessing_Code/final/data/perm_unique_officers.csv", index=False)
end_time = time.time()
print('Runtime: ', end_time - start_time)
# print(profile_df.head())

# Note Complaint Register ID Number (CRID)
# allegations_officers_df = df[["OfficerID", "OfficeFirst", "OfficerLast"]]
# allegations_officers_df.head()

# officers = pd.unique(allegations_officers_df["OfficerID"]).shape

# officers_2 = pd.unique(profile_df["OfficerID"]).shape

# unique_officers = profile_df.drop_duplicates(subset="OfficerID")

# # Make a new column in unique_officers called "Beat" where the value is a float
# unique_officers["Beat"] = 0
# # unique_officers["Beat"] = unique_officers["Beat"].astype(float)

# for index, row in unique_officers.iterrows():
#     # check if officer in df, if not then skip
#     if row["OfficerID"] not in pd.unique(df["OfficerID"]):
#         continue
#     unique_officers.loc[index, "Beat"] = df.loc[df["OfficerID"]
#                                                 == row["OfficerID"], "Beat"].iloc[0]

# # Load Excel Sheets using ExcelFile
# zero = pd.ExcelFile(
#     '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/Website/2000_allegation.xlsx')
# one = pd.ExcelFile(
#     '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis//Data/Website/2001_allegation.xlsx')
# two = pd.ExcelFile(
#     '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/Website/2002_allegation.xlsx')
# three = pd.ExcelFile(
#     '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/Website/2003_allegation.xlsx')
# four = pd.ExcelFile(
#     '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/Website/2004_allegation.xlsx')
# five = pd.ExcelFile(
#     '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/Website/2005_allegation.xlsx')
# six = pd.ExcelFile(
#     '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/Website/2006_allegation.xlsx')
# seven = pd.ExcelFile(
#     '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/Website/2007_allegation.xlsx')
# eight = pd.ExcelFile(
#     '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/Website/2008_allegation.xlsx')
# nine = pd.ExcelFile(
#     '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/Website/2009_allegation.xlsx')
# ten = pd.ExcelFile(
#     '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/Website/2010_allegation.xlsx')
# eleven = pd.ExcelFile(
#     '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis//Data/Website/2011_allegation.xlsx')
# twelve = pd.ExcelFile(
#     '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/Website/2012_allegation.xlsx')
# thirteen = pd.ExcelFile(
#     '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/Website/2013_allegation.xlsx')
# fourteen = pd.ExcelFile(
#     '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/Website/2014_allegation.xlsx')
# fifteen = pd.ExcelFile(
#     '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/Website/2015_allegation.xlsx')
# sixteen = pd.ExcelFile(
#     '/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/Website/2016_allegation.xlsx')

# # Select excel sheet allegations from excel file
# allegations_00 = zero.parse('Allegations')
# allegations_01 = one.parse('Allegations')
# allegations_02 = two.parse('Allegations')
# allegations_03 = three.parse('Allegations')
# allegations_04 = four.parse('Allegations')
# allegations_05 = five.parse('Allegations')
# allegations_06 = six.parse('Allegations')
# allegations_07 = seven.parse('Allegations')
# allegations_08 = eight.parse('Allegations')
# allegations_09 = nine.parse('Allegations')
# allegations_10 = ten.parse('Allegations')
# allegations_11 = eleven.parse('Allegations')
# allegations_12 = twelve.parse('Allegations')
# allegations_13 = thirteen.parse('Allegations')
# allegations_14 = fourteen.parse('Allegations')
# allegations_15 = fifteen.parse('Allegations')
# allegations_16 = sixteen.parse('Allegations')

# # combine allegations from 2010-2016 into one csv
# allegations = pd.concat([allegations_00, allegations_01, allegations_02, allegations_03, allegations_04, allegations_05, allegations_06, allegations_07, allegations_08, allegations_09, allegations_10, allegations_11, allegations_12, allegations_13,
#                         allegations_14, allegations_15, allegations_16], ignore_index=True)

# allegations_count = allegations.groupby(
#     'OfficerID').size().reset_index(name='allegations')
# unique_officers['num_allegations'] = unique_officers['OfficerID'].map(
#     allegations_count.set_index('OfficerID')['allegations'])

# unique_officers = unique_officers.dropna(subset=["Beat"])
# unique_officers = unique_officers[unique_officers.Beat != 0.0]

# print(unique_officers.head())

# unique_officers.to_csv(
#     "/Users/jeremyhudsonchan/Dropbox/Files/Boston_College_Courses/Thesis/Data/Processed/unique_officers.csv", index=False)
