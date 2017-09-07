# coding:utf-8


__author__ = 'mwy'
import logging,time
import requests
from random import choice




class Random_ip(object):
       def __init__(self):
           self.ip_set = []
           for i in range(2):
               self.download_ip()
           print ("ip 初始化结束")


       def getIP(self):
           if len(self.ip_set) == 0:
               self.download_ip()
           ip = choice(self.ip_set)
           #if self.judgeIP(ip)==False:
           #    self.ip_set.remove(ip)
           #   return self.getIP()
           return ip


       def judgeIP(self,ip):
           proxies = {
               'http': "http://%s" % ip,
               'https':"http://%s" % ip,
           }
           url = "http://www.jobbole.com/"
           header = {
               'Host':'www.jobbole.com',
               'Upgrade-Insecure-Requests':'1',
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
           }
           try:
               response = requests.get(url, headers=header, timeout=5, proxies=proxies)
               if response.status_code!=200:
                   return False
               else:
                   return True
           except Exception as ex:
               print (ex,"remove:",ip,len(self.ip_set))
               return False




       def download_ip(self):
           #url = "http://www.xdaili.cn/ipagent/greatRecharge/getGreatIp?spiderId=49595241242b4c7f80d36a119d37d245&orderno=YZ20175265966odSeF2&returnType=1&count=10"
           #url = "http://www.xdaili.cn/ipagent/greatRecharge/getGreatIp?spiderId=54c18d96311d4b63ac1204ee111337b9&orderno=YZ20177185705wJ2Hl5&returnType=1&count=20"
           url = "http://dev.kuaidaili.com/api/getproxy/?orderid=990119242598834&num=20&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_an=1&an_ha=1&sep=1"
           this_head = {
                      'Host':'dec.ip3366.net',
                      'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
                      "Upgrade-Insecure-Requests": '1',
                      }
           resutls = requests.get(url)
           time.sleep(5)
           ips = self.load_ip(resutls)
           self.ip_set.extend(ips)


       def load_ip(self, resutls):
           ips = resutls.content.decode("utf-8").split("\n")
           ips = list(filter(lambda x:len(x)>0 , ips))
           ips = [item.strip() for item in ips]
           return ips

       def delete_ip(self,ip):
           if ip in self.ip_set:
              self.ip_set.remove(ip)


if __name__ == '__main__':
    tmp = Random_ip()
    print (tmp.getIP())

