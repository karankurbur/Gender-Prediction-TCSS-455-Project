# Matt P., Josh L., Karan K.
# Jan 17 2018
# Output File Syntax Tester

import os, sys, shutil, optparse
import xml.etree.ElementTree as ET
from os import listdir
from os.path import isfile, join

parser = optparse.OptionParser()

parser.add_option("-o", "--output", action="store", dest="output", help="output dir")

options, args = parser.parse_args()

print "Running output syntax check..."

path = options.output
files = [f for f in listdir(path) if isfile(join(path, f))]

fileCount = 0
errCount = 0

male_count = 0
female_count = 0

# Required sytnax for XML root
requiredRoot = "user"

# Required syntax for attributes
requiredAttributes = ["id", "age_group", "gender", "extrovert", "neurotic", "agreeable", "conscientious", "open"]

for filename in files:
	fileCount += 1

	tree = ET.parse(path + filename)
	root = tree.getroot()
	if (root.tag != requiredRoot):
		print "Mistake in " + filename
		print "Tag is incorrect."
		errCount += 1
	for attr in root.attrib:
		if attr not in requiredAttributes:
			print "Mistake in " + filename
			print "Problem with " + attr
			errCount += 1
	if root.attrib['gender'] == 'male':
		male_count += 1
	if root.attrib['gender'] == 'female':
		female_count += 1
print "Done checking number of files = " + str(fileCount)

if (errCount > 0):
	print errCount + " output syntax errors were found."
else:
	print "Congrats! No output syntax errors were found."
print ('Males :' + str(male_count))
print ('Females :' + str(female_count))
