import pandas as pd

# Update this path to the CSV you downloaded from Kaggle
file_path = "datasets/customer_support_tickets.csv"

df = pd.read_csv(file_path)

# Keep the columns needed for classification
required_columns = [
    "Ticket Description",
    "Ticket Type",
    "Product Purchased",
    "Ticket Priority",
]

# Check that the expected columns exist
missing = [column for column in required_columns if column not in df.columns]
if missing:
    raise ValueError(
        f"Missing expected columns: {missing}\n"
        f"Columns found: {df.columns.tolist()}"
    )

# Keep and rename columns for clarity
data = df[required_columns].copy()
data = data.rename(columns={
    "Ticket Description": "request_text",
    "Ticket Type": "issue_category",
    "Product Purchased": "product",
    "Ticket Priority": "severity",
})

# Remove rows missing the request text or labels
data = data.dropna(subset=[
    "request_text",
    "issue_category",
    "product",
    "severity",
])

# Remove accidental whitespace
for column in data.columns:
    data[column] = data[column].astype(str).str.strip()

# Remove blank values
data = data[
    (data["request_text"] != "") &
    (data["issue_category"] != "") &
    (data["product"] != "") &
    (data["severity"] != "")
].reset_index(drop=True)

print(data.head())
print(f"\nRows ready for classification: {len(data)}")
print("\nSeverity labels:")
print(data["severity"].value_counts())