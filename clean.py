import re
import pandas as pd
# Function to clean the text
def clean_text(text):
    text = str(text).lower()  # Convert to lowercase and ensure text is a string
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove special characters, numbers, and punctuation
    return text

# Apply the cleaning function to the 'Title' and 'Text' columns

df = pd.read_csv("arsenalFC.csv")
df['cleaned_title'] = df['Title'].apply(clean_text)
df['cleaned_text'] = df['Text'].apply(clean_text)

# Display the first few cleaned rows
head = df[['Title', 'cleaned_title', 'Text', 'cleaned_text']].head()
text = df["Text"]
length = len(text.to_string())
print(length)
# text.to_csv("clean.csv")

