import pandas as pd
import numpy  as np

###
#OPEN FILE
print("Enter a class to grade (i.e. class1 for class1)")
name = input()
try:
    with open(name+'.txt','r') as gs:
        grades = gs.readlines()
        print("Successfully opened", name+'.txt')
        #print(grades)
except IOError:
        print("File not accessible")
print("----------------------")

###
#SCAN FILE AND ANALYSE
#Make a copy dataframe to check how many invalid lines of data have been removed
new_grades_df = grades.copy()
for grade in grades: 
            value = grade.split(",")
            length = len(value)
            #Check if line contain 26 values. If not, print then remove from copied dataframe
            if length != 26:
                corrupted_ID = value[0]
                print("Invalid line of data:", corrupted_ID, " does not contain exactly 26 values:")
                print(grade)
                new_grades_df.remove(grade)
            #Check if ID has 9 characters. If not, print then remove from copied dataframe
            id = value[0]
            id_length = len(id)
            if id_length != 9:
                corrupted_ID = value[0]
                print("Invalid line of data:", corrupted_ID, " is invalid")
                print(grade)
                new_grades_df.remove(grade)
            #Check if ID is N + 8 numbers. If not, print then remove from copied dataframe
            id_chars= list(id)
            first_chars= id_chars.pop(0)
            for char in id_chars:
                    if char.isnumeric() ==0:
                        print("Invalid line of data:", id, " is invalid")
                        print(grade)
                        new_grades_df.remove(grade)
            #Check if first character of id is N. If not, print then remove from copied dataframe
            if first_chars != "N":
                 print("Invalid line of data:", id, " is invalid")
                 print(grade)
                 new_grades_df.remove(grade)            
#Calculate number of invalid lines by subtract original dataframe to the copied one.
values_false = len(grades) - len(new_grades_df)
#Calculate number of valid lines by get the len of the copied dataframe.
num_students = len(new_grades_df)
print("Total valid lines of data:", num_students)
print("Total invalid lines of data:", values_false)
print("----------------------")

###
#CALCULATE SCORE
#Input answer keys and split answer key string to list, then turn into dataframe
answer_keys = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
answer_key = answer_keys.split(",")
answer_key_table = pd.DataFrame(answer_key)
#Create variables to store values from for loop
answers_checked = []
score_list = []
for grade in new_grades_df:
        value = grade.split(",")
        id = value[0]
        #Create "answer_table" data frame from the grades dataframe and remove student id from data frame
        answer_table = pd.DataFrame(value)
        answer_table = answer_table.iloc[1: , :]
        answer_table = answer_table.reset_index(drop=True)
        #Remove \n from value
        cVal = answer_table.iloc[24][0]
        cValSplit = cVal.split("\n")
        c = cValSplit[0]
        answer_table = answer_table.replace([cVal],c)
        #Compare student answers with answer keys to a new column called "checkAnswer", return True if correct, return the correct answer if false and "" if blank
        conditions  = [answer_table[0] == answer_key_table[0], answer_table[0] == "" , answer_table[0] != answer_key_table[0]]
        choices     = [ "True", '',answer_key_table[0]]
        answer_table["checkAnswer"] = np.select(conditions, choices, default=np.nan)
        #Calculate the quantity of correct, false and blank answers.
        num_correct = (answer_table['checkAnswer']=='True').sum()
        num_blank = (answer_table['checkAnswer']=='').sum()
        num_incorrect = len(answer_table[answer_table['checkAnswer'].map(lambda x: x !='True' and x !='')])
        #Calculate the score
        score = num_correct*4 + num_incorrect*(-1)
        #Make a new dataframe with 2 columns, id and score, then export the dataframe outside loop
        score_fl = pd.DataFrame({'id': [id], 'score': [score]})
        score_list.append(score_fl)
        answers_checked.append(answer_table) 

#Calculate score related question
score_pd = pd.concat(score_list)
# Get the number of students with high score(>80)
high_score_pd = score_pd[score_pd['score'] > 80]
high_score_count = len(high_score_pd)
print("Total student of high scores:",high_score_count)
# Calculate max,min, mean, range of score, and median
mean = round(score_pd['score'].mean(),2)
max = score_pd['score'].max()
min = score_pd['score'].min()
RoS = max - min
# sort score from low to high into 'score_pd_sorted' dataframe
score_pd_sorted = score_pd.sort_values(by=['score'])
score_pd_sorted = score_pd_sorted.reset_index(drop=True)
med_row = score_pd_sorted.median(numeric_only=True)
med= med_row[0]
print("Mean (average) score:", mean)
print("Highest score:", max)
print("Lowest score:", min)
print("Range of scores:", RoS)
print("Median score:", med)

# Calculate answer related question
answer_pd = pd.concat(answers_checked)
answer_pd.columns = ['studentAnswer', 'checkAnswer']
answer_pd['question'] = answer_pd.index
#Find out the question students most answer incorrectly and how many time the question is incorrect.
answers_incorrect_pd = answer_pd[answer_pd['checkAnswer'] != "True"]
answers_incorrect_pd = answers_incorrect_pd[answers_incorrect_pd['studentAnswer'] != ""]
answer_incorrect_count = answers_incorrect_pd.groupby('question')['question'].count()
question_most_incorrect = answer_incorrect_count.idxmax()
num_answer_incorrect = answer_incorrect_count.max()
ratio_incorrect = round(num_answer_incorrect / num_students,2)
print("Question that most people answer incorrectly:", question_most_incorrect)
print("Question", question_most_incorrect, "is answered incorrectly", num_answer_incorrect, "times","-",ratio_incorrect)
#Find out the question students most leave blank and how many time the question is leave blank.
answers_blank_pd = answer_pd[answer_pd['studentAnswer'] == ""]
answers_blank_count = answers_blank_pd.groupby('question')['question'].count()
question_most_leave_blank = answers_blank_count.idxmax()
num_answer_blank = answers_blank_count.max()
ratio_blank = round(num_answer_blank/ num_students,2)
print("Question that most people skip:", question_most_leave_blank)
print("Question", question_most_leave_blank, "is skipped", num_answer_blank, "times","-",ratio_blank)

###
#EXPORT RESULT TO FILE
#turn id and score from dataframe to string
export_lines = score_pd.to_string(header=False,index=False,index_names=False).split('\n')
# export result out. File name will be 'input name'+'_grades.txt'
with open(name+'_grades.txt', 'w') as f:
    for line in export_lines:
        line = line.split(None,2)
        f.write(','.join(line)+ '\n')



