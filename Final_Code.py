import pandas as pd
import time

start_time = time.time()

# Load dataset
original_data = pd.read_csv('Titanic-Dataset.csv')

# Rename columns with meaningful full names
original_data.rename(columns={
    'PassengerId': 'Passenger_ID',
    'Survived': 'Survival_Status',
    'Pclass': 'Passenger_Class',
    'Name': 'Full_Name',
    'Sex': 'Gender',
    'Age': 'Age_Years',
    'SibSp': 'Sibling_Spouse_Count',
    'Parch': 'Parent_Child_Count',
    'Ticket': 'Ticket_Number',
    'Fare': 'Fare_Price',
    'Cabin': 'Cabin_Number',
    'Embarked': 'Embarked_Town'
}, inplace=True)

# Map Survival_Status numeric to text values
original_data['Survival_Status'] = original_data['Survival_Status'].map({0: 'Not Survived', 1: 'Survived'})

# Convert Passenger_Class numeric to descriptive strings
passenger_class_map = {1: '1st', 2: '2nd', 3: '3rd'}
original_data['Passenger_Class'] = original_data['Passenger_Class'].map(passenger_class_map)

# Map Embarked codes to full town names
port_mapping = {'C': 'Cherbourg', 'Q': 'Queenstown', 'S': 'Southampton'}
original_data['Embarked_Town_Full'] = original_data['Embarked_Town'].map(port_mapping)

# Fill missing Embarked_Town_Full with mode (most frequent port)
original_data['Embarked_Town_Full'] = original_data['Embarked_Town_Full'].fillna(original_data['Embarked_Town_Full'].mode()[0])

# Fill missing Cabin_Number values cycling through a list of clubbed example cabins
cabin_list = ['C85', 'B28', 'E24', 'D10', 'A5', 'F33', 'G6', 'B57', 'C123', 'E46']
filled_cabins = []
idx = 0
for cabin in original_data['Cabin_Number']:
    if pd.isna(cabin):
        filled_cabins.append(cabin_list[idx % len(cabin_list)])
        idx += 1
    else:
        filled_cabins.append(cabin)
original_data['Cabin_Number_Filled'] = filled_cabins

# Drop columns not required for ML (you can keep Full_Name if you want)
cleaned_data = original_data.drop(columns=['Ticket_Number', 'Embarked_Town'])

# Rename the descriptive Embarked_Town_Full to Embarked_Town for clarity
cleaned_data.rename(columns={'Embarked_Town_Full': 'Embarked_Town'}, inplace=True)

# Fill missing Age values with median
cleaned_data['Age_Years'] = cleaned_data['Age_Years'].fillna(cleaned_data['Age_Years'].median())

# Keep Gender as categorical text, no mapping here needed

# Reorder to have Passenger_ID as first column for easy reference
cols = list(cleaned_data.columns)
cols.remove('Passenger_ID')
cols = ['Passenger_ID'] + cols
cleaned_data = cleaned_data[cols]

# Save to final cleaned CSV file
cleaned_data.to_csv('Final-Titanic-Dataset.csv', index=False)

end_time = time.time()
print(f"Elapsed time for data cleaning: {end_time - start_time:.4f} seconds")
