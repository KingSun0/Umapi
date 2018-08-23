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

list_day=[]#昨天到前31天的时间列表（日期要大于30 才会有30天的留存率更新出来）
for i in range(1,32):
	day_i=(datetime.datetime.now()+datetime.timedelta(days=-i)).strftime("%Y-%m-%d")
	list_day.append(day_i)
endDate=list_day[0]
startDate=list_day[-1]#八天前时间
#得到前一天安卓新增、活跃以及启动次数
dict_app={'手机惠农-安卓':{'appkey':'52254b8a56240be8db048933'}
		,'手机惠农-ios':{'appkey':'55b9851be0f55a59cb0052fc'}
		}
data_all=pd.DataFrame()
for key,value in dict_app.items():

	data=pd.DataFrame()
	opi_parameter={'appkey':value['appkey'],'startDate':startDate,
			'endDate':endDate,'periodType':'daily'}#函数参数信息
	try:#活跃用户
		data_ActiveUsers=Umapi.API().UmengUappGetActiveUsersRequest(opi_parameter)
		data['daydate']=data_ActiveUsers['date']
		data['act_users']=data_ActiveUsers['value']
		data['app_name']=key
	except :
		try:
			time.sleep(30)
			data_ActiveUsers=Umapi.API().UmengUappGetActiveUsersRequest(opi_parameter)
			data['daydate']=data_ActiveUsers['date']
			data['act_users']=data_ActiveUsers['value']
			data['app_name']=key
		except :
			print(key,'UmengUappGetActiveUsersRequest error',startDate,endDate)
			data['daydate']=None
			data['act_users']=None
			data['app_name']=key
	try:#新用户
		data_NewUsers=Umapi.API().UmengUappGetNewUsersRequest(opi_parameter)
		data['new_users']=data_NewUsers['value']
	except :
		try:
			time.sleep(30)
			data_NewUsers=Umapi.API().UmengUappGetNewUsersRequest(opi_parameter)
			data['new_users']=data_NewUsers['value']
		except:
			print(key,'UmengUappGetNewUsersRequest error',startDate,endDate)
			data['new_users']=None
	try:#启动次数
		data_launch=Umapi.API().UmengUappGetLaunchesRequest(opi_parameter)
		data['launches']=data_launch['value']
	except :
		try:
			time.sleep(30)
			data_launch=Umapi.API().UmengUappGetLaunchesRequest(opi_parameter)
			data['launches']=data_launch['value']
		except :
			print(key,'UmengUappGetLaunchesRequest error')
			data['launches']=None

#得到app用户的停留时间，不区分安卓的渠道和版本，如要区分请增加相应的列
	data_Durations=pd.DataFrame()
	for date in list_day:
		data_Duration=pd.DataFrame()
		try:
			data_Duration_day=Umapi.API().UmengUappGetDurationsRequest(opi_parameter={'appkey':value['appkey'],
						'date':date,'statType':'daily','channel':None,'version':None})
			data_Duration['duration_average']=data_Duration_day['average']
			data_Duration['durationInfos']=data_Duration_day['durationInfos']
			data_Duration['date']=date
		except:
			try:
				time.sleep(30)
				data_Duration_day=Umapi.API().UmengUappGetDurationsRequest(opi_parameter={'appkey':value['appkey'],
						'date':date,'statType':'daily','channel':None,'version':None})
				data_Duration['duration_average']=data_Duration_day['average']
				data_Duration['durationInfos']=data_Duration_day['durationInfos']
				data_Duration['date']=date
			except: 
				print(key,'UmengUappGetDurationsRequest  error',date)
				data_Duration=pd.DataFrame([{'duration_average':None,'durationInfos':None,'date':date}])
		data_Durations=data_Durations.append(data_Duration)
	data=pd.merge(data,data_Durations,how='inner',left_on='daydate',right_on='date')
	del data['date']
#每次启动的停留时间
	time.sleep(30)#强制停止一分钟
	data_launch_Durations=pd.DataFrame()
	for date in list_day:
		data_launch_Duration=pd.DataFrame()
		try:
			data_launch_Duration_day=Umapi.API().UmengUappGetDurationsRequest(opi_parameter={'appkey':value['appkey'],
						'date':date,'statType':'daily_per_launch','channel':None,'version':None})
			data_launch_Duration['durationInfos_per_launch']=data_launch_Duration_day['durationInfos']
			data_launch_Duration['duration_per_launch_average']=data_launch_Duration_day['average']
			data_launch_Duration['date']=date
		except:
			try:
				time.sleep(30)
				data_launch_Duration=Umapi.API().UmengUappGetDurationsRequest(opi_parameter={'appkey':value['appkey'],
						'date':date,'statType':'daily_per_launch','channel':None,'version':None})
				data_launch_Duration['durationInfos_per_launch']=data_launch_Duration_day['durationInfos']
				data_launch_Duration['duration_per_launch_average']=data_launch_Duration_day['average']
				data_launch_Duration['date']=date
			except: 
				print(key,'launch_Durations UmengUappGetDurationsRequest  error',date)
				data_launch_Duration=pd.DataFrame([{'durationInfos_per_launch':None,'durationInfos_per_launch':None,'date':date}])
		data_launch_Durations=data_launch_Durations.append(data_launch_Duration)
	data=pd.merge(data,data_launch_Durations,how='inner',left_on='daydate',right_on='date')
	del data['date']

#app用户的留存率s 31天的日期昨天的没有留存数据，昨天新增人数留存为空故用 leftjoin
	try:
		data_Retentions=Umapi.API().UmengUappGetRetentionsRequest(opi_parameter={'appkey':value['appkey'],'startDate':startDate,
					'endDate':endDate,'periodType':'daily','channels':None,'versions':None})
		data_Retentions=data_Retentions.rename(columns={'totalInstallUser':'retention_install'})
		data=pd.merge(data,data_Retentions,how='left',left_on='daydate',right_on='date')
		del data['date']
	except :
		try:
			time.sleep(30)
			data_Retentions=Umapi.API().UmengUappGetRetentionsRequest(opi_parameter={'appkey':value['appkey'],'startDate':startDate,
					'endDate':endDate,'periodType':'daily','channels':None,'versions':None})
			data_Retentions=data_Retentions.rename(columns={'totalInstallUser':'retention_install'})
			data=pd.merge(data,data_Retentions,how='left',left_on='daydate',right_on='date')
			del data['date']
		except:
			print('UmengUappGetRetentionsRequest error',startDate,endDate)
			data['retentionRate']=None
			data['retention_install']=None
	
	data_all=data_all.append(data)
data_all['addtime']=add_time
data_all['date_seg']='daily'
data_umeng_basic_acc=data_all[['addtime','daydate','app_name','date_seg','new_users',
		'act_users','launches','duration_average','durationInfos','duration_per_launch_average',
		'durationInfos_per_launch','retentionRate','retentionRatee']]
