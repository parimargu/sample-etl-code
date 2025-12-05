import csv
import os
import random

def generate_data():
    departments = ['Admin', 'HR', 'Finance', 'IT']
    data_dir = "data/raw"
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    filename = os.path.join(data_dir, "documents.csv")
    
    print(f"Generating sample data in {filename}...")
    
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['doc_id', 'source_text', 'department']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for i in range(1, 21): # 20 documents
            dept = random.choice(departments)
            doc_id = f"{dept}_{i}"
            
            # Generate some dummy text
            text = f"This is a confidential document for {dept} department. " \
                   f"It contains important information regarding internal policies. " \
                   f"Please review carefully. Document ID: {doc_id}. " \
                   f"End of document."
            
            # Add some noise/URLs for preprocessing test
            if i % 3 == 0:
                text += " Visit https://internal.portal for more info."
            
            writer.writerow({
                'doc_id': doc_id, 
                'source_text': text,
                'department': dept
            })
            
    print("Data generation complete.")

if __name__ == "__main__":
    generate_data()
