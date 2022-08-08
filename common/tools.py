import time,datetime,logging,os,sys,traceback,base64,requests,json,hmac,hashlib,operator,random,urllib3
from business.others import reOpenApp
from HTMLReport import addImage

########################################### FTP 相关 Start #######################################################
import posixpath
from ftplib import error_perm, FTP

def ftp_delete_file(ftpObj,pathTofile):
	try:
		ftpObj.delete(pathTofile)
	except error_perm as e:
		if 'No such file or directory' not in str(e):
			raise e

def ftp_makedirs_cwd(ftpObj, path, first_call=True):
	try:
		ftpObj.cwd(path)
	except error_perm:
		ftp_makedirs_cwd(ftpObj,posixpath.dirname(path),False)
		ftpObj.mkd(path)
		if first_call:ftpObj.cwd(path)

def ftp_store_file(localFile,remotePath,host='0.0.0.0',port=21,username='****',password='****',use_active_mode=False):
	logging.info(f'上传文件 {localFile} 至 {remotePath}')
	with open(localFile,'rb') as fileObj:
		with FTP() as ftp:
			ftp.connect(host,port)
			ftp.login(username,password)
			if use_active_mode:ftp.set_pasv(False)
			ftp_delete_file(ftp,remotePath)# 删除已有的
			dirname,filename = posixpath.split(remotePath)
			ftp_makedirs_cwd(ftp,dirname)
			ftp.storbinary('STOR %s' % filename,fileObj)
	logging.info(f'上传成功')

########################################### FTP 相关 End #######################################################

def pressKeyboard(driver,s):
    keyCodeDict={'0':7,'1':8,'2':9,'3':10,'4':11,'5':12,'6':13,'7':14,'8':15,'9':16,'A':29,'B':30,'C':31,'D':32,'E':33,'F':34,'G':35,'H':36,'I':37,'J':38,'K':39,'L':40,'M':41,'N':42,'O':43,'P':44,'Q':45,'R':46,'S':47,'T':48,'U':49,'V':50,'W':51,'X':52,'Y':53,'Z':54,'.':56}
    for i in str(s):
        driver.keyevent(keyCodeDict[i])
        time.sleep(1)

def getHKid():
	hk_id=int(random.random()*26+1)
	sums=hk_id*8
	hk_id=chr(hk_id+64)
	for i in range(1,7):
		s=round(random.random()*9)
		sums=sums+s*(8-i)
		hk_id=f'{hk_id}{s}'
	return f'{hk_id}{11-(sums%11)}'


def encryption(jsonData,keyType='APP'):
	keyDict={'APP':'****','H5':'****'}
	timestamp=str(int(1000*time.time()))
	jsonData=dict(sorted(jsonData.items(),key=operator.itemgetter(0),reverse=False))# 排序
	msg=json.dumps(jsonData).replace(" ","")+timestamp
	signature=hmac.new(keyDict[keyType].encode('utf-8'),msg.encode('utf-8'),hashlib.md5).hexdigest()
	return timestamp,signature

def getSoup(driver):
	from bs4 import BeautifulSoup
	html=driver.page_source
	soup=BeautifulSoup(html,'lxml')
	return soup

def encode_md5(string):
	# for TTL resetpwd
	import hashlib
	md5=hashlib.md5()
	md5.update(string.encode(encoding='utf-8'))
	return md5.hexdigest()

def replaceVideolog(timeStr):
	htmlPath=f'report/{timeStr}/index.html'
	allLines=open(htmlPath,'r',encoding='utf-8').readlines()
	flag=0
	for i,line in enumerate(allLines):
		if '录屏保存成功' in line:
			flag=1
			videoName=line.split('/')[-1]
			allLines[i]=f'<video controls width="400" type="video/mp4" preload="auto"><source src="videos/{videoName}" autostart="false"></video><br>'
	if flag:
		with open(htmlPath,'w',encoding='utf-8') as htmlFile:
			htmlFile.writelines(allLines)

def start_recording(driver):
	logging.info('开始录屏')
	driver.start_recording_screen(videoType='h264',videoSize='720x1280',timeLimit=600)
	# driver.start_recording_screen(videoType='mpeg4',videoSize='1440x1920')

def stop_recording(driver,report_timestr,videoName=None):
	# print(os.getcwd()) /Users/mac/zp/myCode/appAutoTest
	logging.info('结束录屏')
	mp4_base64=driver.stop_recording_screen()
	mp4_decode=base64.b64decode(mp4_base64)
	savePath=f'report/{report_timestr}/videos'
	if not os.path.exists(savePath):os.makedirs(savePath)
	if not videoName:videoName=time.strftime('%H%M%S')
	with open(f"{savePath}/{videoName}.mp4","wb") as fd:fd.write(mp4_decode)
	logging.info(f'录屏保存成功: videos/{videoName}.mp4')

def scrollByXpath(driver,xpath):
	xpath=xpath.replace("'",'"')
	js1="function getElementByXpath(path) {return document.evaluate(path,document,null,XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;};"
	js2=f"getElementByXpath('{xpath}').scrollIntoView();"
	driver.execute_script(js1+js2)

def keyboardInput(driver,amount=0,boardType=1,n=0):
	if not amount:
		from random import uniform
		amount=round(uniform(1000,10000),2)
	time.sleep(1)
	logging.info(f'输入金额 {amount}')
	keyboardDic={'1':0,'2':1,'3':2,'4':3,'5':4,'6':5,'7':6,'8':7,'9':8,'.':9,'0':10} if boardType==1 else {'1':0,'2':1,'3':2,'4':3,'5':4,'6':5,'7':6,'8':7,'9':8,'0':9}
	for i in str(amount):
		js=f'document.getElementsByClassName("keyboard-number-list")[{n}].getElementsByClassName("keyboard-number-item")[{keyboardDic[i]}].click();'
		time.sleep(0.5)
		driver.execute_script(js)
	time.sleep(0.5)
	logging.info('点击键盘 确定 ')
	driver.execute_script(f'document.getElementsByClassName("keyboard-operate-list")[{n}].querySelector(".confirm").click();')

def switch_execute(func):
	def wrapped(*args):
		# context=args[0].driver.current_context
		try:current_url=args[0].driver.current_url
		except:current_url=0
		if args[0].driver.capabilities['platformName']=='iOS':time.sleep(5)#ios端经常会卡死，可能是切换太快
		args[0].driver.switch_to.context(args[0].driver.contexts[0])
		logging.info(f'已切换为原生context')
		func(*args)
		# args[0].driver.switch_to.context(context)
		try:swithToRightWeb(args[0].driver,current_url,reopen=0)
		except:swithToRightWeb(args[0].driver,0)
		try:current_url=args[0].driver.current_url
		except:current_url=None
		logging.info(f'已切换回webview: {current_url}')
	return wrapped

@switch_execute
def myAddScreen(self,msg=''):
	# 当处于webview页面时使用此方法
	addImage(self.driver.get_screenshot_as_base64(),msg)

def swithToRightWeb(driver,urlFlag,exclude='',reopen=1):
	from .seleniumError import SCEWDE
	urlFlag=str(urlFlag)
	if driver.capabilities['platformName']=='iOS':time.sleep(3)#ios端经常会卡死，可能是切换太快
	if urlFlag=='0':
		try:
			driver.switch_to.context(driver.contexts[0])
		except urllib3.exceptions.MaxRetryError:
			reOpenApp(driver)
			raise Exception(f'切换webview失败')
		logging.info(f'已切换为原生context')
	else:
		for i in range(10):
			contexts=driver.contexts
			for context in contexts[1:]:
				try:
					driver.switch_to.context(context)
					window_handles=driver.window_handles
				except:
					continue
				for handle in window_handles:
					if not handle:continue
					try:
						driver.switch_to.window(handle)
					except SCEWDE:
						continue
					try:
						current_url=driver.current_url
					except:
						current_url='er'
					if urlFlag.lower() in current_url.lower():
						if exclude and exclude.lower() in current_url.lower():continue
						logging.info(f'切换webview成功，当前URL: {current_url}')
						return
			logging.info(f'切换webview失败，1秒后重试')
			time.sleep(1)
		driver.switch_to.context(contexts[0])
		addImage(driver.get_screenshot_as_base64(),f'切换webview失败 {urlFlag}')
		if reopen:
			reOpenApp(driver)
			raise Exception(f'切换webview失败')

def coordinate(xy0,size1,size0=(1440,2960)):
	x1=int(xy0[0]/size0[0]*size1[0])
	y1=int(xy0[1]/size0[1]*size1[1])
	return x1,y1

def maxVersion(v1,v2):
	v1List=v1.split('.')
	v2List=v2.split('.')
	maxLen=max(len(v1List),len(v2List))
	for i in range(maxLen):
		str1=v1List[i];str2=v2List[i]
		if i==maxLen-1:
			while 1:
				if len(str1)<len(str2):str1=f'{str1}0'
				elif len(str1)>len(str2):str2=f'{str2}0'
				elif len(str1)==len(str2):break
		int1=int(str1);int2=int(str2)
		if int1>int2:return v1
		elif int1<int2:return v2
		else:
			if i==maxLen-1:return v1

def isTradeTime(timeNow=None,market='HK'):
	#传入时间戳
	from chinese_calendar import is_workday
	if not timeNow:timeNow=time.time()
	date,weekDay=time.strftime('%Y%m%d %w').split()
	yestodate_date=datetime.datetime.now()+datetime.timedelta(days = -1)
	yestodate=yestodate_date.strftime('%Y%m%d')
	resp=is_workday(datetime.date(int(date[:4]),int(date[4:6]),int(date[6:])))# 节假日返回 False
	if (not resp) or (weekDay in ['0','6']):#周六日休市
		return 0
	else:
		if market=='HK':
			start1=start2=time.mktime(time.strptime(f'{date} 09:20:00','%Y%m%d %X'))
			# stop1=time.mktime(time.strptime(f'{date} 12:00:00','%Y%m%d %X'))
			# start2=time.mktime(time.strptime(f'{date} 13:00:00','%Y%m%d %X'))
			stop1=stop2=time.mktime(time.strptime(f'{date} 16:00:00','%Y%m%d %X'))
		elif market=='A':
			start1=time.mktime(time.strptime(f'{date} 09:30:00','%Y%m%d %X'))
			stop1=time.mktime(time.strptime(f'{date} 11:30:00','%Y%m%d %X'))
			start2=time.mktime(time.strptime(f'{date} 13:00:00','%Y%m%d %X'))
			stop2=time.mktime(time.strptime(f'{date} 15:00:00','%Y%m%d %X'))
		elif market=='US':
			start1=time.mktime(time.strptime(f'{date} 22:30:00','%Y%m%d %X'))
			stop1=start1+6.5*60*60
			start2=time.mktime(time.strptime(f'{yestodate} 22:30:00','%Y%m%d %X'))
			stop2=start2+6.5*60*60
		timeNow_strf=time.strftime('%Y-%m-%d %X',time.localtime(timeNow))
		# print(start1,stop1)
		if start1<timeNow<stop1 or start2<timeNow<stop2:
			print(f'当前时间 {timeNow_strf} 为 {market} 交易时间')
			return 1
		else:
			print(f'当前时间 {timeNow_strf} 为 {market} 菲交易时间')
			return 0

def getCapability(args):
	# skipServerInstallation 跳过uiAutomator2服务器的安装，当设备上已经安装了正确版本的uiAutomator2时，可用于提高启动性能。
	# newCommandTimeout 在**秒内未收到任何脚本发过来的命令后会自动关闭，session关闭后会自动点home键，将设备返回主界面

	from config import deviceDic
	if 'iPhone' not in args.deviceName:
		andVer=executeCmd(f'adb -s {args.deviceName} shell getprop ro.build.version.release')
		deviceDic[args.deviceName]={
			'platformName':'Android',
			'platformVersion':andVer,
		}
	app_id='com.cmbi.zytx'
	if deviceDic[args.deviceName]['platformName'].lower()=='android':
		commCapa={
			'udid':args.deviceName,
			'appPackage':app_id,
			"appActivity": '.module.AppStartEmptyActivity',
			'autoGrantPermissions':True,
			'unicodeKeyboard': True,
			'resetKeyboard': True,
			'automationName':'uiautomator2',
			'recreateChromeDriverSessions':True,
			# 'skipServerInstallation':True,
		}
	elif deviceDic[args.deviceName]['platformName'].lower()=='ios':
		commCapa={
			"platformVersion":args.platformVersion,
			"autoAcceptAlerts": True,# 自动接收弹窗（不支持基于XCUITest的测试）
			"automationName": "XCUITest",
		}
		if args.iosAppPath:
			commCapa['app']=args.iosAppPath.strip()
		else:
			commCapa['bundleId']=app_id
		if args.WDAP:commCapa['webDriverAgentUrl']=f"http://localhost:{args.WDAP}"
	commCapa['app_id']=app_id
	commCapa['deviceName']=args.deviceName
	commCapa['noReset']=True
	commCapa['newCommandTimeout']=7200
	capability=dict(deviceDic[args.deviceName],**commCapa)
	return capability

def moveFiles(reportName,ops='move'):
	from config import platform,genPath,webPath
	if platform=='darwin':
		cmd=f'mv {os.path.join(genPath,reportName)} {webPath}'
	elif platform=='win32':
		cmd=f'echo d | xcopy /r /y /e "{os.path.join(genPath,reportName)}" "{os.path.join(webPath,reportName)}"'
	os.system(cmd)

def baiduOCR(picBase64):
	import requests,json
	url='http://ai.baidu.com/aidemo'
	__head={
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
		'Cookie':'BAIDUID=8AFE279DACE07546FCABA930EFF0B042:FG=1; PSTM=1569201597; BIDUPSID=47F8C9B28FCE37C21E4FD26EAA669FB8; H_WISE_SIDS=135882_125703_114552_136650_135584_134727_136243_114745_134983_120131_136601_136365_132910_136455_136618_131246_136682_136721_132378_131518_118883_118872_118849_118829_118793_107320_132782_136800_136429_136092_133351_129653_136193_132250_128967_135308_133847_132552_135874_136604_131423_133857_135861_134601_136019_136301_110085_131115_134153_127969_136298_131755_131951_135623_136611_135458_128201_136076_135036_136636_134844_135718_132468_136413_136705; BDUSS=xXeTREZVBubEItfkJTTWowaGNsUHFKZkxYT2l3dFgxYzZEc1lKM1ZEelpPZDlkRVFBQUFBJCQAAAAAAAAAAAEAAADvozcwxt-30rC8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANmst13ZrLdddW; BDSFRCVID=48tOJeCmH6VsaxbwxuKnwgae-mKK0gOTHllkTDd-8ZVEgHLVJeC6EG0Ptf8g0KubFTPRogKK0gOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tRk8oDKhJCvbfP0k-tT85tP8qxby26nAQg6eaJ5n0-nnhncajP5bWCueKHolQ43LBbn0hU7FKKnDMP0Ry6CKjTo3DGLfJTneaKcJsJ78anT_eJbv5PI_h4L3eUjfJURZ5m7LaIQCbb7CO43j25A55P-_becLBMPj52OnanRsbJRMjPP4BnrU3Ro3346-35543bRTLnLy5KJvfJoD3h3ChP-UyN3MWh37Je3lMKoaMp78jR093JO4y4Ldj4oxJpOJ5JbMopCafD_bhD-4Djt2entebl8X2-6Q2Co-0n75ajr_et-rj57MXUI8LUc7tq5eK6baL-naWbrbenjNqtcvyT8sXnO72P7WQgnbsCnuQq5JOhRKy4oTjxL1Db3JKjvMtg3t3qQmLUooepvoD-Jc3MvByPjdJJQOBKQB0KnGbUQkeq8CQft20b0EeMtjW6LEK5r2SCKhtCL-3e; delPer=0; PSINO=6; H_PS_PSSID=1464_21078_29568_29221; BDAIUID=5dca39f9e18c21593681865; BDAUIDD=5dca39f9e190c7824739540; Hm_lvt_8b973192450250dd85b9011320b455ba=1573534203; seccode=1a79a1c32e688a53e106c58e8882a7e2; Hm_lpvt_8b973192450250dd85b9011320b455ba=1573534217; __yjsv5_shitong=1.0_7_c6fd46d055928f6baf2960ddb1306ccfc9b4_300_1573534217363_210.21.237.101_7104490c',
		'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
		'Connection':'close',
	}
	keys={
		'image':picBase64,
		'image_url':'',
		'type':'commontext',
		'detect_direction':'false',
	}
	resp=requests.post(url,headers=__head,data=keys)
	try:
		repJson=resp.json()
	except json.decoder.JSONDecodeError:
		raise Exception(resp.text)
	if repJson['errno']:
		raise Exception(f'调用百度识图接口失败: {repJson}')
	else:
		return repJson['data']['words_result'][0]['words']

def saveFile(strs,out=1):
	from config import regFilePath
	if out:print(strs)
	try:
		with open(regFilePath,'a',encoding='utf-8') as f:
			f.write(f'{strs}\n')
	except FileNotFoundError:
		pass

def ifskip(kword):
	skipList=open('skip','r',encoding='utf-8').read()
	if kword in skipList:return 1
	else:return 0

def getDriver(desired_caps,appiumUrl='http://127.0.0.1:4723/wd/hub'):
	import traceback
	from appium import webdriver
	from .seleniumError import SCENSEE
	driver=webdriver.Remote(appiumUrl,desired_caps)
	time.sleep(0.5)
	if desired_caps['platformName'].lower()=='android':
		time.sleep(10)
		driver.tap([(1285,2850)])
	elif desired_caps['platformName'].lower()=='ios':
		time.sleep(5)
	time.sleep(5)
	return driver

def getWebDriver(setwindow=1,headless=0):
	from selenium import webdriver

	chrome_option=webdriver.ChromeOptions()
	chrome_option.add_experimental_option('useAutomationExtension',False)#禁止显示“请停用以开发者……”
	chrome_option.add_experimental_option("excludeSwitches",['enable-automation'])#禁止显示“Chrome正受到自动化软件的控制”
	# chrome_option.add_experimental_option('w3c',False)
	if headless:chrome_option.add_argument('--headless')

	driver=webdriver.Chrome(options=chrome_option)
	if setwindow:driver.set_window_size(400,1000)
	return driver

def swipeAbs(driver,x1,y1,x2,y2,n=1):
	from selenium.webdriver.common.touch_actions import TouchActions
	# from appium.webdriver.common.touch_action import TouchAction
	actions = TouchActions(driver)
	for i in range(n):
		actions.long_press(x=x1, y=y1)
		actions.move_to(x=x2, y=y2)
		actions.release()
		actions.perform()

def swipeUp(driver,t=200,n=1,xy=0):# 向上滑动屏幕 t 滑动耗时(毫秒);n 滑动次数;xy 滑动起始坐标
	size=driver.get_window_size()
	if xy:
		x1,y1=xy
	else:
		x1=size['width']*0.5# x坐标
		y1=size['height']*0.75# 起始y坐标
	y2=size['height']*0.25# 终点y坐标
	for i in range(n):
		driver.swipe(x1,y1,x1,y2,t)

def swipeDown(driver,t=200,n=1,xy=0):
	size=driver.get_window_size()	
	if xy:
		x1,y1=xy
	else:
		x1=size['width']*0.5
		y1=size['height']*0.25
	y2=size['height']*0.75
	for i in range(n):
		driver.swipe(x1,y1,x1,y2,t)

def swipLeft(driver,t=200,n=1,xy=0):
	size=driver.get_window_size()
	if xy:
		x1,y1=xy
	else:
		x1=size['width']*0.75
		y1=size['height']*0.5
	x2=size['width']*0.25
	for i in range(n):
		driver.swipe(x1,y1,x2,y1,t)

def swipRight(driver,t=200,n=1,xy=0):
	size=driver.get_window_size()	
	if xy:
		x1,y1=xy
	else:
		x1=size['width']*0.25
		y1=size['height']*0.5
	x2=size['width']*0.75
	for i in range(n):
		driver.swipe(x1,y1,x2,y1,t)

def sendMail(text,platformName,fromInfo=None,cusReceiver=None):
	import smtplib
	from email.header import Header
	from email.mime.text import MIMEText
	from email.utils import formataddr
	if cusReceiver:
		receiver,mailToCc=cusReceiver.split(),[]
	else:
		from config import receiver,mailToCc
	sender='****-****@****.***.**'
	# password='****'
	subject=f'【{platformName}】壹隆环球APP自动化测试报告'

	msg=MIMEText(text,'html','utf-8')
	msg['Subject']=Header(subject,'utf-8') #设置主题和格式
	if not fromInfo:fromInfo="appAutoTest UI自动化测试"
	msg['From']=formataddr([fromInfo,sender])
	msg['To']=';'.join(receiver)
	msg['Cc']=';'.join(mailToCc)
	
	smtp=smtplib.SMTP('m***.c***.***.hk',25)
	# smtp=smtplib.SMTP_SSL('smtp.qq.com',465)
	# smtp.ehlo()
	# smtp.starttls()
	# smtp.login(username, password)
	smtp.sendmail(sender, receiver+mailToCc, msg.as_string())
	smtp.quit()
	logging.info('邮件发送成功!')

def getCellStr(cell,noStrip=0):
	if cell.value==None:return cell.value
	try:
		strs=str(cell.value) if noStrip else str(cell.value).strip().replace('\n','<br>')
	except AttributeError:
		strs=str(cell.value)
	return strs

def removeFile(filePath):
	try:
		os.remove(filePath)
	except FileNotFoundError:
		pass

def executeCmd(cmd):
	import subprocess
	try:
		result=subprocess.getoutput(cmd)
		return result
	except Exception as err:
		print(f'执行cmd命令失败：{cmd}\n原因：{err}')
		sys.exit()

def out(strings):
	sys.stdout.write(f'{strings}\r')
	sys.stdout.flush()

def saveCookie(cookie,file):
	sys.path.append('..')
	fpath='testData/cookie'
	if not os.path.exists(fpath):os.mkdir(fpath)
	with open(f'{fpath}/{file}','w',encoding='utf-8') as f:
		f.write(cookie)

def readCookie(file):
	sys.path.append('..')
	try:
		return open(f'testData/cookie/{file}').read().strip()
	except:
		logging.info(f'读取cookie文件失败: {file}')
		return '0'

