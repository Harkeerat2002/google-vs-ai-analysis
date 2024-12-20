import pandas as pd
import numpy as np
import pickle
import csv

# open new_data.csv and predict relevance for each row
df = pd.read_csv('./data/new_data.csv', delimiter=',')

# Load the trained CountVectorizer and LogisticRegression objects from a file
with open('model.pkl', 'rb') as f:
    vectorizer, model = pickle.load(f)


def predict_relevance(model, vectorizer, query, snippet):
    # Preprocess the input data
    input_data = [query + ' ' + snippet]
    input_data = vectorizer.transform(input_data)

    # Make a prediction using the trained model
    prediction = model.predict(input_data)

    # Return the prediction (1 for relevant and 0 for not relevant)
    return prediction[0]


# Drop the source column
df = df.drop('source', axis=1)

# Create a new column for relevance
df['relevance'] = ""

# Iterate over the rows and predict the relevance
for index, row in df.iterrows():
    session_id = row['session_id']
    query = row['user_query']
    snippet = row['snippet']
    prediction = predict_relevance(model, vectorizer, query, snippet)
    # print(
    #     f"Prediction for input {index}: {prediction} (1=Relevant, 0=Not relevant)")
    df.at[index, 'relevance'] = prediction

# Save the dataframe to a new csv file
df.to_csv('./data/new_data_with_relevance.csv', index=False)

df = pd.read_csv('./data/ChatGPT-Results.csv', delimiter=',')

# Create a new column for relevance
df['relevance'] = ""


# Iterate over the rows and predict the relevance
for index, row in df.iterrows():
    query = row['query']
    snippet = row['response']
    prediction = predict_relevance(model, vectorizer, query, snippet)

    # print(
    #     f"Prediction for input {index}: {prediction} (1=Relevant, 0=Not relevant)")
    df.at[index, 'relevance'] = prediction

# Find how many are relevant and how many are not relevant


# Save the dataframe to a new csv file
df.to_csv('./data/ChatGPT-Results-with-relevance.csv', index=False)

with open('./data/ChatGPT-Results-with-relevance.csv', 'r') as f:
    reader = csv.reader(f)
    relevance = []
    for row in reader:
        relevance.append(row[2])
    
    # Drop the first value in relevance
    relevance = relevance[1:]
    # Add all the numbers in relevance
    Relevant = relevance.count('R')
    NotRelevant = relevance.count('NR')
    print(f"Relevant: {Relevant}")
    print(f"Not Relevant: {NotRelevant}")

with open('./data/new_data_with_relevance.csv', 'r') as f:
    reader = csv.reader(f)
    relevance = []
    for row in reader:
        print(row[5])
    
    # # Drop the first value in relevance
    # relevance = relevance[1:]
    # # Add all the numbers in relevance
    # Relevant = relevance.count('R')
    # NotRelevant = relevance.count('NR')
    # print(f"Relevant: {Relevant}")
    # print(f"Not Relevant: {NotRelevant}") 
