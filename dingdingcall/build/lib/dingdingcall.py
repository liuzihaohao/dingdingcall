import requests
import time
import hmac
import hashlib
import base64
import urllib.parse

def hasscall(secret):
	timestamp = str(round(time.time() * 1000))
	secret_enc = secret.encode('utf-8')
	string_to_sign = '{}\n{}'.format(timestamp, secret)
	string_to_sign_enc = string_to_sign.encode('utf-8')
	hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
	sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
	return {"timestamp":timestamp,"sign":sign}

def text(secret,url,content):
	#url,content
	headers = {'content-type': 'application/json'}
	data={"msgtype": "text","text": {"content":content}}
	a=hasscall(secret)
	r = requests.post(url+"&timestamp="+a['timestamp']+"&sign="+a["sign"], json=data,headers=headers)
	return {'status':r.status_code,'returntext':r.text}

def link(secret,url,content,linkurl,title,picurl=""):
	#url,content,linkurl,picurl,title
	headers = {'content-type': 'application/json'}
	data={"msgtype": "link","link": {"text": content, "title": title,"picUrl": picurl,"messageUrl": linkurl}}
	a=hasscall(secret)
	r = requests.post(url+"&timestamp="+a['timestamp']+"&sign="+a["sign"], json=data,headers=headers)
	return {'status':r.status_code,'returntext':r.text}

def markdown(secret,url,content,title):
	#url,content,title
	'''
	标题
	# 一级标题
	## 二级标题
	### 三级标题
	#### 四级标题
	##### 五级标题
	###### 六级标题

	引用
	> A man who stands for nothing will fall for anything.

	文字加粗、斜体
	**bold**
	*italic*

	链接
	[this is a link](http://name.com)

	图片
	![](http://name.com/pic.jpg)

	无序列表
	- item1
	- item2

	有序列表
	1. item1
	2. item2
	'''
	headers = {'content-type': 'application/json'}
	data={"msgtype": "markdown","markdown": {"title":title,"text": content},}
	a=hasscall(secret)
	r = requests.post(url+"&timestamp="+a['timestamp']+"&sign="+a["sign"], json=data,headers=headers)
	return {'status':r.status_code,'returntext':r.text}

if __name__ == '__main__':
	url="https://oapi.dingtalk.com/robot/send?access_token=d28f0478f550da5467f53b34bc2396f3a6f60a5c96597d086080d069b177f257"
	secret="SECf89dae444773953b996bbce8511d4f05b60caf3ad2141715bbb33a409c196dc0"
	print(text(secret,url,"[ff"))
	print(link(secret,url,"[fff","127.0.0.1:8000","777"))
	print(markdown(secret,url,"[this is a link](http://name.com)","[]f"))