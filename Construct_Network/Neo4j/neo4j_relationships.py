from py2neo import Graph
import pandas as pd

url = "bolt://localhost:7687"
pwd = "beat_and_officers"

unique_officers = pd.read_csv(
    "file:///Users/jeremyhudsonchan/Library/Application Support/Neo4j Desktop/Application/relate-data/projects/project-e29b7268-ed54-46aa-8b23-04625787f4df/unique_officers.csv")

graph = Graph(url, auth=("neo4j", pwd), name="officers-and-beats-update")

# I want to create a relationship between each officer and their beat
# If office is assigned to beat 1, then create a relationship between the officer and beat 1
# loop through each row in the dataframe
for index, row in unique_officers.iterrows():
    OfficerID = row["OfficerID"]
    Beat = int(row["Beat"])
    # create relationship between officer and beat
    graph.run(
        "MATCH (o:OFFICER {OfficerID: $OfficerID}), (b:BEAT {Beat: $Beat}) CREATE (o)-[:ASSIGNED_TO]->(b)", OfficerID=OfficerID, Beat=Beat)
    print(index, row)

print("Created_All_Relationships")
