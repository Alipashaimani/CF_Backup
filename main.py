import requests
from bs4 import BeautifulSoup
import zipfile
import os
import time

def sub_req(contestid, subid):
    t0 = time.time()
    url = 'https://codeforces.com/contest/' + contestid + '/submission/' + subid
    page = requests.get(url)
    res_delay = time.time() - t0
    time.sleep(2 * res_delay)
    soup = BeautifulSoup(page.content, 'html.parser')
    code = soup.find(id = 'program-source-text')
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
    url = 'https://codeforces.com/api/user.status?handle=' + username + '&from=1'
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
            code = sub_req(str(problem['contestId']), str(problem['id']))
            object_name = problem_id + lang
            object_handle = open(object_name, 'w')
            object_handle.write(code)
            object_handle.close()
            zip_file.write(object_name)
            os.remove(object_name)
    zip_file.close()

f('apiv')
