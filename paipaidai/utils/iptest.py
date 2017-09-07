import requests
session = requests.session()
ip = '111.74.56.247:9000'
proxies = {
           'https': ip,
           'http': ip,

        }
headers = {
'Host':'invest.ppdai.com',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
}

# headers = {
# 'Host':'www.baidu.com',
# 'Upgrade-Insecure-Requests':'1',
# 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
# }
# url = "http://www.baidu.com"

url = "http://invest.ppdai.com/loan/listnew?LoanCategoryId=8"
#url = "http://www.ppdai.com/"
response = session.get(url, headers=headers, proxies=proxies)
print (response.status_code)
print  (response.text)