from bs4 import BeautifulSoup
import requests
import sys
import string
import os

# your template
template = r"""#include <bits/stdc++.h>
#define int long long
#define IOS ios_base::sync_with_stdio(false)

using namespace std;

int32_t main(){IOS;

	return 0;
}
"""

# This implementation is ugly
bash_script = r"""#!/bin/sh

read test_case

g++ -std=c++17 -o sol sol.cpp
for ((i=1;i<=$test_case;i++));
do
	echo $i"th test's differnce:"
	./sol<input$i>you$i
        echo "Your Output"
        cat you$1 
        echo "Answer : "
        cat output$1
        echo "============================================="
done"""


def question_parser(url):
    alpha = url.rsplit('/')
    alpha = alpha[-1]
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    # creating c++ file
    cur_path = os.path.abspath(os.path.join(os.getcwd(), alpha))
    try:
        os.mkdir(cur_path)
    except OSError:
        print(f'Unable to make folder, the folder might exist')
        sys.exit(1)
        # pass
    with open(os.path.abspath(os.path.join(cur_path, 'sol.cpp')), 'w') as f:
        f.write(template)
        f.close()
    bash_file_location = os.path.abspath(os.path.join(cur_path, 'run'))
    with open(bash_file_location, 'w') as f:
        f.write(bash_script)
        f.close()

    os.system(f'chmod +x {bash_file_location}')
    # creating test cases
    test_cases = soup.find(class_='sample-test')
    for put in ['input', 'output']:
        cnt = 1
        inputs = test_cases.find_all(class_=put)
        for test_case in inputs:
            file_data = str(test_case.pre)
            # if they use line breakers
            file_data = file_data.replace('<pre>', '')
            file_data = file_data.replace('</pre>', '')
            file_data = file_data.replace('<br/>', '\n')
            file_data = file_data.split('\n')
            while file_data[0] in ['\n', '']:
                file_data.pop(0)
            # file_data.pop(0) # uncomment if input has leading line
            print(f'{put+str(cnt)} file : {file_data}')
            with open(os.path.abspath(os.path.join(cur_path, put+str(cnt))), 'w') as f:
                for line in file_data:
                    f.write(line+'\n')
            cnt += 1
    return alpha


def contest_parser(id, base_url='https://codeforces.com/contest/'):
    url = base_url+str(id)+'/problems'
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    problems = soup.find_all(class_='problemindexholder')
    # print(problems)
    # sys.exit(0)
    for problem in problems:
        name = problem.find(class_='title').text
        name, other_things = name.split('.')
        cur_path = os.path.abspath(os.getcwd())
        # creating folder for each question
        try:
            os.mkdir(os.path.abspath(os.path.join(cur_path, name)))
        except OSError:
            print('Unable to create Folder, the folder might exists already')
            sys.exit(1)

        # creating template for solving problem
        # cur path is the folder of the question
        cur_path = os.path.abspath(os.path.join(cur_path, name))
        with open(os.path.abspath(os.path.join(cur_path, 'sol.cpp')), 'w') as f:
            f.write(template)
            f.close()
        bash_file_location = os.path.abspath(os.path.join(cur_path, 'run'))
        with open(bash_file_location, 'w') as f:
            f.write(bash_script)
            f.close()

        os.system(f'chmod +x {bash_file_location}')
        # creating test cases
        for put in ['input', 'output']:
            cnt = 1  # numbering cases
            test_cases = problem.find_all(class_=put)
            for test_case in test_cases:
                file_data = str(test_case.pre)
                # if they use line breakers
                file_data = file_data.replace('<pre>', '')
                file_data = file_data.replace('</pre>', '')
                file_data = file_data.replace('<br/>', '\n')
                file_data = file_data.split('\n')
                while file_data[0] in ['', '\n']:
                    file_data.pop(0)
                # file_data.pop(0) #uncomment if leading blank line appear
                with open(os.path.abspath(os.path.join(cur_path, put+str(cnt))), 'w') as f:
                    for line in file_data:
                        f.write(line+'\n')
                cnt += 1


def main():
    url = input('Enter the contest id or link to the question\n')
    if url.isdigit():
        contest_parser(id=url)
        print('Parsing of contest is done')
    else:
        # assuming user entered correnct url
        question_name = question_parser(url=url)
        print(f'Parsing of {question_name} is done successfully')


if __name__ == '__main__':
    main()
