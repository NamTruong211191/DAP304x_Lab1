import pandas as pd
import re
import numpy as np
#declare the variables
count_no_good=0 # count invalid line
answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
answer_key_list = re.split(",", answer_key)
expected_columns = 27  # df index + N# + 25 answers 
    
filename = input("Enter a filename: ")
try:
    with open(filename +".txt","r") as file:
        lines = file.readlines()
        print("Successfully opened " + filename +".txt")
except FileNotFoundError:
    print("File can not be found")
    quit()
   
# Convert lines to DataFrame
data = [line.strip().split(",") for line in lines]
df = pd.DataFrame(data)
 
for row_tuple in df.itertuples():
    # Check N# format
    match = re.match(r"^[N]\d{8}", row_tuple[1])
    if match:
        # In case N# format is correct, check the total number of answers
        # If the length of row_tuple wthout None value is equal to expected_columns, process the scoring
        if len(row_tuple)-row_tuple.count(None) == expected_columns:
            score = 0
            # compare the answer list to the answer key list
            for i in range(expected_columns - 2):  # -2 for N# and index
                # Right answer: +4, wrong answer: -1, skipped answer: 0
                if answer_key_list[i] == row_tuple[i+2]:
                    score += 4
                elif row_tuple[i+2] == "":
                    score += 0
                else: score += -1
            # Add score to the DataFrame
            df.at[row_tuple.Index, 'Score'] = score
        else:
            # in case the total answer not equal to 25, report invalid line
            count_no_good += 1  
            print("Invalid data (does not contain 25 answers): " 
                      + str(len(row_tuple)-row_tuple.count(None)))
            print(list(row_tuple))
    else:
        # in case the N# format is incorrect, report the invalid line
        count_no_good += 1
        print("Invalid data (invalid N#):")
        print(list(row_tuple))
# Print agg results

print("Total invalid lines of " + filename + " :" + str(count_no_good))
print("Total valid lines of " + filename + " :" + str(len(df) - count_no_good))
hs_student = df[df['Score'] > 80].shape[0]
print("Total student of high scores: " + str(hs_student))
median_score = round(df['Score'].median(),3)
print("Median score of " + filename + " :" + str(median_score))
average_score = round(df['Score'].mean(),3)
print("Average score of " + filename + " :" + str(average_score))
print("Maximum score of " + filename + " :" + str(df['Score'].max()))
print("Minimum score of " + filename + " :" + str(df['Score'].min()))
range_score = df['Score'].max() - df['Score'].min()
print("Range of score of " + filename + " :" + str(range_score))
print("Standard deviation of score of " + filename + " :" + str(round(df['Score'].std(),3)))


# Save the DataFrame to a new CSV file with only N# column and Score columns
df = df.iloc[:, [0, -1]]  # Select the first column (N#) and the last column (Score)
df.columns = ['StudentNo', 'Score']  # Rename columns for clarity
df = df.dropna()  # Drop rows with NaN values in Score  
output_filename = filename + "_graded_test.txt"
df.to_csv(output_filename, index=False)