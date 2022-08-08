import logging,time,os

from common.tools import swipeDown
from common.apiCenter import downloadApp,checkNew

def checkVerEnv(driver,capability,args):
	cusVer=args.cusVer;env=args.env
	from page.navBar import PageBar
	from page.mine.my import PageMy
	from page.mine.set import PageSet
	from page.alert import PageAlert
	pageAlert=PageAlert(driver)
	pageBar=PageBar(driver)
	pageMy=PageMy(driver)
	pageSet=PageSet(driver)
	
	time.sleep(1)
	pageBar.clickMy()
	pageAlert.clickAlert()
	pageMy.clickSet()

	currentEnv=pageSet.textEnv()
	env=env.upper()
	if env==currentEnv:
		logging.info(f'当前运行环境已是 {env}，无需切换')
		reopen=0
	else:
		pageSet.clickSwiSer()
		pageSet.chooseSer(env)
		pageSet.clickConfirm()
		pageSet.clickRebootYes()
		logging.info(f'服务器已切换为 {env}')
		reopen=1

	PFN=driver.capabilities['platformName']
	appVersion=pageSet.textVersion()
	logging.info(f'当APP前版本 {appVersion}')
	if PFN=='Android':
		# logging.info('获取最新app版本号……')
		newerVer=checkNew()
		logging.info(f'最新APP版本 {newerVer}')
		if cusVer:
			logging.info(f'指定需要测试的APP版本 {cusVer}')
			if cusVer!=appVersion:
				cusAppInfo=checkNew(cusVer)
				_appPath=os.path.abspath(f"testData/apk/{cusAppInfo['fullname']}")
				if os.path.exists(_appPath):
					logging.info('检测到目录中已存在该版本，无需下载')
				else:
					downloadApp(cusAppInfo)
				driver.close_app()
				logging.info(f'卸载旧版app……')
				driver.remove_app(capability['appPackage'])
				logging.info(f'安装新版app……')
				driver.install_app(_appPath)
				driver.launch_app()
				return cusAppInfo["version"],reopen
			else:
				logging.info('当前版本已是指定的版本')
				driver.back()
				return appVersion,reopen
		else:
			driver.back()
			return appVersion,reopen
	elif PFN=='iOS':
		driver.back()
		return appVersion,reopen