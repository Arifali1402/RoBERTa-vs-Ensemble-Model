import pandas as pd
from sentiment import predict_sentiment
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Read the test.csv file with tweets and labels
test_data = pd.read_csv("./twitter_validation.csv")
# test_data = pd.read_csv("./test.csv")

print("\n")
test_data.info()
print("\n")
test_data.head(5)
print("\n")

# Mapping for converting the sentiment to numeric labels
sentiment_mapping = {
    'positive': 1,
    'negative': -1,
    'neutral': 0
}

# Lists to store the predicted labels and true labels
y_true = []
y_pred = []

# Function to convert string labels to numeric values
def convert_label_to_numeric(label):
    if isinstance(label, str):
        # Convert string labels to numeric using sentiment_mapping
        return sentiment_mapping.get(label.lower(), 0)  # Default to 0 (neutral) if not found
    return label  # Return the label as is if it's already numeric

# Iterate over each tweet in the test data
for _, row in test_data.iterrows():
    tweet_text = row["tweets"]
    true_label = row["label"]

    try:
        # Convert true_label to numeric if it's a string
        true_label_numeric = convert_label_to_numeric(true_label)

        # Predict sentiment for the tweet
        sentiment = predict_sentiment(tweet_text)

        # Convert predicted sentiment to numeric value using the sentiment_mapping
        predicted_label = sentiment_mapping.get(sentiment, 0)  # Default to 0 (neutral) if not found

        # Append true label and predicted label to lists
        y_true.append(true_label_numeric)
        y_pred.append(predicted_label)

    except Exception as e:
        print(f"Error predicting sentiment for tweet: {e}")

# Calculate the metrics
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)

# Print the results
print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")
print()












import pandas as pd
from sentiment import predict_sentiment

def predict_and_save_sentiments(input_csv: str, output_csv: str):
    """
    Reads a CSV file containing tweets, predicts the sentiment for each tweet,
    and saves the result to a new CSV file with an additional sentiment column.
    If the output CSV already exists, it will be overwritten.
    
    Args:
    - input_csv (str): Path to the input CSV file (tweets.csv).
    - output_csv (str): Path to the output CSV file (output.csv).
    """
    # Read the tweets from the input CSV file
    tweets_data = pd.read_csv(input_csv)

    # List to store predicted sentiments
    sentiments = []

    # Iterate over each tweet in the input data
    for _, row in tweets_data.iterrows():
        tweet_text = row["Text"]

        try:
            # Predict sentiment for the tweet
            sentiment = predict_sentiment(tweet_text)

            # Append the predicted sentiment to the list
            sentiments.append(sentiment)

        except Exception as e:
            print(f"Error predicting sentiment for tweet: {e}")
            sentiments.append("Error")  # In case of error, mark as 'Error'

    # Add the predicted sentiment as a new column in the DataFrame
    tweets_data["sentiment"] = sentiments

    # Save the updated DataFrame to the output CSV file (it will overwrite if it exists)
    tweets_data.to_csv(output_csv, index=False)
    print(f"Output saved to {output_csv}")

# Usage: Calling the function to read tweets.csv, predict sentiment, and save to output.csv
predict_and_save_sentiments("./tweets.csv", "./output.csv")


print()