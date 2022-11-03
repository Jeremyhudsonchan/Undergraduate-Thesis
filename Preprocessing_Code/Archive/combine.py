# load excel files
import pandas as pd

# Load Excel Sheets using ExcelFile
ten = pd.ExcelFile('Data/Website/2010_allegation.xlsx')
eleven = pd.ExcelFile('Data/Website/2011_allegation.xlsx')
twelve = pd.ExcelFile('Data/Website/2012_allegation.xlsx')
thirteen = pd.ExcelFile('Data/Website/2013_allegation.xlsx')
fourteen = pd.ExcelFile('Data/Website/2014_allegation.xlsx')
fifteen = pd.ExcelFile('Data/Website/2015_allegation.xlsx')
sixteen = pd.ExcelFile('Data/Website/2016_allegation.xlsx')

# Select excel sheet allegations from excel file
allegations_10 = ten.parse('Allegations')
allegations_11 = eleven.parse('Allegations')
allegations_12 = twelve.parse('Allegations')
allegations_13 = thirteen.parse('Allegations')
allegations_14 = fourteen.parse('Allegations')
allegations_15 = fifteen.parse('Allegations')
allegations_16 = sixteen.parse('Allegations')

# combine allegations from 2010-2016 into one csv
allegations = pd.concat([allegations_10, allegations_11, allegations_12, allegations_13,
                        allegations_14, allegations_15, allegations_16], ignore_index=True)
# save to csv
allegations.to_csv('Data/allegations.csv', index=False)

# Select excel sheet Police Witnesses from excel file
police_witnesses_10 = ten.parse('Police Witnesses')
police_witnesses_11 = eleven.parse('Police Witnesses')
police_witnesses_12 = twelve.parse('Police Witnesses')
police_witnesses_13 = thirteen.parse('Police Witnesses')
police_witnesses_14 = fourteen.parse('Police Witnesses')
police_witnesses_15 = fifteen.parse('Police Witnesses')
police_witnesses_16 = sixteen.parse('Police Witnesses')

# combine police_witnesses from 2010-2016 into one csv
police_witnesses = pd.concat([police_witnesses_10, police_witnesses_11, police_witnesses_12, police_witnesses_13,
                              police_witnesses_14, police_witnesses_15, police_witnesses_16], ignore_index=True)
# combine police_witnesses from 2010-2016 into one csv
police_witnesses.to_csv('Data/police_witnesses.csv', index=False)

# Get Complaining Witnesses from excel file
complaining_witnesses_10 = ten.parse('Complaining Witnesses')
complaining_witnesses_11 = eleven.parse('Complaining Witnesses')
complaining_witnesses_12 = twelve.parse('Complaining Witnesses')
complaining_witnesses_13 = thirteen.parse('Complaining Witnesses')
complaining_witnesses_14 = fourteen.parse('Complaining Witnesses')
complaining_witnesses_15 = fifteen.parse('Complaining Witnesses')
complaining_witnesses_16 = sixteen.parse('Complaining Witnesses')

# combine complaining_witnesses from 2010-2016 into one csv
complaining_witnesses = pd.concat([complaining_witnesses_10, complaining_witnesses_11, complaining_witnesses_12, complaining_witnesses_13,
                                   complaining_witnesses_14, complaining_witnesses_15, complaining_witnesses_16], ignore_index=True)
# save to csv
complaining_witnesses.to_csv('Data/complaining_witnesses.csv', index=False)


# Select Excel Sheet Officer Profile from excel file
officer_profile_10 = ten.parse('Officer Profile')
officer_profile_11 = eleven.parse('Officer Profile')
officer_profile_12 = twelve.parse('Officer Profile')
officer_profile_13 = thirteen.parse('Officer Profile')
officer_profile_14 = fourteen.parse('Officer Profile')
officer_profile_15 = fifteen.parse('Officer Profile')
officer_profile_16 = sixteen.parse('Officer Profile')

# Combine Officer Profile from 2010-2016 into one csv
officer_profile = pd.concat([officer_profile_10, officer_profile_11, officer_profile_12, officer_profile_13,
                            officer_profile_14, officer_profile_15, officer_profile_16], ignore_index=True)
# combine all officer progiles into one csv
officer_profile.to_csv('Data/officer_profile.csv', index=False)
