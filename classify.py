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
            {"role": "system", "content": "This patent is about " + summary_text},
            {"role": "user", "content": "Classify if the patent is (a) related to automotive safety with a confidence score between 0 to 1, (b) if related to safety, then is it related to passive safety (e.g. physical structures, seat belt) i.e. things that help protect occupants during a crash, or is it related to active safety (e.g. software systems, mirrors for blind spots) i.e. things that help occupants prevent a crash, (answer only as passive or active) and (c) if related to passive safety, is it related to protection during side impact crashes (answer as yes or no)? All the answers should be comma separated"}
        ]
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
output_file = "patents_with_classification_v2.csv"
n = 20  # Set the number of rows to process
model_to_use = "textproject35"#"textproject35" #textproject4
with open(input_file, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames + ["classification_result"]
    with open(output_file, "w", encoding="utf-8", newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        row_count = 0
        for row in reader:
            if row_count >= n:
                break
            try:
                patent_id = row["patent_id"]
                summary_text = row["summary_text"]
                classification_result = classify_patent(summary_text,model_to_use)
            except Exception as e:
                classification_result = "error"
                print(f"Error processing patent ID {row['patent_id']}: {e}")                
            row["classification_result"] = classification_result
            writer.writerow(row)
            row_count += 1

print(f"Processed {row_count} rows and saved the results to {output_file}.")

