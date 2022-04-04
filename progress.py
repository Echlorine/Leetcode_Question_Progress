from urllib import request
import json, argparse

def get_leetcode(id):
    leetcode_id = "leetcode" if id == None else id # 此处可将 "leetcode" 改为你的力扣id，可以去力扣个人主页 https://leetcode-cn.com/u/****/ 查看，****就是力扣id
    '''
    numAcceptedQuestions 已通过题目
    numFailedQuestions 提交未通过题目
    numUntouchedQuestions 未开始题目
    '''
    textmod = {"query":"\n\
                    query userQuestionProgress($userSlug: String!) {\n\
                        userProfileUserQuestionProgress(userSlug: $userSlug) {\n\
                            numAcceptedQuestions {\n difficulty\n count\n}\n\
                            numFailedQuestions {\n difficulty\n count\n}\n\
                            numUntouchedQuestions {\n difficulty\n count\n}\n\
                        }\n\
                    }\n"
               }
    textmod["variables"] = {"userSlug":leetcode_id}
    textmod = json.dumps(textmod).encode(encoding='utf-8')
    header_dict = {'Accept': '*/*', 'Content-Type': 'application/json'}
    url = 'https://leetcode-cn.com/graphql/'
    # POST请求
    req = request.Request(url=url, data=textmod, headers=header_dict, method='POST')
    #添加User-Agent的Header信息
    req.add_header('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29')
    res = request.urlopen(req)
    res = json.loads(res.read().decode())
    for i in res['data']['userProfileUserQuestionProgress']['numAcceptedQuestions']:
        if i['difficulty'] == 'EASY':
            easy_num = i['count']
        if i['difficulty'] == 'MEDIUM':
            medium_num = i['count']
        if i['difficulty'] == 'HARD':
            hard_num = i['count']

    print("{} 目前刷题状况\n简单题: {:,}\n中等题: {:,}\n困难题: {:,}".format(leetcode_id.title(), easy_num, medium_num,hard_num))
    # print(easy_num + medium_num + hard_num)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", default=None)
    args = parser.parse_args()
    get_leetcode(id=args.id)