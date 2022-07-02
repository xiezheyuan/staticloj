import requests
import json

import tqdm

from database import *


# noinspection PyBroadException
def spider_submission(id):
    url = "https://api.loj.ac.cn/api/submission/getSubmissionDetail"
    payload = json.dumps(
        {"submissionId": str(id), "locale": "zh_CN"})
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload, timeout=3000)
    except BaseException:
        return ["", "", ""]
    body = response.json()
    return [body["content"]["code"], body["content"]["language"], body["meta"]["submitter"]["username"]]


# noinspection PyBroadException
def spider_fastest_code(pid):
    url = "https://api.loj.ac.cn/api/submission/querySubmissionStatistics"
    payload = json.dumps(
        {"problemDisplayId": pid, "statisticsType": "Fastest", "locale": "zh_CN", "skipCount": 0, "takeCount": 10})
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, timeout=3000)
    except BaseException:
        return ["None", "None", "None", "[]"]
    body = response.json()
    fastest = ["None", "None", "None", "[]"]
    try:
        information = spider_submission(body["submissions"][0]["id"])
        fastest = information
        fastest.append(json.dumps(body["scores"]))
    except BaseException:
        pass
    return fastest


# noinspection PyBroadException
def spider(pid):
    url = "https://api.loj.ac.cn/api/problem/getProblem"

    payload = json.dumps({
        "displayId": pid,
        "localizedContentsOfLocale": "zh_CN",
        "tagsOfLocale": "zh_CN",
        "samples": True,
        "judgeInfo": True,
        "judgeInfoToBePreprocessed": True,
        "statistics": True,
        "discussionCount": True,
        "permissionOfCurrentUser": True,
        "lastSubmissionAndLastAcceptedSubmission": True
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, timeout=3000)
    except BaseException:
        return
    if response.status_code not in [200, 201]:
        return
    body = response.json()
    main = ""
    tags = []

    try:
        for content in body["localizedContentsOfLocale"]["contentSections"]:
            if content["type"] == "Sample":
                sample = body["samples"][content["sampleId"]]
                main += ("\n## 样例%d \n\n### 输入 \n\n```\n%s\n```\n\n### 输出\n\n```\n%s\n```\n" % (content["sampleId"],
                                                                                                sample["inputData"],
                                                                                                sample["outputData"]))
            else:
                main += ("\n## %s \n\n%s\n" % (content["sectionTitle"], content["text"]))

        for tag in body["tagsOfLocale"]:
            name = tag["name"]
            tags.append(name)
        try:
            time_limit = body["judgeInfo"]["timeLimit"]
        except KeyError:
            time_limit = 0
        try:
            memory_limit = body["judgeInfo"]["memoryLimit"]
        except KeyError:
            memory_limit = 0

        code = spider_fastest_code(pid)
        LOJProblem.insert(id=pid,
                          name=body["localizedContentsOfLocale"]["title"],
                          accepted_count=body["meta"]["acceptedSubmissionCount"],
                          submit_count=body["meta"]["submissionCount"],
                          problem_type=body["meta"]["type"],
                          time_limit=time_limit,
                          memory_limit=memory_limit,
                          body=main,
                          tags=','.join(tags),
                          fastest_code=code[0],
                          fastest_language=code[1],
                          fastest_submitter=code[2],
                          score=code[3]
                          ).execute()
    except BaseException:
        pass


for i in tqdm.tqdm(range(2164, 6819)):
    spider(i)
