# -*- coding: utf-8 -*-
import scrapy, re, datetime, logging,os,codecs
from scrapy.http import Request
from paipaidai.items import PaipaidaiItem

class PaispiderSpider(scrapy.Spider):
    name = "paiSpider"


    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(crawler, settings)

    def read_items(self,filename):
        f = codecs.open(filename, "r+", encoding="utf-8")
        results = f.readlines()
        f.close()
        crawlSet = set()
        for item in results:
            if "item finish" in item or "OneDown" in item :
                id = re.findall("item finish:(\d+)", item)
                if id:
                    crawlSet.add(id[0])
                if 'OneDown' in item:
                    id = re.findall("ITEM fiinish\(OneDown\):(\d+)", item)
                    if id:
                        crawlSet.add(id[0])

            # if  "ERROR: Spider error processing" in item:
            #     id = re.findall("id=(\d+)",item )
            #     if id:
            #         crawlSet.add(id[0])
        return crawlSet

    def __init__(self, crawler, settings):
        self.crawler = crawler
        # 读取 今天log
        log_file = settings['LOG_FILE']
        self.hascrawl = self.read_items(log_file)

        # 读取今天item
        TODAY_ITEM_FILES = settings['TODAY_ITEM_FILES']
        f = codecs.open(TODAY_ITEM_FILES, "r+", encoding="utf-8")
        items = f.readlines()
        f.close()
        self.start_urls = set([item.strip() for item in items])
        self.start_urls = list(self.start_urls - self.hascrawl)
        print("this time will crawl %s" % str(len(self.start_urls)))




    def start_requests(self):
        heasers = {'Host':'invest.ppdai.com','Upgrade-Insecure-Requests':'1'}
        for itemid in self.start_urls:
            if itemid not in self.hascrawl:
                url = "http://invest.ppdai.com/loan/info?id=%s" % itemid
                yield Request(url=url, headers={'Host': 'invest.ppdai.com'}, callback=self.parse_user)

    def parse_user(self, response):
        item =  PaipaidaiItem()
        # 项目id
        id = re.findall("id=(\d+)",response.url)[0]
        item['id'] = id
        # 用户名
        userName = response.xpath(".//a[@class='userface']/@href").extract_first()
        userName =  userName.split("/")[-1]
        item['userName'] = userName



        # 用户评级
        userRate = response.xpath(".//span[contains(@class,'creditRating')]/@class").extract_first().replace('creditRating',"").strip()
        item['userRate'] = userRate
        # 金额 年利率 年限
        amount, year_rate, timeLimit = response.xpath(".//div[@class='newLendDetailMoneyLeft']//dd/text()").extract()
        item['amount'] = amount.replace(",","")
        item['year_rate'] = year_rate
        item['timeLimit'] = timeLimit
        #payMethod = response.xpath(".//div[@class='part mb16 clearfix']/div")
        progressBar = "".join(response.xpath(".//div[@class='part clearfix']/div[@class='item w260']/text()").extract())
        # 进度条
        progressBar = re.findall("\d+%",progressBar)[0]
        item['progressBar'] = progressBar
        bidders = response.xpath(".//div[@class='item w164']/text()").extract_first()
        # 投标人数
        bidders = re.findall("\d+", bidders)[0]
        item['bidders'] = bidders
        # 剩余时间
        rest_time = response.xpath(".//span[@id='leftTime']//text()").extract_first()
        item['end_time'] = rest_time
        #rest_time = re.findall("\d+天", rest_time)[0]
        # # 借款余额
        # borrow_balance = response.xpath(".//span[@id='listRestMoney']/text()").extract_first()
        # if borrow_balance:
        #     borrow_balance = borrow_balance.replace(",","").replace("¥","")
        #item['borrow_balance'] = borrow_balance
        borrow_info = response.xpath(".//div[@class='lender-info']//div[@class='flex']//span/text()").extract()
        # 借款人信息
        male, age, registerTime, degree_education, college, learn_form = borrow_info
        item['male'] = male
        item['age'] = age
        item['registerTime'] = registerTime
        item['degree_education'] = degree_education
        item['college'] = college
        item['learn_form'] = learn_form
        # 认证信息
        authentication_information = "|".join(response.xpath(".//ul[@class='record-info']/li/text()").extract())
        item['authentication_information'] = authentication_information
        html = response.text
        html = html.replace("&#165;","")
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)
        html = re_script.sub('', html)  # 去掉SCRIPT
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        html = re_comment.sub('', html)  # 去掉SCRIPT
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        html = re_style.sub('', html)
        html = re.sub("</?\w+[^>]*>","",html)
        if '成功借款次数' in html:
            succeed_borrow = re.findall("成功借款次数.*?(\d+).*?次",html)[0]
        else:
            succeed_borrow = ""
        item['succeed_borrow'] = succeed_borrow
        if '第一次成功借款时间' in html:
            first_borrow_time = re.findall("第一次成功借款时间.*?(\d+/\d+/\d+).*?$",html,re.M)[0]
        else:
            first_borrow_time = ""
        item['first_borrow_time'] = first_borrow_time
        if '历史记录' in html:
            #borrow_history = re.findall("历史记录： 1次流标，1次撤标，0次失败",html)[0]
            borrow_history = re.findall(u"历史记录： ([\u4e00-\u9fa5|\d+|，]*)", html)[0]
        else:
            borrow_history = ""
        item['borrow_history'] = borrow_history
        if '成功还款次数' in html:
            succeed_repay = re.findall("成功还款次数：.*?(\d+).*?次", html)[0]
        else:
            succeed_repay = ""
        item['succeed_repay'] = succeed_repay
        if  '正常还清次数' in html:
            normal_repay = re.findall("正常还清次数：.*?(\d+).*?次",html)[0]
        else:
            normal_repay = ""
        item['normal_repay'] = normal_repay.strip()
        if '逾期(0-15天)还清次数' in html:
            overtime_less_15 = re.findall("逾期\(0-15天\)还清次数：.*?(\d+).*?次",html)[0]
        else:
            overtime_less_15 = ""
        item['overtime_less_15'] = overtime_less_15
        if '逾期(15天以上)还清次数' in html:
            overtime_more_15 = re.findall("逾期\(15天以上\)还清次数：.*?(\d+).*?次",html)[0]
        else:
            overtime_more_15 = ""
        item['overtime_more_15'] = overtime_more_15
        if '累计借款金额'in html: # 47,570.00
            cumulative_amount_of_borrowing = re.findall("累计借款金额：((?:\d+,?)*(?:\d+)?(?:\.\d+)?)", html)[0].replace(",","")
        else:
            cumulative_amount_of_borrowing = ""
        item['cumulative_amount_of_borrowing'] = cumulative_amount_of_borrowing
        if '待还金额' in html:
            to_be_repay = re.findall("待还金额：((?:\d+,?)*(?:\d+)?(?:\.\d+)?)", html)[0].replace(",","")
        else:
            to_be_repay = ""
        item['to_be_repay'] = to_be_repay
        if '待收金额' in html:
            #to_be_gather = re.findall("待收金额：.*?((?:\d+,?)*(?:\d+)?(?:\.\d+)?)", html)[0].replace(",","")
            to_be_gather = re.findall("待收金额：\s*?((?:\d+,)*\d+\.\d+)", html,re.S)[0].replace(",", "")
        else:
            to_be_gather = ""
        item['to_be_gather'] = to_be_gather
        if '单笔最高借款金额' in html:
            max_borrow_amount = re.findall("单笔最高借款金额：((?:\d+,?)*(?:\d+)?(?:\.\d+)?)", html)[0].replace(",","")
        else:
            max_borrow_amount = ""
        item['max_borrow_amount'] = max_borrow_amount
        if '历史最高负债' in html:
            max_liabilities = re.findall("历史最高负债：((?:\d+,?)*(?:\d+)?(?:\.\d+)?)", html)[0].replace(",","")
        else:
            max_liabilities = ""
        item['max_liabilities'] = max_liabilities
        if '负债曲线图' in html:
            #categories = re.findall("categories:\s*\[([\s\S]*?)\]", html)[0]
            #categories = categories.split(",")
            #categories = list(map(lambda x:x.replace('"',"").strip(),categories))

            data = re.findall("data:\s*\[([\s\S]*?)\]", html)[0]
            data = data.split(",")
            #data = list(map(lambda x:x.strip(),data))
            data = list(filter(lambda x:len(x.strip())>0,data))
            last_fuzhai = data[-1].strip()
            #fuzhai = list(zip(categories,data))
            item['last_fuzhai'] = last_fuzhai
        lendDetailTab_tabContent_table1 = response.xpath(".//table[@class='lendDetailTab_tabContent_table1 normal' and not(@style)]")
        sum_of_to_pay = max_overtime = ""
        for table in lendDetailTab_tabContent_table1:
            name = table.xpath(".//th/text()").extract()
            if '金额' in name:# 说明是未来6个月的待还记录
                table_f_six_info = table.xpath(".//td/text()").extract()
                table_f_six_info = [item.replace("¥","") for item in table_f_six_info]
                half_length = int(len(table_f_six_info)/2)
                #table_f_six_info = list(zip(table_f_six_info[:half_length], table_f_six_info[half_length:]))
                table_f_six_info = table_f_six_info[half_length:]
                table_f_six_info = sum([float(item.replace(",","")) for item in table_f_six_info])
                sum_of_to_pay = table_f_six_info
            if '最大逾期天数' in name: # 说明是过去6个月有回款记录的逾期天数
                table_last_six_info = table.xpath(".//td/text()").extract()
                half_length = int(len(table_last_six_info) / 2)
                #table_last_six_info = list(zip(table_last_six_info[:half_length], table_last_six_info[half_length:]))
                table_last_six_info = table_last_six_info[half_length:]
                max_overtime = max([float(item.replace(",","")) for item in table_last_six_info])
                pass
        item['sum_of_to_pay'] = sum_of_to_pay
        item['max_overtime'] = max_overtime

        # 历史成功借款
        hisBorrowTable = response.xpath(".//table[@class='lendDetailTab_tabContent_table1 normal' and @style]//tr[@class='tab-list']")
        avg_rate = avg_data = avg_amount = 0
        if hisBorrowTable:
           for item_1 in hisBorrowTable:
               itemList = item_1.xpath(".//text()").extract()
               itemList = list(filter(lambda x:len(x.strip())>0,itemList))
               itemList = [item.strip() for item in itemList]
               rate = float(itemList[1][:-1])*0.01
               avg_rate += rate
               # 期限
               data = re.findall("(\d+)个月",itemList[2])
               if data:
                   data = int(data[0])*30
                   avg_data += data
               data = re.findall("(\d+)天", itemList[2])
               if data:
                   data = int(data[0])
                   avg_data += data

               avg_amount += float(itemList[3].replace(",",""))
           avg_rate =  avg_rate / len(hisBorrowTable)
           avg_data = avg_data / len(hisBorrowTable)
           avg_amount = avg_amount / len(hisBorrowTable)
        item['avg_rate'] = avg_rate
        item['avg_data'] = avg_data
        item['avg_amount'] = avg_amount
        item['update_time'] = datetime.datetime.now().strftime("%Y-%m-%d")
        # 状态
        if response.xpath(".//div[@class='newbidstatus_lb']"):# 投标已结束
            state = "0"
        elif response.xpath(".//div[@class='restMoney']"): # 还在进行
            state = "0.5"
        elif response.xpath(".//div[@class='wrapNewLendDetailInfoRight']//img[@alt='借款成功']"):
            state = "1"
        elif "借款成功" in response.text:
            state = '1'
        else:
            print("item state error:%s" % id, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.log("tem state error:%s" % id, logging.INFO)
            state = "-1"
        item['state'] = state
        if state!='-1':
            if state == '1':
               self.log("ITEM fiinish(OneDown):%s" % id, logging.INFO)
            else:
                self.log("item finish:%s" % id, logging.INFO)
            print ("item finish:%s" % id,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            yield item



        #succeed_borrow,first_borrow_time = response.xpath(".//div[@class='flex wid720']/p[@class='ex col-1']/span[@class='num']/text()").extract()
        # #  成功借款次数  第一次成功借款时间
        # succeed_borrow_first_borrow_time = response.xpath(".//div[@class='flex wid720']/p[@class='ex col-1']/span[@class='num']/text()").extract_first()
        # if not succeed_borrow_first_borrow_time:
        #     succeed_borrow = 0;
        #     first_borrow_time = 0
        # elif len(succeed_borrow_first_borrow_time) == 2:
        #     succeed_borrow, first_borrow_time = succeed_borrow_first_borrow_time
        # elif len(succeed_borrow_first_borrow_time) ==1:
        #     succeed_borrow = succeed_borrow_first_borrow_time[0]
        #     first_borrow_time = 'this time'
        #
        #
        #
        # borrow_history, succeed_repay = response.xpath(".//div[@class='inner']/p[@class='flex']/span[@class='num']/text()").extract()
        # amountInfo = response.xpath(".//div[@class='inner']/div[@class='flex']/p[@class='ex col-1']/span[@class='num']/text()").extract()
        # amountInfo = [item.replace(",","").replace("次","").replace("¥","").strip() for item in amountInfo]
        # normal_repay, overtime_less_15,overtime_more_15,to_be_repay,to_be_gather,max_borrow_amount,max_liabilities = amountInfo
        # # 未来6个月的待还记录
        # table_f_six =  response.xpath(".//table[@class='lendDetailTab_tabContent_table1 normal' and not(@style)][1]//td").extract()
        # table_f_six = list(filter(lambda x:x.strip(),table_f_six))

