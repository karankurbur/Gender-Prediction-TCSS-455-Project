import random
import numpy as np
import pandas as pd
import os, sys, shutil, optparse


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

import string
import pickle
from sklearn.externals import joblib

from os import listdir
from os.path import isfile, join, exists

# Handle input arguments: they get saved in options
parser = optparse.OptionParser()

parser.add_option("-i", "--input", action="store", dest="input", help="input dir")
parser.add_option("-o", "--output", action="store", dest="output", help="output dir")

options, args = parser.parse_args()

profile_dir = os.path.join('/data', 'training', 'profile/')
text_dir    = os.path.join('/data', 'training', 'text/')
tsv_file    = 'User-Text-to-Gender.tsv'
#print(profile_dir)
# Create a TSV file with all the users
# Remove it if it already exists.
if (os.path.exists(tsv_file)):
	os.remove(tsv_file)
with open(tsv_file, 'w') as tsv:
	tsv.write('Id' + '\t' + 'status' + '\t' + 'gender' + '\n')
	with open(os.path.join(profile_dir, 'profile.csv')) as datafile:
		# Skip the first line with the labels
		next(datafile)
		# Gets the user id from CSV
		id = ""
		# Gets the text status update from CSV
		text = ""
		# Gets the gender from CSV
		gender = 0.0
		for line in datafile:
			data = line.split(",")
			id = data[1]
			with open(os.path.join(text_dir, id + '.txt'), 'r') as text_file:
				text = text_file.read().replace('\n', '')
			gender = float(data[3])
			tsv.write(id + '\t' + text + '\t' + str(gender) + '\n')

profile_dir2 = options.input + 'profile/'
text_dir2    = options.input + 'text/'
tsv_file2    = 'User-Text-to-Gender2.tsv'

# Create a TSV file with all the users
# Remove it if it already exists.
if (os.path.exists(tsv_file2)):
	os.remove(tsv_file2)
with open(tsv_file2, 'w') as tsv:
	tsv.write('Id' + '\t' + 'status' + '\t' + 'gender' + '\n')
	with open(os.path.join(profile_dir2, 'profile.csv')) as datafile:
		# Skip the first line with the labels
		next(datafile)
		# Gets the user id from CSV
		id = ""
		# Gets the text status update from CSV
		text = ""
		# Gets the gender from CSV
		gender = 0.0
		for line in datafile:
			data = line.split(",")
			id = data[1]
			with open(os.path.join(text_dir2, id + '.txt'), 'r') as text_file:
				text = text_file.read().replace('\n', '')
			gender = 0
			tsv.write(id + '\t' + text + '\t' + str(gender) + '\n')


# Reading the data into a dataframe and selecting the columns we need
with open(tsv_file, 'r') as tsv:
	df = pd.read_table(tsv, encoding = "ISO-8859-1")

with open(tsv_file2, 'r') as tsv:
	df2 = pd.read_table(tsv, encoding = "ISO-8859-1")


#print (df.shape)
#print(df.columns)
#print (df2.shape)
#print(df2.columns)
#print(df2.head())
# Correlating status and gender
data_statuses = df.loc[:,['status', 'gender']]
test_data = df2.loc[:,['status', 'gender']]


# Splitting the data into 300 training instances and 104 test instances
n = 1500

all_Ids = np.arange(len(data_statuses))

# 104 instances for training
# Rest for testing
# Maybe want this in case list is sorted?
random.shuffle(all_Ids)
test_Ids = all_Ids[0:n]
train_Ids = all_Ids[n:]
data_test = data_statuses.loc[test_Ids, :]
data_train = data_statuses.loc[train_Ids, :]

# Training a Naive Bayes model
# Two lines are for transforming into feature table
# In this case, it's on transcripts -> wordcounts
count_vect = CountVectorizer()

# Look in CountVectorizer() docs for returning to word format
# X inputs x1x2x3...
X_train = count_vect.fit_transform(data_train['status'])
# In output:
# In row 0, col 3384, there is a 1.
# Y output
y_train = data_train['gender']

# The type of model you want (naive_bayes)
clf = MultinomialNB()

# Classified becomes naive_bayes model using X_train as x1x2x3...
# and using data_train['gender'] as Y output.
clf.fit(X_train, data_train['gender'])

# Pickle the model and export it
pickled_model = 'finalized_model.sav'
pickle.dump(clf, open(pickled_model, 'wb'))

# Testing the Naive Bayes model
#X_test = count_vect.transform(data_test['status'])
X_test2 =  count_vect.transform(test_data['status'])
#print(X_test2)

y_test = data_test['gender']

#print(X_test2)

# Import model
loaded_model = joblib.load(pickled_model)
y_predicted = loaded_model.predict(X_test2)
#print(y_predicted)



def getPredictedValue(userID):
    getIndex = df2.loc[df2['Id'] == userID].index.values[0]
    #print(getIndex)
    if(y_predicted.item(getIndex) == 0):
        return "male"
    else:
        return "female"

 
#print(getPredictedValue('0ae27ad8fce85b8354228642403f22ce'))    

# This is the library for writing to XML
import xml.etree.ElementTree as ET

print("\n\n\nRunning script...\n\n\n")

print ("Input dir: " + options.input)
print ("Output dir: " + options.output)

# Cumulative gender count helper
def storeGender(gender, genders):
	genders[gender] += 1

# Cumulative age count helper
def storeAge(age, ages):
	if (age < 25):
		ages[0] += 1
	elif (age < 35):
		ages[1] += 1
	elif (age < 50):
		ages[2] += 1
	else:
		ages[3] += 1

# Cumulative personality sum helper
def storePersonality(personality, personalities):
	for i in range (0, 5):
		personalities[i] += float(personality[i])

# Reads from existing user profiles (training data)
# Creates XML for predictions

# Ages stored in bracketed counts
genders = [0, 0]
ages = [0, 0, 0, 0]
personalities = [0, 0, 0, 0, 0]

ageGroups = ["xx-24", "25-34", "35-49", "50-xx"]

count = 0

# Accumulate data and store in a decent format
with open(options.input + "profile/profile.csv") as datafile:

	# Skip the first line with the labels
	next(datafile)

	for line in datafile:
		data = line.split(",")

		id = data[1]
		age = 0
		gender = 0
		#personality = data[4:9]

		storeGender(int(gender), genders)
		storeAge(age, ages)
		#storePersonality(personality, personalities)

		count += 1

# Find the most popular data
# (1) Gender is generalized to one gender, the most popular
# (2) Age is generalized to one age group, the most popular
# (3) The five personality traits are averaged
popularGender = ""
popularAge = ""
popularPersonality = [2.5, 2.5, 2.5, 2.5, 2.5]

if (genders[0] > genders[1]):
	popularGender = "male"
else:
	popularGender = "female"

maxAgeCount = 0
for i in range(0, 4):
	if (ages[i] > maxAgeCount):
		maxAgeCount = ages[i]
		popularAge = ageGroups[i]


# Print out for debugging purposes
print ("\n\n\n*******************************************")
print ("Gender Counts: ")
print (genders)
print ("Popular Gender: ")
print (popularGender)
print ("Age Counts: ")
print (ages)
print ("Popular Age: ")
print (popularAge)
print ("Total Personality Sum: ")
print (personalities)
print ("Total Persons Count: ")
print (count)
print ("Popular Personality: ")
print (popularPersonality)
print ("*******************************************\n\n\n")

# Delete output directory if it exists, then remake it
if os.path.exists(options.output):
	shutil.rmtree(options.output)
os.makedirs(options.output)

# Use accumulated data to write to XML
print ("\n\n\nWriting results to XML files...\n\n\n")

with open(options.input + "profile/profile.csv") as datafile:

	# Skip the header line
	next(datafile)

	for line in datafile:
		data = line.split(",")

		id = data[1]

		user = ET.Element("user")
		user.set("id", id)
		user.set("age_group", popularAge)
		user.set("gender", getPredictedValue(id))
		user.set("extrovert", str(popularPersonality[0]))
		user.set("neurotic", str(popularPersonality[1]))
		user.set("agreeable", str(popularPersonality[2]))
		user.set("conscientious", str(popularPersonality[3]))
		user.set("open", str(popularPersonality[4]))
		userData = ET.tostring(user)
		userFile = open(options.output + id + ".xml", "w")
		userFile.write(userData)
    
print ("Finished.")








