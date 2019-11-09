import glob
import os

files = glob.glob("filesToZip/")

def extract_file_name(string):
	return string[::-1].partition("/")[0][::-1]

os.system("cp *.py filesToZip/")
os.system("cd filesToZip; zip -r ../Archive.zip .")