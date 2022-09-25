# https://www.youtube.com/watch?v=oAxR4jtPYaU&ab_channel=ClairSullivan
# from neo4j import GraphDatabase
from py2neo import Graph
import pandas as pd

url = "bolt://localhost:7687"
pwd = "beat_and_officers"

unique_officers = pd.read_csv(
    "file:///Users/jeremyhudsonchan/Library/Application Support/Neo4j Desktop/Application/relate-data/projects/project-e29b7268-ed54-46aa-8b23-04625787f4df/unique_officers.csv")

# connect to the database
graph = Graph(url, auth=("neo4j", pwd), name ="officers-and-beats")

# add officers to the database
# OfficerID,OfficerFirst,OfficerLast,Gender,Race,ApptDate,Unit,Rank,Star,Age,Beat
for index, row in unique_officers.iterrows():
    OfficerID = row["OfficerID"]
    OfficerFirst = row["OfficerFirst"]
    OfficerLast = row["OfficerLast"]
    Gender = row["Gender"]
    Race = row["Race"]
    ApptDate = row["ApptDate"]
    Unit = row["Unit"]
    Rank = row["Rank"]
    Star = row["Star"]
    Age = row["Age"]
    Beat = int(row["Beat"])
    # create node using each row
    graph.run(
        "CREATE (:OFFICER {OfficerID: $OfficerID, OfficerFirst: $OfficerFirst, OfficerLast: $OfficerLast, Gender: $Gender, Race: $Race, ApptDate: $ApptDate, Unit: $Unit, Rank: $Rank, Star: $Star, Age: $Age, Beat: $Beat})", OfficerID=OfficerID, OfficerFirst=OfficerFirst, OfficerLast=OfficerLast, Gender=Gender, Race=Race, ApptDate=ApptDate, Unit=Unit, Rank=Rank, Star=Star, Age=Age, Beat=Beat)

print("Created_All_Officers")
# get unique beats from dataframe then convert it to integers
unique_beats = pd.unique(unique_officers["Beat"])
unique_beats = unique_beats.astype(int)
# convert to native int
unique_beats = unique_beats.tolist()
# print(unique_beats[0].dtype)

# create beat node in graph
for beat in unique_beats:
    graph.run("CREATE (:BEAT {Beat: $beat})", beat=beat)

print("Created_All_Beats")
