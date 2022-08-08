import logging,time
from HTMLReport import addImage
from page.navBar import PageBar
from page.mine.my import PageMy
from page.alert import PageAlert

def login(driver,acc_pwd,forceLogout=0,cusNickName=None,args=None,acc=1,needNickname=1):
	# forceLogout 0表示登录前先检测是否已登陆，是则直接返回；1表示如果已登录，则先退出，再登录
	#cusNickName 若指定了要登录账户的昵称 则判断获取的与指定的是否一致；不指定则只判断是否已登录 不限账户
	# acc=0 只登陆手机号的情况
	# from common.getCode_BP import getCodeLog
	from common.system_boss import getSMScode
	# from common.seleniumError import SCENSEE
	from page.mine.login_uname import PageLogin_u
	from page.mine.login_pword import PageLogin_p
	from page.mine.logined import PageLogined
	from page.mine.lingpai import PageLingpai
	from page.trade.trade import PageTrade
	from testData.data import accBinding

	pageBar=PageBar(driver)
	pageMy=PageMy(driver)
	pageTrade=PageTrade(driver)
	pageAlert=PageAlert(driver)

	for i in range(5):
		pageBar.clickMy(timeout=5,screen=False)
		pageAlert.clickAlert()
		try:
			nickName=pageMy.textNick(logit=0,timeout=5)
		except AttributeError:
			nickName=0
		if nickName:# 有昵称，说明已登录
			if cusNickName:
				if cusNickName in nickName:
					if forceLogout:
						logging.info('检测到已登录指定昵称的账号，强制先登出……')
						logout(driver)
					else:
						logging.info('检测到已登录指定昵称的账号，无需登录……')
						#点击交易，检查登录态是否失效
						pageBar.clickTrade()
						pageAlert.clickAlert()
						if pageTrade.loginFlagExists():
							pageTrade.inputPwd(acc_pwd[1])
							pageTrade.clickloginFlag()
							time.sleep(1)
						return
				else:
					logging.info('检测到已登录其它账号，需先登出……')
					logout(driver)
			else:
				if forceLogout:
					logging.info('检测到是已登录状态，需先登出……')
					logout(driver)
				else:
					logging.info('检测到是已登录状态，无需登录……')
					#点击交易，检查登录态是否失效
					pageBar.clickTrade()
					pageAlert.clickAlert()
					if pageTrade.loginFlagExists():
						pageTrade.inputPwd(acc_pwd[1])
						pageTrade.clickloginFlag()
						time.sleep(1)
					return

		logging.info(f'开始登录,账号 {acc_pwd}')
		
		pageLogin_u=PageLogin_u(driver)
		pageLogin_p=PageLogin_p(driver)
		pageLogined=PageLogined(driver)
		pageLingpai=PageLingpai(driver)

		try:
			pageMy.clickLogin()
			break
		except AttributeError:
			if i==4:
				addImage(driver.get_screenshot_as_base64(),'登录失败，无法找到登录按钮')
				reOpenApp(driver)
				raise Exception('登录失败，无法找到登录按钮')
			pageBar.goBack()

	if args.env=='prod':
		pageLogin_u.inputUname(acc_pwd[0])
		pageLogin_u.clickLogin()
		if pageLogin_u.unCheckFlagExists():
			pageLogin_u.clickConfirm()
			pageLogin_u.clickCheckView(args.appVersion,env=args.env,only=1)
			pageLogin_u.clickLogin()
	else:
		pageLogin_u.clickCheckView(args.appVersion,env=args.env)
		pageLogin_u.inputUname(acc_pwd[0])
		pageLogin_u.clickLogin()

	pageLogin_p.inputPword(acc_pwd[1])
	pageLogin_p.clickConfirm()
	if acc:
		try:
			text=pageLogined.textSMS()
			if '手机短信' in text or 'SMS verification' in text:flag=1;logging.info('要求输入验证码')
			else:logging.info(text);flag=0;logging.info('未要求输入验证码')
		except AttributeError:
			flag=0;logging.info('未要求输入验证码')
		if flag:
			if args.env=='prod':
				pageLogined.clickLingpai()
				pageLogined.clickOpenLPapp()

				pageLingpai.inputUnlockpwd()
				pageLingpai.clickGetLP(acc_pwd[0])
				token=pageLingpai.getToken()
				pageBar.goBack(3)

				pageLogined.inputlingpai(token)
				pageLogined.clickConfirm()

			else:
				pageLogined.clickSMS()
				for i in range(5):
					time.sleep(5)					
					# phone=accBinding[acc_pwd[0]][1]
					code=getSMScode('phone',args.env,6)
					pageLogined.inputSMS(code)
					pageLogined.clickConfirm()
					if pageLogined.errToastExists():time.sleep(1);continue
					else:break
		# msg=pageLogined.textEleMsg()
		pageLogined.clickIknow()

	# time.sleep(1)
	if needNickname:nickName=pageMy.textNick()
	logging.info(f'{acc_pwd[0]} {acc_pwd[1]} 登录完成')

def logout(driver):
	# from common.tools import swipeDown
	from page.mine.set import PageSet
	pageBar=PageBar(driver)
	pageMy=PageMy(driver)
	pageSet=PageSet(driver)
	pageAlert=PageAlert(driver)

	pageBar.clickMy()
	pageAlert.clickAlert()
	try:
		nickName=pageMy.textNick(logit=0)
	except AttributeError:
		nickName=0
	if nickName:
		pageMy.clickSet()
		pageSet.clickLogout()#点击安全退出
		# pageSet.clickLogout_confirm()#ios 
		time.sleep(1)
		if driver.capabilities['platformName']=='Android':
			time.sleep(2)
			driver.back()
		logging.info('已登出')
		# swipeDown(driver)
	else:
		logging.info('已是登出状态')
