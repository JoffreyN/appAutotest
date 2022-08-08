#配置设备
deviceDic={
	'VBJDU19510007442':{#华为荣耀v10
		'platformName':'Android',
		'platformVersion':'9',
		# 'systemPort':'8200',
	},
	'iPhone 11 Pro Max':{
		"platformName": "iOS",
		# "platformVersion": "13.5",
	},
	'iPhone 11 Pro':{
		"platformName": "iOS",
		# "platformVersion": "13.5",
	},
	'iPhone 11':{
		"platformName": "iOS",
		# "platformVersion": "13.5",
	}
}

##################以下配置一般不用修改#################

receiver=['CMBI-****@****.***.**']
mailToCc=[]#抄送


import sys,os
platform=sys.platform
if platform=='darwin':
	try:
		ip=[a for a in os.popen('ifconfig en2').readlines() if 'inet' in a][1].split()[1]
	except:
		ip=[a for a in os.popen('ifconfig en1').readlines() if 'inet' in a][1].split()[1]
	port='80'
	host=f'http://{ip}:{port}/report'
	genPath=os.path.join(sys.path[0],'report/')
	webPath='~/zp/www/report/'
elif platform=='win32':
	# ip=[a for a in os.popen('route print').readlines() if ' 0.0.0.0 ' in a][0].split()[-2]
	ip='192.168.31.80'
	port='80'
	host=f'http://{ip}:{port}/report'
	genPath=os.path.join(sys.path[0],'report/')
	webPath='/WWW/report'

#regWeb开户保存的开户信息
regFilePath='testData/regFile.txt'

#regWeb开户自动修改的密码
newPwd='******'
