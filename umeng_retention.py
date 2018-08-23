import Umapi
import pandas as pd
import time
import datetime
#请求信息的时间
add_time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())#显示本地时间

endDate=(datetime.datetime.now()+datetime.timedelta(days=-2)).strftime("%Y-%m-%d")
startDate=(datetime.datetime.now()+datetime.timedelta(days=-31)).strftime("%Y-%m-%d")
list_day=[]#昨天到前31天的时间列表（日期要大于30 才会有30天的留存率更新出来）
for i in range(2,32):
	day_i=(datetime.datetime.now()+datetime.timedelta(days=-i)).strftime("%Y-%m-%d")
	list_day.append(day_i)
#读入安卓以及ios的渠道和版本名称

channels_Android=list(pd.read_excel('channels_Android.xlsx')['channels_Android'])
channels_ios=list(pd.read_excel('channels_ios.xlsx')['channels_ios'])

versions_Android=list(pd.read_excel('versions_Android.xlsx')['versions_Android'])
versions_ios=list(pd.read_excel('versions_ios.xlsx')['versions_ios'])

dict_app={'手机惠农-安卓':{'appkey':'52254b8a56240be8db048933','channels':channels_Android,'versions':versions_Android}
		,'手机惠农-ios':{'appkey':'55b9851be0f55a59cb0052fc','channels':channels_ios,'versions':versions_ios}
		}
data_app_day=pd.DataFrame()
for key,value in dict_app.items():
	for channel in value['channels']:
		for version in value['versions']:
			opi_parameter1={'appkey':value['appkey'],'startDate':startDate,
						'endDate':endDate,'periodType':'daily',
						'channels':channel,'versions':version}#函数参数信息
			#各版本渠道的新增用户
			try:
				data_NewUsers=Umapi.API().UmengUappGetNewUsersByChannelOrVersionRequest(opi_parameter1)
			except:
				try:

					time.sleep(15)
					data_NewUsers=Umapi.API().UmengUappGetNewUsersByChannelOrVersionRequest(opi_parameter1)
				except:
					print(startDate,'-',endDate,key,channel,version,'新增获取失败')
					data_NewUsers=pd.DataFrame(data=list_day,columns=['date'])
					data_NewUsers['value']=1
					data_NewUsers['channels']=channel
					data_NewUsers['versions']=version
			opi_parameter2={'appkey':value['appkey'],'startDate':startDate,
						'endDate':endDate,'periodType':'daily',
						'channel':channel,'version':version}#函数参数信息
			try:
				data_Retentions=Umapi.API().UmengUappGetRetentionsRequest(opi_parameter2)
				print(key,'Retentions',channel,version)
			except :
				try:
					time.sleep(15)
					data_Retentions=Umapi.API().UmengUappGetRetentionsRequest(opi_parameter2)
					print(key,'Retentions',channel,version)

				except :
					print(key,'UmengUappGetRetentionsRequest 留存  error',channel,version)
					data_Retentions=pd.DataFrame(data=list_day,columns=['date'])
					data_Retentions['retentionRate']=None
					data_Retentions['channels']=channel
					data_Retentions['versions']=version
					data_Retentions['totalInstallUser']=1
			data=pd.merge(data_NewUsers[data_NewUsers['value']>0],data_Retentions[data_Retentions['totalInstallUser']>0]
						,how='inner',on=['date','channels','versions'])
			data['app_name']=key
			data['add_time']=add_time
			data=data.rename(columns={'date':'daydate','channels':'channel','versions':'version',
				'value':'new_users','retentionRate':'retention_per_list'})
			data['int_date']=list(map(lambda a:str(time.mktime(time.strptime(str(a), "%Y-%m-%d"))),data['daydate']))
			data_app_day=data_app_day.append(data)
data_umeng_retention=data_app_day[['add_time','daydate','int_date','app_name','channel','version',
					'new_users','retention_per_list']]
#print(data_umeng_retention)