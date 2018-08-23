# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 10:32:30 2018

@author: HN00242
"""

import Umapi
import pandas as pd
import time
import datetime
#请求信息的时间
add_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())#显示本地时间
#请求前一天的的数据，前一天的日期
yesterday=(datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
#读入安卓以及ios的渠道和版本名称

channels_Android=list(pd.read_excel('channels_Android.xlsx')['channels_Android'])
channels_ios=list(pd.read_excel('channels_ios.xlsx')['channels_ios'])

versions_Android=list(pd.read_excel('versions_Android.xlsx')['versions_Android'])
versions_ios=list(pd.read_excel('versions_ios.xlsx')['versions_ios'])

dict_app={'手机惠农-安卓':{'appkey':'52254b8a56240be8db048933','channels':channels_Android,'versions':versions_Android}
		,'手机惠农-ios':{'appkey':'55b9851be0f55a59cb0052fc','channels':channels_ios,'versions':versions_ios}
		}
#得到安卓或ios各渠道各版本新增、活跃以及启动次数
data_umeng_basic=pd.DataFrame()
for key,value in dict_app.items():
	data_app =pd.DataFrame()
	for channel in value['channels']:
		for version in value['versions']:
			data=pd.DataFrame()
			opi_parameter={'appkey':'52254b8a56240be8db048933','startDate':yesterday,
							'endDate':yesterday,'periodType':'daily',
							'channels':channel,'versions':version}#函数参数信息
			try:#尝试请求某渠道某版本的新增、活跃、以及启动次数
				data_ActiveUsers=Umapi.API().UmengUappGetActiveUsersByChannelOrVersionRequest(opi_parameter)
				data['daydate']=data_ActiveUsers['date']
				#数据时间转化后的float时间（新列）
				data['int_date']=list(map(lambda a:str(time.mktime(time.strptime(str(a), "%Y-%m-%d"))),data_ActiveUsers['date']))
				data['channel']=data_ActiveUsers['channels']
				data['version']=data_ActiveUsers['versions']
				data['act_users']=data_ActiveUsers['value']
			except:#如果上面请求出错
				try:#休眠60秒，再次请求
					time.sleep(15)
					data_ActiveUsers=Umapi.API().UmengUappGetActiveUsersByChannelOrVersionRequest(opi_parameter)
					data['daydate']=data_ActiveUsers['date']
					data['int_date']=list(map(lambda a:str(time.mktime(time.strptime(str(a), "%Y-%m-%d"))),data_ActiveUsers['date']))
					data['channel']=data_ActiveUsers['channels']
					data['version']=data_ActiveUsers['versions']
					data['act_users']=data_ActiveUsers['value']
				except:#如果再次请求出错，该次请求结果为Nan
					print('UmengUappGetActiveUsersByChannelOrVersionRequest error',channel,version)
					data['daydate']=None
					data['channel']=None
					data['version']=None
					data['act_users']=None
			try:
				data_NewUsers=Umapi.API().UmengUappGetNewUsersByChannelOrVersionRequest(opi_parameter)
				data['new_users']=data_NewUsers['value']
			except :
				try:
					time.sleep(15)
					data_NewUsers=Umapi.API().UmengUappGetNewUsersByChannelOrVersionRequest(opi_parameter)
					data['new_users']=data_NewUsers['value']
				except:
					print('UmengUappGetNewUsersByChannelOrVersionRequest error',channel,version)
					data['new_users']=None
			try:
				data_launch=Umapi.API().UmengUappGetLaunchesByChannelOrVersionRequest(opi_parameter)
				data['launch']=data_launch['value']
			except:
				try:
					time.sleep(15)
					data_launch=Umapi.API().UmengUappGetLaunchesByChannelOrVersionRequest(opi_parameter)
					data['launch']=data_launch['value']
				except :
					print('UmengUappGetLaunchesByChannelOrVersionRequest error',channel,version)
					data['launch']=None
			data['app_name']=key
			data['add_time']=add_time
			print(channel,version)
			data_app=data_app.append(data)
	data_umeng_basic=data_umeng_basic.append(data_app)
data_umeng_basic=data_umeng_basic[['add_time','daydate','int_date','app_name','channel','version',
					'new_users','act_users','launch']]
print(data_umeng_basic)
