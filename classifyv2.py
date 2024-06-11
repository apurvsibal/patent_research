import csv
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Load environment variables
azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

# Initialize AzureOpenAI client
client = AzureOpenAI(
    api_key=azure_openai_api_key,
    azure_endpoint=azure_openai_endpoint,
    api_version = "2024-02-01"
    #location="eastus2",
    #model="gpt-3.5"
)

# Function to classify patent summary text
def classify_patent(summary_text,model_name="textproject35"):
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a automobile safety patent expert. This patent is about " + summary_text[0:600]},
            {"role": "user", "content": "Classify if the patent is (a) related to automotive safety with a confidence score between 0 to 1 upto two decimal places like 0.01 or 0.98. Only reply with a number. If the patent is not related to automobile safety then reply with a number closer to 0 and if it is related to automobile safety then reply with a number greater than 0. What is the confidence score that this patent is related to automobile safety: \n\n"}
        ],
        max_tokens = 4,
        temperature = 0
    )
    classification = response.choices[0].message.content
    return classification

'''
# Read CSV file and classify each patent
with open("patents_with_summary.csv", "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        patent_id = row["patent_id"]
        print(patent_id)
        summary_text = row["summary_text"]
        classification_result = classify_patent(summary_text)
        print(f"Patent ID: {patent_id}, Classification: {classification_result}")
        break
'''

input_file = "patents_with_summary.csv"
output_file = "patents_automobile_score.csv"
n = 600  # Set the number of rows to process
model_to_use = "textproject35"#"textproject35" #textproject4
with open(input_file, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames + ["classification_result3"] + ["classification_result4"]
    with open(output_file, "w", encoding="utf-8", newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        row_count = 0
        for row in reader:
            if row_count >= n:
                break
            try:
                patent_id = row["patent_id"]
                summary_text = "Organization" + row["organization"] + "\n\n" + row["summary_text"]
                classification_result3 = classify_patent(summary_text,"textproject35")
                print(classification_result3)
                classification_result4 = classify_patent(summary_text,"textproject4")
                print(classification_result4)
            except Exception as e:
                classification_result3 = "error"
                classification_result4 = "error"
                print(f"Error processing patent ID {row['patent_id']}: {e}")                
            row["classification_result3"] = classification_result3
            row["classification_result4"] = classification_result4
            writer.writerow(row)
            row_count += 1

print(f"Processed {row_count} rows and saved the results to {output_file}.")

