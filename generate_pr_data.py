import csv  

# Define the CSV file name  
csv_filename = "pull_requests.csv"  

# Define the headings  
headers = ["Pull Request Size", "Time to First Review (mins)", "Pull Request Duration (mins)", "Reviewers"]  

# Sample dummy data  
data = [  
    [120, 30, 180, "Alice, Bob"],  
    [300, 45, 240, "Charlie"],  
    [80, 20, 90, "David, Eve"],  
    [500, 60, 360, "Frank, Grace"],  
]  

# Write to CSV  
with open(csv_filename, mode="w", newline="") as file:  
    writer = csv.writer(file)  
    writer.writerow(headers)  # Write the headers  
    writer.writerows(data)  # Write the sample data  

print(f"CSV file '{csv_filename}' has been created successfully!")  
