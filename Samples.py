import pandas as pd

df  = pd.read_csv('dataset.csv')
# Define conditions based on common dietary guidelines
def determine_condition(row):
    # General criteria for each condition
    if (row['ProteinContent'] >= 10 and row['FiberContent'] >= 3 and row['CholesterolContent'] <= 200):
        return "Pregnancy"
    elif (row['SugarContent'] <= 5 and row['CarbohydrateContent'] <= 45 and row['FiberContent'] >= 3):
        return "Diabetes"
    elif (row['SaturatedFatContent'] <= 3 and row['CholesterolContent'] <= 200 and row['SodiumContent'] <= 400):
        return "Heart Disease"
    else:
        return "Normal"

# Apply the function to create the new 'Condition' column
df['Condition'] = df.apply(determine_condition, axis=1)

# Display the updated dataset with the new 'Condition' column
df[['Name', 'ProteinContent', 'FiberContent', 'CholesterolContent', 
    'SugarContent', 'CarbohydrateContent', 'SaturatedFatContent', 
    'SodiumContent', 'Condition']].head()

df.info()

print(df.head)

