import logging,time,traceback

def switchServer(driver,env='UAT',swipe=0):
	from page.navBar import PageBar
	from page.mine.my import PageMy
	from page.mine.set import PageSet
	from common.seleniumError import SCENSEE
	PFN=driver.capabilities['platformName']
	pageBar=PageBar(driver)
	pageMy=PageMy(driver)
	pageSet=PageSet(driver)

	time.sleep(0.5)
	if PFN=='Android':
		try:
			driver.find_element_by_xpath("//*[@text='同意']").click()
		except SCENSEE:
			pass
		except:
			logging.error(traceback.format_exc())

	for i in range(3):
		try:
			pageBar.clickMy(swipe=swipe)
			pageMy.clickSet()
			break
		except AttributeError:
			pass

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
	time.sleep(1)
	driver.back()
	return reopen

def reOpenApp(driver):
	logging.info('重启APP...')
	# driver.close_app()
	driver.terminate_app(driver.capabilities['app_id'])
	time.sleep(2)
	# driver.launch_app()
	driver.activate_app(driver.capabilities['app_id'])
	try:
		PFN=driver.capabilities['platformName']
	except KeyError:
		PFN='Android'
		
	if PFN=='Android':
		time.sleep(10)
		driver.tap([(1285,2850)])
		time.sleep(5)
	else:
		time.sleep(5)
