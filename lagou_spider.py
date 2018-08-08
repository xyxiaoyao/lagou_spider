# coding:utf-8


import requests
import jsonpath
import json
import time
import random

class LagouSpider(object):
    def __init__(self):
        self.base_url = "https://www.lagou.com/jobs/positionAjax.json?"
        self.headers = {
            "Accept" : "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding" : "gzip, deflate, br",
            "Accept-Language" : "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection" : "keep-alive",
            "Content-Length" : "26",
            "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie" : "user_trace_token=20170923184359-1ba5fe6f-a04c-11e7-a60e-525400f775ce; LGUID=20170923184359-1ba6010d-a04c-11e7-a60e-525400f775ce; index_location_city=%E5%8C%97%E4%BA%AC; JSESSIONID=ABAAABAACEBACDGF071FAE6BE1F68696EF4356C16381303; X_HTTP_COOK_CODE=85782; TG-TRACK-CODE=index_search; SEARCH_ID=3f9e61601dc745c39f89855c4ba48fff; _gid=GA1.2.1239271841.1510196816; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1509193471,1509936663,1510196816,1510216967; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1510219012; _ga=GA1.2.136733168.1506163440; LGSID=20171109164247-f6241c4c-c529-11e7-986b-5254005c3644; LGRID=20171109171652-b8fc422e-c52e-11e7-986b-5254005c3644",
            "Host" : "www.lagou.com",
            "Origin" : "https://www.lagou.com",

            # 1 . 反爬点1：检查Referer值，必须是一个合理值
            "Referer" : "https://www.lagou.com/jobs/list_python?px=default&xl=%E6%9C%AC%E7%A7%91&city=%E5%8C%97%E4%BA%AC&district=%E6%B5%B7%E6%B7%80%E5%8C%BA",

            # 2. 反爬点2：User-Agent
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36",
            "X-Anit-Forge-Code" : "0",
            "X-Anit-Forge-Token" : "None",
            "X-Requested-With" : "XMLHttpRequest"
        }

        # 4. 添加代理池，每次请求可以更换代理，还可以配合User-Agent池、Cookie池
        self.proxy_list = [
            {"http" : "mr_mao_hacker:sffqry9r@120.26.167.140:16816"},
            {"http" : "mr_mao_hacker:sffqry9r@43.226.164.66:16816"},
        ]

        self.position = raw_input("请输入需要抓取的职位名:")
        self.city = raw_input("请输入需要抓取的城市名:")
        self.page = int(raw_input("请输入需要抓取的页数:"))
        self.pn = 1
        self.count = 0

        self.item_list = []


    def load_page(self):
        params = {
            "px" : "default",
            "city" : self.city,
            "needAddtionalResult" : "false",
            "isSchoolJob" : "0"
        }

        data = {
            "first" : "false",
            "pn" : self.pn,
            "kd" : self.position
        }

        proxy = random.choice(self.proxy_list)

        try:
            print "[INFO]: 正在抓取第%d页.." % self.pn
            print proxy
            json_obj = requests.post(self.base_url, params = params, data = data, headers = self.headers, proxies = proxy).json()

        except:
            print "[ERROR] : 请求发送失败.."


        try:
            #jsonpath 返回的列表，result本身就是列表，[[]]
            result_list = jsonpath.jsonpath(json_obj, "$..result")[0]

            for result in result_list:
                item = {}
                item["companyFullName"] = result["companyFullName"]
                item["salary"] = result["salary"]
                item["positionName"] = result["positionName"]
                item["createTime"] = result["createTime"]
                self.item_list.append(item)
        except:
            print json_obj
            print "[ERROR]: 数据提取失败..."

            #print result
        #json_obj = json.loads(json_str)

    def write_page(self):

        json.dump(self.item_list, open("lagou.json", "w"))

        #json_str = json.dumps(self.item_list)
        #with open("lagou.json", "w") as f:
        #    f.write(json_str)

    def start_work(self):
        #for page in range(1, self.page + 1)
        while self.pn <= self.page:
            self.load_page()

            # 3. 控制请求发送的频率，尽量保证请求的安全。
            time.sleep(2)

            self.count += 1
            if self.count == 5:
                time.sleep(3)
                self.count = 0

            self.pn += 1

        self.write_page()



if __name__ == "__main__":
    spider = LagouSpider()
    spider.start_work()
