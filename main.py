import requests
from bs4 import BeautifulSoup
import zipfile
import os
import time


headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',}

#def get_proxies():
#    TODO
#proxies = get_proxies()

def sub_req(contestid, subid):
    url = 'https://codeforces.com/contest/' + contestid + '/submission/' + subid
    i = 2
    while True:
        t0 = time.time()
        page = requests.get(url, headers=headers,)
        res_delay = time.time() - t0
        time.sleep(0.5 + res_delay)
        soup = BeautifulSoup(page.content, 'html.parser')
        code = soup.find(id = 'program-source-text')
        if code is None:
            time.sleep(i * res_delay)
            i = i * 2
            print(i)
            if i > 32:
                return -1
        else:
            break
    return code.text

def determineLang(lang):
    if lang.find('C++') >= 0:
        return '.cpp'
    if lang.find('Java') >= 0:
        return '.java'
    if lang.find('Python') >= 0:
        return '.py'
    return '.txt'

def f(username):
    cnt = 0
    url = 'https://codeforces.com/api/user.status?handle=' + username
    filename = username + "'s submissions.zip"
    zip_file = zipfile.ZipFile(filename, 'w', compresslevel=zipfile.ZIP_DEFLATED)
    page = requests.get(url)
    data = page.json()['result']
    data.sort(key=lambda x: (x['timeConsumedMillis']))
    seen = {}
    for problem in data:
        if problem['verdict'] == 'OK':
            if 'problemsetName' in problem['problem']:
                continue
            problem_id = str(problem['problem']['contestId']) + problem['problem']['index']
            if problem_id in seen:
                continue
            seen[problem_id] = True
            lang = determineLang(problem['programmingLanguage'])
            print(str(cnt) + ': ' + problem_id)
            cnt = cnt + 1
            code = sub_req(str(problem['contestId']), str(problem['id']))
            if code == -1:
                continue
            object_name = problem_id + lang
            object_handle = open(object_name, 'w')
            object_handle.write(code)
            object_handle.close()
            zip_file.write(object_name)
            os.remove(object_name)
    zip_file.close()

f('apiv')

