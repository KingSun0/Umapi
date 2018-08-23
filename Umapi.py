# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 10:32:30 2018

@author: HN00242
"""

import requests
import hmac
import hashlib
from urllib import parse
import pandas as pd

def signature_rule(signature,apiSecurity=None):
	'''签名规则函数,s为签名因子字符串,返回加密后文件'''  
	hmac_sha1 = hmac.new(apiSecurity.encode(),
	                     signature.encode(), hashlib.sha1).hexdigest()#转换为二进制编码，再转换成十六进制再加密   
	Signature = hmac_sha1.upper()#加密后的码值大写
	return '_aop_signature='+Signature

def url_change(string_channel=None):
	'''把channels转化成url码'''
	url_channnels=parse.quote(string_channel)
	return url_channnels


def dict_url_signature(opi_parameter={}):
	'''字典参数返回需要加密的签名字符串，和url相应的字符串'''
	dict_keys_sort=sorted(opi_parameter.keys())#对字典的key排序
	signature_opi_parameter=''#参数签名字符串构成
	url_opi_parameter=''#url参数项构成
	for key in dict_keys_sort:
		if opi_parameter[key] is None:
			pass
		else:
			signature_opi_parameter=signature_opi_parameter+key+str(url_change(opi_parameter[key]))
			url_opi_parameter=url_opi_parameter+key+'='+str(url_change(url_change(opi_parameter[key])))+'&'
	return signature_opi_parameter,url_opi_parameter


class API():#url 对应的固定参数组成
	def __init__(self,dominopi='https://gateway.open.umeng.com/openapi/',apikey='*****',apiSecurity='******',
				path='param2/1/com.umeng.uapp/'):
		self.dominopi=dominopi
		self.apikey=apikey
		self.apiSecurity=apiSecurity
		self.path=path
		'''apikey,apiSecurity为网站提供值'''


	def UmengUappGetNewAccountsRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933','startDate':'2018-08-12',
				'endDate':'2018-08-14','periodType':'daily','channel':None}):
		'''获得新增账户,返回DataFrame数据类型,列明为对应的json字典key名。
		返回一个日期数行3列或4列（如果有channel）的DataFrame数据，返回'date'日期, 'newAccount', 'newUser',（channel）
		名称		类型		是否必须		描述		示例值
		appkey	string_channel是		应用ID	--
		startDate	String	是 	查询起始日期	2018-01-01
		endDate	String	是	查询截止日期	2018-01-01
		periodType	String	否	查询类型（按日daily,按周weekly,按月monthly 查询）	默认daily
		channel	String	否	渠道名称（仅限一个App%20Store）	应用市场-vivo（可以输入汉字）
		'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.getNewAccounts/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		data=pd.DataFrame(message['newAccountInfo'])
		if opi_parameter['channel'] is None:
			pass
		else:
			data['channel']=opi_parameter['channel']
		return data
	def UmengUappGetActiveAccountsRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933','startDate':'2018-08-12',
				'endDate':'2018-08-14','periodType':'daily','channel':None}):
		'''获取活跃账号，返回一个日期数行3列或4列（如果有channel）的DataFrame数据
		返回'date', 'activeAccount', 'activeUser',（channel）

		参数：名称		类型	是否必须		描述		示例值	
			appkey	String	是	应用ID	--	
			startDate	String	是	查询起始日期	2018-01-01
			endDate	String	是	查询截止日期	2018-01-01
			periodType	String	否	查询类型（按日daily,按周weekly,按月monthly 查询）	默认daily
			channel	String	否	渠道名称（仅限一个App%20Store）	应用市场-vivo'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.getActiveAccounts/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		list_values=list(message.values())[0]#把外层字典的值转换为列表
		data=pd.DataFrame(message['activeAccountInfo'])
		if opi_parameter['channel'] is None:
			pass
		else:
			data['channel']=opi_parameter['channel']
		return data

		#未成功
	def UmengUappEventCreateRequest(self,opi_parameter={'appkey':"", 'eventName':"", 'eventDisplayName':"", 'eventType':None}):
		'''创建自定义事件'''

		pass


	def UmengUappGetLaunchesByChannelOrVersionRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933','startDate':'2018-01-01',
				'endDate':'2018-01-02','periodType':'daily','channels':None,'versions':None}):
		'''根据渠道或版本条件，获取App启动次数.注意这里channels比前面的多了个s
		返回日期行两列或者四列的DataFrame数据,'date'日期, 'value',('channels', 'versions')
		名称	类型	是否必须	描述	示例值
		appkey	String	是	应用ID	--
		startDate	String	是	查询起始日期	2018-01-01
		endDate	String	是	查询截止日期	2018-01-01
		periodType	String	是	查询类型（按日daily,按周weekly,按月monthly 查询）	默认daily
		channels	String	否	渠道名称（App%20Store）	应用市场-vivo
		versions	String	否	版本名称（1.0.0）	1.0.0'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.getLaunchesByChannelOrVersion/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		data=pd.DataFrame(message['launchInfo'])
		if opi_parameter['channels'] is None:
			pass
		else:
			data['channels']=opi_parameter['channels']
		if opi_parameter['versions'] is None:
			pass
		else:
			data['versions']=opi_parameter['versions']
		return data


	def UmengUappGetActiveUsersByChannelOrVersionRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933','startDate':'2018-01-01',
				'endDate':'2018-01-02','periodType':'daily','channels':None,'versions':None}):
		'''根据渠道或版本条件，获取App活跃用户数
		返回日期行两列或者四列的DataFrame数据,'date'日期, 'value',('channels', 'versions')
		名称	类型	是否必须	描述	示例值
		appkey	String	是	应用ID	--
		startDate	String	是	查询起始日期	2018-01-01
		endDate	String	是	查询截止日期	2018-01-01
		periodType	String	是	查询类型（按日daily,按周weekly,按月monthly 查询）	默认daily
		channels	String	否	渠道名称（App%20Store）	应用市场-vivo
		versions	String	否	版本名称（1.0.0）	1.0.0'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.getActiveUsersByChannelOrVersion/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		data=pd.DataFrame(message['activeUserInfo'])
		if opi_parameter['channels'] is None:
			pass
		else:
			data['channels']=opi_parameter['channels']
		if opi_parameter['versions'] is None:
			pass
		else:
			data['versions']=opi_parameter['versions']
		return data
		


	def UmengUappGetNewUsersByChannelOrVersionRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933','startDate':'2018-01-01',
				'endDate':'2018-01-02','periodType':'daily','channels':None,'versions':None}):
		'''根据渠道或版本条件，获取App新增用户数
		返回日期行两列或者四列的DataFrame数据,'date'日期, 'value',('channels', 'versions')
		名称	类型	是否必须	描述	示例值
		appkey	String	是	应用ID	--
		startDate	String	是	查询起始日期	2018-01-01
		endDate	String	是	查询截止日期	2018-01-01
		periodType	String	是	查询类型（按日daily,按周weekly,按月monthly 查询）	默认daily
		channels	String	否	渠道名称（App%20Store）	应用市场-vivo
		versions	String	否	版本名称（1.0.0）	1.0.0'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.getNewUsersByChannelOrVersion/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		data=pd.DataFrame(message['newUserInfo'])
		if opi_parameter['channels'] is None:
			pass
		else:
			data['channels']=opi_parameter['channels']
		if opi_parameter['versions'] is None:
			pass
		else:
			data['versions']=opi_parameter['versions']
		return data

		#没数据
	def UmengUappEventParamGetValueDurationListRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933','startDate':'2018-01-01',
				'endDate':'2018-01-02','eventName':None,'eventParamName':None}):
		'''获取事件参数值时长列表'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.event.param.getValueDurationList/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		list_values=list(message.values())[0]#把外层字典的值转换为列表
		data=pd.DataFrame(columns=list_values[0].keys())
		for i in range(len(list_values)):
			data.loc[i]=list(list_values[i].values())
		return data
		

	def UmengUappGetTodayYesterdayDataRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933'}):
		'''获取App今天与昨天的统计数据,返回1行5列的DataFrame数据。
		'activityUsers', 'date'日期, 'launches', 'newUsers', 'totalUsers' 
		名称	类型	是否必须	描述	示例值
		appkey	String	是	应用ID	--'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.getTodayYesterdayData/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		data=pd.DataFrame([message['todayData'],message['yesterdayData']])
		return data 

	def UmengUappGetYesterdayDataRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933'}):
		'''获取App昨天统计数据返回1行5列的DataFrame数据。
		'activityUsers', 'date'日期, 'launches', 'newUsers', 'totalUsers' 
		名称	类型	是否必须	描述	示例值
		appkey	String	是	应用ID	--'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.getYesterdayData/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		data=pd.DataFrame([message['yesterdayData']])
		return data 
		
	def UmengUappGetTodayDataRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933'}):
		'''获取App今天统计数据返回1行5列的DataFrame数据。
		'activityUsers', 'date'日期, 'launches', 'newUsers', 'totalUsers' 
		名称	类型	是否必须	描述	示例值
		appkey	String	是	应用ID	--'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.getTodayData/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		data=pd.DataFrame([message['todayData']])
		return data 
		#没数据
	def UmengUappEventGetUniqueUsersRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933','startDate':'2018-08-12',
				'endDate':'2018-08-14','eventName':None}):
		'''获取自定义事件的独立用户数
			名称		类型		是否必须		描述		示例值		
			appkey		String		是		应用ID		--		
			startDate	String		是		查询起始日期		2018-01-01		
			endDate		String		是		查询截止日期		2018-01-01		
			eventName	String		是		自定义事件名称（通过umeng.uapp.event.list获取）		--'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.event.getUniqueUsers/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		return message
		
	def UmengUappGetAllAppDataRequest(self,opi_parameter={}):
		'''获取所有App统计数据,返回一个1行7列的DataFrame数据
		无参数todayActivityUsers', 'todayLaunches'（今日启动次数）, 'todayNewUsers', 'totalUsers','yesterdayActivityUsers', 
		'yesterdayLaunches', 'yesterdayNewUsers' '''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.getAllAppData/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		data=pd.DataFrame(message['allAppData'])#所给数据已经是列表字典形式
		return data 
		
	def UmengUappGetAppCountRequest(self,opi_parameter={}):

		'''获取App数量,返回1行1列的DataFrame数据。app种类数据？'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.getAppCount/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		data=pd.DataFrame([message])
		return data 

	def UmengUappGetChannelDataRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933', 
			'date':'2018-08-14', 'perPage':60, 'page':1}):
		'''获取渠道维度统计数据,经过测试知道page只能等于1，perPage小于100,返回n（perPage*page）行,7列的DataFrame数据
			名称		类型		是否必须		描述		示例值		
			appkey		String		是		应用ID		--		
			date		String		是		查询日期		2018-01-01		
			perPage		Integer		否		每页显示数量（最大100）		--		
			page		Integer		否		页数		--'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.getChannelData/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		data=pd.DataFrame(message['channelInfos'])
		return data

	def UmengUappGetVersionDataRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933', 'date':'2018-08-14'}):
		'''获取版本维度统计数据。返回当前版本数行6列的DataFrame数据
		返回'activeUser', 'date', 'newUser', 'totalUser', 'totalUserRate','version'
		参数：名称		类型		是否必须		描述		示例值		
			appkey		String		是		应用ID		--		
			date		String		是		查询日期		2018-01-01'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.getVersionData/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		data=pd.DataFrame(message['versionInfos'])
		return data
		#无数据
	def UmengUappEventParamGetDataRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933','startDate':'2018-01-01',
				'endDate':'2018-01-02','eventName':None,'eventParamName':None,'paramValueName':None}):
		'''获取事件参数值统计数据，所有参数不为空

		参数：名称	类型		是否必须		描述		示例值
			appkey	String	是	应用ID	--
			startDate	String	是	查询起始日期	2018-01-01
			endDate	String	是	查询截止日期	2018-01-01
			eventName	String	是	自定义事件名称（通过umeng.uapp.event.list获取）	--
			eventParamName	String	是	自定义事件参数名称（通过umeng.uapp.event.param.list获取）	--
			paramValueName	String	是	自定义参数值名称（通过umeng.uapp.event.param.getValueList获取）	--'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.event.param/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		#data=pd.DataFrame(message['versionInfos'])
		#return data
		#无数据
	def UmengUappEventParamGetValueListRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933','startDate':'2018-01-01',
				'endDate':'2018-01-02','eventName':None,'eventParamName':None}):
		'''获取事件参数值统计列表，所有参数不为空

		参数：名称	类型		是否必须		描述		示例值
			appkey	String	是	应用ID	--
			startDate	String	是	查询起始日期	2018-01-01
			endDate	String	是	查询截止日期	2018-01-01
			eventName	String	是	自定义事件名称（通过umeng.uapp.event.list获取）	--
			eventParamName	String	是	自定义事件参数名称（通过umeng.uapp.event.param.list获取）	--'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.event.param.getValueList/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		#data=pd.DataFrame(message['versionInfos'])
		#return data
		#无数据
	def UmengUappEventGetDataRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933','startDate':'2018-01-01',
				'endDate':'2018-01-02','eventName':None}):
		'''获取事件统计数据，所有参数不为空

		参数：名称	类型		是否必须		描述		示例值
			appkey	String	是	应用ID	--
			startDate	String	是	查询起始日期	2018-01-01
			endDate	String	是	查询截止日期	2018-01-01
			eventName	String	是	自定义事件名称（通过umeng.uapp.event.list获取）	--'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.event.getData/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		#data=pd.DataFrame(message['versionInfos'])
		#return data
		#无数据
	def UmengUappEventParamListRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933','startDate':'2018-01-01',
				'endDate':'2018-01-02','eventId':None}):
		'''获取事件参数列表，所有参数不为空

		参数：名称	类型		是否必须		描述		示例值
			appkey	String	是	应用ID	--
			startDate	String	是	查询起始日期	2018-01-01
			endDate	String	是	查询截止日期	2018-01-01
			eventId	String	是	事件ID（通过umeng.uapp.event.list接口查询得到的ID）	--'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.event.param.list/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		#data=pd.DataFrame(message['versionInfos'])
		#return data

	def UmengUappEventListRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933', 'startDate':'2018-08-12',
			'endDate':'2018-08-14', 'perPage':'60', 'page':'1','version':None}):
		'''获取事件列表(事件的对应信息),经过测试知道page，perPage小于100,返回n（perPage*page）行,4列列的DataFrame数据
		'count', 'displayName', 'id', 'name' 
		参数：名称	类型		是否必须		描述		示例值
			appkey	String	是	应用ID	--
			startDate	String	是	查询起始日期	2018-01-01
			endDate	String	是	查询截止日期	2018-01-01
			perPage	Integer	否	每页显示数量（最大100）	10
			page	Integer	否	页数	1
			version	String	否	应用版本号	--'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.event.list/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		data=pd.DataFrame(message['eventInfo'])
		return data

	def UmengUappGetRetentionsRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933','startDate':'2018-01-01',
				'endDate':'2018-01-02','periodType':'daily','channel':None,'version':None}):
		'''获取App留存用户数 返回日期行11列的DataFrame数据
		行标签为日起 安装用户数 1-7天留存 14天留存 30天留存

		参数：名称	类型	是否必须	描述	示例值
			appkey	String	是	应用ID	--
			startDate	String	是	查询起始日期	2018-01-01
			endDate	String	是	查询截止日期	2018-01-01
			periodType	String	否	查询类型（按日daily,按周weekly,按月monthly 查询）	daily
			channel	String	否	渠道名称（仅限一个App%20Store）	应用市场-vivo
			version	String	否	版本名称（仅限一个1.0.0）	1.0.0
			'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.getRetentions/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		'''把留存解析成一列一列的数据时间不匹配的补None
		dict_list=[]
		retentionRateday=['1dayretentionRate','2dayretentionRate','3dayretentionRate',
							'4dayretentionRate','5dayretentionRate','6dayretentionRate',
							'7dayretentionRate','14dayretentionRate','30dayretentionRate']
		for j in range(len(message['retentionInfo'])):
			dict_day={}
			for i in range(len(retentionRateday)):
				try:
					dict_day[retentionRateday[i]]=message['retentionInfo'][j]['retentionRate'][i]
				except:
					dict_day[retentionRateday[i]]=None
			del message['retentionInfo'][j]['retentionRate']
			dict_list.append(dict(dict_day,**message['retentionInfo'][j]))
		data=pd.DataFrame(dict_list)
		'''
		data=pd.DataFrame(message['retentionInfo'])
		if opi_parameter['channel'] is None:
			pass
		else:
			data['channels']=opi_parameter['channel']
		if opi_parameter['version'] is None:
			pass
		else:
			data['versions']=opi_parameter['version']
		return data

	def UmengUappGetDurationsRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933', 'date':'2018-08-14',
			'statType':'daily','channel':None,'version':None}):
		'''获取App使用时长
		返回8行3列DataFrame数据 列标签 停留时长区间 比率 人数 		行标签为对应区间
		参数：名称	类型	是否必须	描述	示例值
			appkey	String	是	应用ID	--
			date	String	是	查询日期	2018-01-01
			statType	String	否	查询时长统计类型（按天daily，按次daily_per_launch）	daily
			channel	String	否	渠道名称（仅限一个App%20Store）	App%20Store
			version	String	否	版本名称（仅限一个1.0.0）	1.0.0'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.getDurations/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		data=pd.DataFrame([message])
		
		if opi_parameter['channel'] is None:
			pass
		else:
			data['channels']=opi_parameter['channel']
		if opi_parameter['version'] is None:
			pass
		else:
			data['versions']=opi_parameter['version']
		return data
		

	def UmengUappGetLaunchesRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933','startDate':'2018-01-01',
				'endDate':'2018-01-02','periodType':'daily'}):
		'''获取App启动次数 返回日期行 两列数据 列标签；为日期和当天启动数 （测试结果和所给示例不一样 没有按小时的）
		参数：名称	类型	是否必须	描述	示例值
			appkey	String	是	应用ID	--
			startDate	String	是	查询起始日期	2018-01-01
			endDate	String	是	查询截止日期	2018-01-01
			periodType	String	否	查询类型（按日daily,按周weekly,按月monthly 查询）	daily'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.getLaunches/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		data=pd.DataFrame(message['launchInfo'])
		return data
	def UmengUappGetActiveUsersRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933','startDate':'2018-08-12',
				'endDate':'2018-08-14','periodType':'daily'}):
		'''获取App活跃用户数 返回日期行 两列数据 列标签：为日期和APP当天活跃数 （测试结果和所给示例不一样 没有按小时的）
		参数：名称	类型	是否必须	描述	示例值
			appkey	String	是	应用ID	--
			startDate	String	是	查询起始日期	2018-01-01
			endDate	String	是	查询截止日期	2018-01-02
			periodType	String	否	查询类型（按日daily,按周weekly,按月monthly 查询）	daily'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.getActiveUsers/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		data=pd.DataFrame(message['activeUserInfo'])
		return data
	def UmengUappGetNewUsersRequest(self,opi_parameter={'appkey':'52254b8a56240be8db048933','startDate':'2018-01-01',
				'endDate':'2018-01-02','periodType':'daily'}):
		'''获取App新增用户数 返回日期行 两列数据 列标签：为日期和当天app新增用户数 （测试结果和所给示例不一样 没有按小时的）
		参数：名称	类型	是否必须	描述	示例值
			appkey	String	是	应用ID	--
			startDate	String	是	查询起始日期	2018-01-01
			endDate	String	是	查询截止日期	2018-01-02
			periodType	String	否	查询类型（按日daily,按周weekly,按月monthly 查询）	daily'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.getNewUsers/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		data=pd.DataFrame(message['newUserInfo'])
		return data
		#没有测试接口
	def UmengUappGetDailyDataRequest(self,opi_parameter={'channel':None,'versions':None,
				'appkey':'52254b8a56240be8db048933','date':'2018-08-14'}):
		'''获取App统计数据
		参数：名称	类型	是否必须	描述	示例值
			appkey	String	是	应用ID	--
			date	String	是	查询日期	2018-01-01
			version	String	否	版本名称（选填，仅一次一个）	--
			channel	String	否	渠道名称（选填，仅一次一个）	--'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.getDailyData/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		#data=pd.DataFrame(message['retentionInfo'])
		#return data
		#没有接口
	def UmengUappGetAppListRequest(self,opi_parameter={'perPage':60, 'page':1}):
		'''获取App列表
		参数:名称	类型	是否必须	描述	示例值
			page	Integer	否	页号，从1开始	1
			perPage	Integer	否	每页显示数量（最大100）	10'''
		signature_opi_parameter,url_opi_parameter=dict_url_signature(opi_parameter)
		detail_api='umeng.uapp.getAppList/'#详细api地址
		signature=self.path+detail_api+self.apikey+signature_opi_parameter#构建签名字符串
		url=self.dominopi+self.path+detail_api+self.apikey+'?'+url_opi_parameter+signature_rule(signature,self.apiSecurity)#构建url字符串
		message=requests.get(url).json()#请求url返回一个json字典文档文档
		#data=pd.DataFrame(message['retentionInfo'])
		#return data
