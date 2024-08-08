import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

review = pd.read_csv("data/Reviews.csv")

test = review.head(100).drop(columns=['Id', 'UserId','HelpfulnessNumerator',   
                                   'HelpfulnessDenominator',
                                   'Score', 'Time', 'Summary'])

documents = []
for index, row in test.iterrows():
    document = {
        "ProductId": row["ProductId"],
        "Text": row["Text"],
        "ProfileName": row["ProfileName"],
    }
    documents.append(document)

with open("../data/documents.py", "w") as file:
    for i, doc in enumerate(documents):
        file.write(f"DOCUMENT_{i + 1} = {doc}\n")

print("Documents exported to documents.py successfully.")