from bs4 import BeautifulSoup
import requests
import string , os

template = r"""#include <bits/stdc++.h>
#define int long long 
#define IOS ios_base::sync_with_stdio(false)

using namespace std;

int32_t main(){
		
	return 0;
}"""

def create_question_list():
	upper_case_letters = string.ascii_uppercase
	ans = []
	for letter in upper_case_letters:
		for num in ['','1','2']:
			ans.append(letter+str(num))
	return ans

def question_parser(url,alpha):
	current_path = os.getcwd()
	new_path = current_path+f'/{alpha}'
	try:
		os.mkdir(new_path)
	except OSError:
		print(f'Creation of question director {alpha} has failed.')
	else:
		print(f'Creating files for question {alpha}.')
	with open(new_path+'/sol.cpp','w') as f:
		f.write(template)
		f.close()
	soup = BeautifulSoup(requests.get(url).text,'lxml')
	for classs in ['input','output']:
		test_cases = soup.find_all('div',class_=classs)
		cnt = 1 # for numbering different input and output files 
		for test_case in test_cases:
			with open(new_path+'/'+classs+str(cnt),'w') as f:
				f.write(test_case.pre.text)
				f.close()
			with open(new_path+'/'+classs+str(cnt),'w+') as f:
				lines = f.readlines()
				bani = False
				for line in lines:
					if bani:
						f.write(line)
					else:
						bani = True
			cnt += 1
	return alpha


def site_exists(url,alpha):
	n = len(alpha)
	soup = BeautifulSoup(requests.get(url).text,'lxml')
	title = soup.find('div',class_='title').text
	return title[:n] == alpha

def contest_parser(id,base_url='https://codeforces.com/contest/'):
	url = base_url+str(id)
	capital_letters = create_question_list() # list of capital letters with 1 2 3 part
	for alpha in capital_letters:
		source = url+'/problem/'+alpha
		if site_exists(source,alpha=alpha):
			question_parser(url=source,alpha=alpha)
			print(f'Parsing of {alpha} is done.')
		else:
			continue
	print('Contest is parsed.')


def main():
	contest_id = input('Single Question or Contest?')
	if contest_id in ['a','all','ALL']:
		contest_id = int(input('Enter the id of the contest.'))
		contest_parser(id=contest_id)
		print('Parsing of Contest Completed')
	else:
		contest_id = input("Enter the url of question.")
		alpha = contest_id[-1]
		question_name = question_parser(url=contest_id,alpha=alpha)
		print(f'Parsing of {question_name} is completed.')

if __name__ == '__main__':
	main()