import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

destinations = pd.read_csv('../data/Destinations.csv')

dtest = destinations.head(100).drop(columns=['Coordinate','Source', 'Google Maps Rating', 'Google Reviews (Count)'])
print(dtest)
ddocuments = []
for index, row in dtest.iterrows():
    document = {
        "Place": row["Place"],
        "Location": row["Location"],
        # "Google Maps Rating": row["Google Maps Rating"],
        # "Google Reviews (Count)": row["Google Reviews (Count)"],
        "Description": row["Description"],
        "Tourism/Visitor Fee (approx in USD)": row["Tourism/Visitor Fee (approx in USD)"]
    }
    ddocuments.append(document)

with open("../data/destinations.py", "w") as file:
    for i, doc in enumerate(ddocuments):
        file.write(f"DESTINATION_{i + 1} = {doc}\n")

print("Documents exported to destinations.py successfully.")