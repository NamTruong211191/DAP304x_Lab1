# -*- coding: utf-8 -*-
"""
Created on Sat Jul 19 11:30:53 2025

@author: pd01
"""

import re

# Task 1
# Input file name, check if exist file name in directory
# If file exist then read file, if not then end code
filename = input("Enter a filename: ")
try:
    with open(filename +".txt","r") as file:
        content = file.readlines()
        print("Successfully opened " + filename +".txt")
except FileNotFoundError:
    print("File can not be found")
    quit()
    
# Task 2 + Task 3   
score_dict = {}
score_list = []
count=0 # count valid line
count_no_good=0 # count invalid line
answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
answer_key_list = re.split(",", answer_key)
for line in content:
    # Check N# format
    match = re.match(r"^[N]\d{8}", line)    
    if match:
        # In case N# format is correct, check the total number of answers
        answer_list=re.split(",", line)
        if len(answer_list) == 26:
            # in case the total answer equal to 25, process the scoring
            count += 1
            score = 0
            # compare the answer list to the answer key list
            for i in range(25):
                # Right answer: +4, wrong answer: -1, ignore answer: 0
                if answer_key_list[i] == answer_list[i+1]:
                    score += 4
                elif answer_list[i+1] == "":
                    score += 0
                else: score += -1
                #                print(answer_key_list[i] , answer_list[i+1],str(score))
            score_dict[answer_list[0]] = score
            score_list.append(score)                                 
        else:
            # in case the total answer not equal to 25, report invalid line
            count_no_good += 1  
            print("Invalid data (does not contain 25 answers): " 
                      + str(len(answer_list)-1))
            print(line)
    else:
        # in case the N# format is incorrect, report the invalid line
        count_no_good += 1
        print("Invalid data (invalid N#):")
        print(line)
        
# Print agg results
print("Total valid lines of " + filename + " :" + str(count))
print("Total invalid lines of " + filename + " :" + str(count_no_good))

hs_student = sum(1 for x in score_list if x>80)
print("Total student of high scores: " + str(hs_student))

avg_score = round(sum(score_list)/len(score_list),3)
print("Average score: " + str(avg_score))

print("Highest score: " + str(max(score_list)))
print("Lowest score: " + str(min(score_list)))
print("Range of score: " + str(max(score_list)
                               -min(score_list)))

sorted_score_list = sorted(score_list)
med_index = (len(score_list)-1)//2
if len(score_list) % 2 :
    med_score = sorted_score_list[med_index]
else: 
    med_score = (sorted_score_list[med_index] 
                 +sorted_score_list[med_index +1]) / 2
print("Median score: " + str(med_score))

# write N#,score to text file
with open(filename +"_grades.txt","w") as write_file:
    for key in score_dict:        
        write_file.write(str(key) + "," + str(score_dict[key]) + "\n")

    


