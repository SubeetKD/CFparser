from bs4 import BeautifulSoup
import requests , sys
import string , os , shutil

# your template 
template = r"""#include <bits/stdc++.h>
#define int long long 
#define IOS ios_base::sync_with_stdio(false)

using namespace std;

int32_t main(){IOS;

	return 0;
}
"""

bash_script=r"""#!/bin/bash

g++ -std=c++14 -o sol sol.cpp 
for ((i=1;i<=$1;i++));
do
	echo $i"th test's differnce:"
	./sol<input$i>you$i
	diff -u output$i you$i
done"""


def question_parser(url):
	alpha=url.rsplit('/')
	alpha = alpha[-1]
	soup = BeautifulSoup(requests.get(url).text,'lxml')
	#creating c++ file
	cur_path = os.path.abspath(os.path.join(os.getcwd(),alpha))
	try:
		os.mkdir(cur_path)
	except OSError:
		pass
	with open(os.path.abspath(os.path.join(cur_path,'sol.cpp')),'w') as f:
		f.write(template)
		f.close()
	bash_file_location = os.path.abspath(os.path.join(cur_path,'run.sh'))
	with open(bash_file_location,'w') as f:
		f.write(bash_script)
		f.close()

	os.system(f'chmod +x {bash_file_location}')
	#creating test cases
	test_cases = soup.find(class_='sample-test')
	for put in ['input','output']:
		cnt = 1
		inputs = test_cases.find_all(class_=put)
		for test_case in inputs:
			file_data = test_case.pre.text
			while file_data[0] in ['\n','']:
				file_data.pop(0)
			#file_data.pop(0) # uncomment if input has leading line 
			print(f'{put+str(cnt)} file : {file_data}')
			with open(os.path.abspath(os.path.join(cur_path,put+str(cnt))),'w') as f:
				f.write(file_data+'\n')
			cnt += 1
	return alpha
	


def contest_parser(id,base_url='https://codeforces.com/contest/'):
	url = base_url+str(id)+'/problems'
	soup = BeautifulSoup(requests.get(url).text,'lxml')
	problems = soup.find_all(class_='problemindexholder')
	#print(problems)
	#sys.exit(0)
	for problem in problems:
		name = problem.find(class_='title').text
		name,shit=name.split('.')
		cur_path = os.path.abspath(os.getcwd())
		# creating folder for each question
		try:
			os.mkdir(os.path.abspath(os.path.join(cur_path,name)))
		except OSError:
			pass
		# creating template for solving problem
		cur_path = os.path.abspath(os.path.join(cur_path,name)) # cur path is the folder of the question 
		with open(os.path.abspath(os.path.join(cur_path,'sol.cpp')),'w') as f :
			f.write(template)
			f.close()
		bash_file_location = os.path.abspath(os.path.join(cur_path,'run.sh'))
		with open(bash_file_location,'w') as f:
			f.write(bash_script)
			f.close()

		os.system(f'chmod +x {bash_file_location}')
		# creating test cases
		for put in ['input','output']:
			cnt = 1 # numbering cases
			test_cases = problem.find_all(class_=put)
			for test_case in test_cases:
				file_data = test_case.pre.text.splitlines()
				while file_data[0] in ['','\n']:
					file_data.pop(0)
				#file_data.pop(0) #uncomment if leading blank line appear 
				with open(os.path.abspath(os.path.join(cur_path,put+str(cnt))),'w') as f:
					for line in file_data :
						f.write(line+'\n')
				cnt += 1



def main():
	contest_id = input('Single Question or Contest?\n')
	if contest_id in ['a','all','ALL']:
		contest_id = int(input('Enter the id of the contest.\n'))
		contest_parser(id=contest_id)
		print('Parsing of Contest Completed.')
	else:
		contest_id = input("Enter the url of question.\n")
		question_name = question_parser(url=contest_id)
		print(f'Parsing of {question_name} is completed.')

if __name__ == '__main__':
	main()
