import logging,time
from selenium.webdriver.common.by import By
try:
	from appium.webdriver.common.appiumby import AppiumBy
except:
	AppiumBy=By
from page.base import PageBase
from common.tools import swipeDown,switch_execute,scrollByXpath,swithToRightWeb,myAddScreen
from common.seleniumError import SCEWDE,SCEIESE


class PageFund(PageBase):
	def __init__(self,driver):
		# '基金' 页面
		super().__init__(driver)
		self.alert={
			'Android':(By.XPATH,'//*[@text="我知道了" or @text="Got it"]'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='我知道了' or name=='Got it'")
		}
		# self.size=(self.driver.get_window_size()['width'],self.driver.get_window_size()['height'])
		# self.flag=(By.XPATH,"//*[contains(text(),'风险评级')]")
		self.flag_fundOrders=(By.XPATH,"//*[contains(text(),'当前委托') or contains(text(),'Today')]")
		self.flag_mine={
			'Android':(By.XPATH,"//*[contains(@text,'添加自选') or contains(@text,'一键添加') or contains(@text,'Add All')]"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name CONTAINS '添加自选' or name CONTAINS '一键添加' or name contains 'Add All'")
		}
		self.btnAccount={
			'Android':(By.ID,"com.cmbi.zytx:id/account_id_view"),
			'iOS':(By.XPATH,'//*[@name="hotline black"]/../XCUIElementTypeOther[2]/XCUIElementTypeOther[1]')
		}#iOS需要第 1 个
		self.btnLogin={
			'Android':(By.XPATH,'//*[@text="交易登录" or @text="Trading login"]'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='交易登录' or name=='Trading login'")
		}
		# self.eleTradeAcc=(By.ID,"text_trade_account")
		self.editPwd={
			'Android':(By.ID,"com.cmbi.zytx:id/input_trade_password"),
			'iOS':(AppiumBy.IOS_PREDICATE,"type=='XCUIElementTypeSecureTextField'")
		}

		self.btnFundOrder={
			'Android':(By.XPATH,'//*[@text="基金市场" or @text="Fund Market"]'),
			'iOS':(By.XPATH,'(//XCUIElementTypeStaticText[@name="基金市场" or @name="Fund Market"])[1]')
		}

		self.btnOptionalFund={
			'Android':(By.XPATH,'//*[@text="基金自选" or @text="Watchlist"]'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='基金自选' or name=='Watchlist'") 
		}
		self.btnfundorderquery={
			'Android':(By.XPATH,'//*[@text="订单查询" or @text="Order Query"]'),
			'iOS':(By.XPATH,'(//XCUIElementTypeStaticText[@name="订单查询" or @name="Order Query"])[1]')
		}
		self.btnFilter=(By.XPATH,'//ul[@id="cellTh_all"]/div/div[2]')
		self.btnReset=(By.XPATH,'//div[@id="fund_list_0"]/div[3]/div[2]/div[3]/div[2]/button[1]')#重置
		# //div[@id="fund_list_0"]/div[3]/div[2]/div[3]/div[2]/button[1] #确定
		self.btnFilterUS={
			'Android':(By.XPATH,"//*[@class='title' and (contains(text(),'货币') or contains(text(),'Currency'))]/following-sibling::div[1]//button[1]"),# webview
			'iOS':(AppiumBy.IOS_PREDICATE,'name contains "美元" or name contains "US Dollar"')
		}
		self.btnFilterHK={
			'Android':(By.XPATH,"//*[@class='title' and (contains(text(),'货币') or contains(text(),'Currency'))]/following-sibling::div[1]//button[2]"),# webview
			'iOS':(AppiumBy.IOS_PREDICATE,'name contains "港元" or name contains "Hong Kong Dollar"')
		}
		self.btnFilterLowRisk={
			'Android':(By.XPATH,"//*[@class='title' and (contains(text(),'风险等级') or contains(text(),'Risk Level'))]/following-sibling::div[1]//button[5]"),# webview
			'iOS':(AppiumBy.IOS_PREDICATE,'name=="低风险" or name contains "Very Low"')
		}

		self.btnFundOne=(By.XPATH,'//div[@class="cell-left"]/div[1]')#第1条基金
		self.btnFundisin=(By.CLASS_NAME,"name_en")
		# self.btnFundName2=(By.CLASS_NAME,"fund-name")#基金详情标题
		# self.btnBuy=(By.XPATH,"//*[text()='申购' or text()='购买']")
		self.buy=(By.CLASS_NAME,'doPurchase')
		self.buy2=(By.CLASS_NAME,'submitAble')
		self.buyPlan=(By.CLASS_NAME,'castSurely')
		self.buyPlan2=(By.XPATH,'//span[text()="定投" or text()="Create Investment Plan"]/..')
		self.checkPlan=(By.XPATH,'//*[text()="查看我的定投" or text()="My Plan"]')
		# self.btnDone={
		# 	# 'Android':(By.XPATH,"//*[text()='完成']"),
		# 	'iOS':(AppiumBy.IOS_PREDICATE,"name=='完成'")
		# }
		self.editAmount=(By.XPATH,'//div[@class="input-content"]')
		self.btnAgree=(By.CLASS_NAME,'van-checkbox')
		# self.btnAgree={
		# 	'Android':(By.XPATH,"//*[@role='checkbox']"),
		# 	'iOS':(AppiumBy.IOS_PREDICATE,"name CONTAINS '本人确认'")
		# }
		# self.btnAgree1={
		# 	'Android':(By.XPATH,""),
		# 	'iOS':(AppiumBy.IOS_PREDICATE,"name CONTAINS '本人已阅读'")
		# }
		self.btnComfirmBuy=(By.CSS_SELECTOR,".van-dialog__confirm")#确认购买
		self.iKnow=(By.XPATH,'//*[text()="我知道了" or text()="Got it"]/../..')

		# self.eleSuccessMsg=(By.XPATH,"//*[text()='申购成功']")
		self.eleComfirm={
			'Android':(By.XPATH,"//*[text()='确定' or text()='确认' or text()='Confirm']/../.."),
			'iOS':(By.XPATH,"//*[text()='确定' or text()='确认' or text()='Confirm']/..")
		}
		# self.eleComfirmNav={
		# 	'Android':(By.XPATH,"//*[@text='确定' or @text='确认']"),
		# 	'iOS':(AppiumBy.IOS_PREDICATE,"name=='确定' or name=='确认'")
		# }

		self.eleOrderName=(By.XPATH,'//div[text()="ISIN"]/../div[@class="cell-value"]')
		
		self.fundHold={
			'Android':(By.ID,"com.cmbi.zytx:id/data_layout"),
			'iOS':(By.XPATH,"//XCUIElementTypeCell")
		}
		self.btnDetail={
			'Android':(By.ID,"com.cmbi.zytx:id/btn_detail"),
			'iOS':(By.XPATH,'//XCUIElementTypeStaticText[@name="行情" or @name="Quotes"]')
		}#行情按钮
		self.btnApplyBuy={
			'Android':(By.ID,"com.cmbi.zytx:id/btn_buy"),
			'iOS':(By.XPATH,'//XCUIElementTypeStaticText[@name="申购" or @name="Subscribe"]')
		}#申购按钮
		self.btnRedeem={
			'Android':(By.ID,"com.cmbi.zytx:id/btn_redeem"),
			'iOS':(By.XPATH,'//XCUIElementTypeStaticText[@name="赎回" or @name="Redeem"]')
		}#赎回按钮
		self.btnRedeem1=(By.XPATH,'//*[text()="赎回" or text()="Redeem"]')
		# self.eleSuccessMsg1=(By.XPATH,"//*[text()='申请成功']")
		self.eleRedeemFlag=(By.CLASS_NAME,"item-type")

		self.flag_Details=(By.XPATH,"//*[text()='基金详情' or text()='Fund Detail']")
		self.flag_applyBuy=(By.XPATH,"//*[contains(text(),'申购金额') or contains(text(),'Subscription Amount')]")
		self.flag_redeem=(By.XPATH,"//*[text()='赎回份额' or text()='Redeemption Units']")

		# 2022-01-11 新页面
		self.allFund=(By.XPATH,'//div[text()="全部基金" or text()="Fund Finder"]/..')
		self.minMoney=(By.XPATH,'//div[@class="input-content"]//span[@class="placeholder"]')

		self.planItems=(By.XPATH,'//div[@class="van-list"]/div[1]')# 定投计划列表里的第一条
		self.stopPlan=(By.XPATH,'//div[text()="终止" or text()="End"]')
		self.stopedPlan=(By.XPATH,'//div[text()="已终止" or text()="End"]')

	def flag_stopedPlan(self):
		return self.isEleExists(self.stopedPlan,10)

	def clickstopPlan(self):
		logging.info(f'点击终止')
		ele=self.findElement(self.stopPlan)
		self.clickByScript(ele)

	def clickplanItems(self):
		logging.info(f'点击进行中')
		self.findElement(self.planItems).click()

	def clickAllfund(self):
		logging.info(f'点击全部基金')
		self.findElement(self.allFund).click()

	def getMinMoney(self):
		logging.info(f'获取最小认购金额')
		text=self.findElement(self.minMoney).text
		logging.info(f'最小认购金额为: {text}')
		try:
			money=float(re.findall(r'\d+.\d+',text)[0])+50
		except:
			logging.info('提取金额失败')
			money='50000'



	@switch_execute
	def clickIknow(self):
		try:
			self.findElement(self.alert[self.PFN],timeout=5,screen=0).click()
			logging.info('点击 我知道了')
		except AttributeError:
			pass

	def flag_applyBuyExists(self):
		return self.isEleExists(self.flag_applyBuy,20)

	def flag_redeemExists(self):
		return self.isEleExists(self.flag_redeem,20)

	def flag_DetailsExists(self):
		return self.isEleExists(self.flag_Details,20)

	def flagExists(self):
		return self.isEleExists(self.flag,20)

	def flagExists_mine(self):
		return self.isEleExists(self.flag_mine[self.PFN],20)
	
	def flagExists_fundOrders(self):
		return self.isEleExists(self.flag_fundOrders,20)

	def clickOpen(self):
		logging.info('点击 打开功能抽屉')
		self.findElement(self.fundHold[self.PFN]).click()

	def clickDetail(self):
		logging.info('点击 行情')
		self.findElement(self.btnDetail[self.PFN]).click()

	def clickApplyBuy(self):
		logging.info('点击 申购')
		self.findElement(self.btnApplyBuy[self.PFN]).click()

	def clickRedeem(self):
		logging.info('点击 赎回 按钮')
		time.sleep(1)
		self.clickOpen()
		for i in range(3):
			try:
				self.findElement(self.btnRedeem[self.PFN]).click()
				return
			except AttributeError:
				from common.tools import swipeDown
				swipeDown(self.driver)
				time.sleep(2)
		raise AttributeError('点击 赎回 按钮失败')

	def inputShare(self):
		time.sleep(3)
		logging.info('输入赎回份额')
		self.findElement(self.editAmount,until='located').send_keys('100')
		# if self.PFN=='iOS':
		# 	self.findElement(self.btnDone[self.PFN]).click()

	def clickRedeem1(self):
		logging.info('点击 赎回')
		self.findElement(self.btnRedeem1).click()

	# def successMsg1Exists(self):
	# 	return self.isEleExists(self.eleSuccessMsg1)

	def textRedeemFlag(self):
		return self.findElements(self.eleRedeemFlag)[0].text

	def clickAccount(self):
		logging.info('点击切换户口')
		self.findElement(self.btnAccount[self.PFN]).click()
		# if self.PFN!='iOS':
		# 	self.findElement(self.btnAccount[self.PFN]).click()
		# else:
		# 	self.findElements(self.btnAccount[self.PFN],until='located')[1].click()

	# def textAccount(self):
	# 	return self.findElement(self.btnAccount[self.PFN]).text

	def clickAccount1(self,acc):
		logging.info('点击第二个户口')
		from testData.data import accBinding
		mAcc=accBinding[acc][0]
		self.btnAccount1={
			'Android':(By.XPATH,f"//*[contains(@text,'{mAcc}')]"),
			'iOS':(AppiumBy.IOS_PREDICATE,f"name CONTAINS '{mAcc}'")
		}
		self.findElement(self.btnAccount1[self.PFN]).click()
		return mAcc

	def loginExists(self,timeout=10):
		time.sleep(1)
		return self.isEleExists(self.btnLogin[self.PFN],timeout=timeout)

	def clickLogin(self):
		logging.info('点击 交易登录')
		self.findElement(self.btnLogin[self.PFN]).click()

	def inputPwd(self,pwd):
		logging.info(f'输入密码 {pwd}')
		self.findElement(self.editPwd[self.PFN]).send_keys(pwd)

	def clickFundMarket(self):
		logging.info('点击 基金市场')
		self.findElement(self.btnFundOrder[self.PFN]).click()

	def clickOptionalFund(self):
		logging.info('点击 基金自选')
		self.findElement(self.btnOptionalFund[self.PFN]).click()

	def clickFundorderquery(self):
		# http://uat-app.cmbi.online/appweb/fund-sys/records?from=app&...
		logging.info('点击 订单查询')
		self.findElement(self.btnfundorderquery[self.PFN]).click()

	# def clickComfirmNav(self):
	# 	logging.info('点击 确定/确认')
	# 	self.findElement(self.eleComfirmNav[self.PFN]).click()

	# @switch_execute
	def clickFilter(self):
		logging.info('点击 筛选')
		self.findElement(self.btnFilter,until='located').click()
		time.sleep(3)
		# self.myTap(self.findElement(self.btnFilter,until='located'))

	def clickReset(self):
		logging.info('点击 重置')
		self.findElement(self.btnReset,until='located').click()
		# for i in range(3):
		# 	try:
		# 		self.myTap(self.findElement(self.btnReset))
		# 		return
		# 	except SCEWDE:
		# 		time.sleep(1)

	def clickFilterUS(self):
		logging.info('点击筛选 美元')
		if  self.PFN=='iOS':
			swithToRightWeb(self.driver,0)
			self.findElement(self.btnFilterUS[self.PFN]).click()
			# if self.driver.capabilities['deviceName']=='iPhone 11 Pro Max':
			# 	self.driver.tap([(145,315)])
			# elif self.driver.capabilities['deviceName']=='iPhone 11 Pro':
			# 	self.driver.tap([(133,296)])
			# elif self.driver.capabilities['deviceName']=='iPhone 11':
			# 	self.driver.tap([(145,315)])
		else:
			self.myTap(self.findElement(self.btnFilterUS[self.PFN],screen=False))

	def clickFilterHK(self):
		logging.info('点击筛选 港元')
		if  self.PFN=='iOS':
			swithToRightWeb(self.driver,0)
			self.findElement(self.btnFilterHK[self.PFN]).click()
			# if self.driver.capabilities['deviceName']=='iPhone 11 Pro Max':
			# 	self.driver.tap([(225,315)])
			# elif self.driver.capabilities['deviceName']=='iPhone 11 Pro':
			# 	self.driver.tap([(202,293)])
			# elif self.driver.capabilities['deviceName']=='iPhone 11':
			# 	self.driver.tap([(225,315)])
		else:
			self.myTap(self.findElement(self.btnFilterHK[self.PFN],screen=False))

	def clickFilterLowRisk(self):
		logging.info('点击筛选 低风险')
		if  self.PFN=='iOS':
			self.findElement(self.btnFilterLowRisk[self.PFN]).click()
			# if self.driver.capabilities['deviceName']=='iPhone 11 Pro Max':
			# 	self.driver.tap([(255,455)])
			# elif self.driver.capabilities['deviceName']=='iPhone 11 Pro':
			# 	self.driver.tap([(232,420)])
			# elif self.driver.capabilities['deviceName']=='iPhone 11':
			# 	self.driver.tap([(255,455)])
		else:
			self.myTap(self.findElement(self.btnFilterLowRisk[self.PFN],screen=False))

	def clickFundOne(self):
		time.sleep(2)
		logging.info('点击 第1条基金')
		self.findElement(self.btnFundOne,until='located').click()

	def textFundisin(self):
		text=self.findElement(self.btnFundisin).text
		return text

	# def textFundName2(self):
	# 	for i in range(10):
	# 		txt=self.findElement(self.btnFundName2).text
	# 		if 'ISIN' in txt:time.sleep(1)
	# 		else:return txt

	def clickBuy(self):
		logging.info('点击 申购')
		# self.driver.execute_script('document.getElementsByClassName("purchase doPurchase")[0].click()')
		self.findElement(self.buy,until='located').click()

	def clickBuyPlan(self):
		logging.info('点击 定投')
		# self.driver.execute_script('document.getElementsByClassName("purchase doPurchase")[0].click()')
		self.findElement(self.buyPlan,until='located').click()

	def clickBuyPlan2(self):
		logging.info('点击 定投')
		# self.driver.execute_script('document.getElementsByClassName("purchase doPurchase")[0].click()')
		scrollByXpath(self.driver,self.buyPlan2[1])
		self.findElement(self.buyPlan2,until='located').click()

	def clickCheckPlan(self):
		logging.info('点击 查看我的定投')
		# self.driver.execute_script('document.getElementsByClassName("purchase doPurchase")[0].click()')
		try:
			self.findElement(self.checkPlan,until='located').click()
		except Exception as err:
			myAddScreen(self,'截图')
			raise err

	def clickBuy2(self):
		logging.info('点击 买入')
		# self.driver.execute_script('document.getElementsByClassName("purchase doPurchase")[0].click()')
		self.findElement(self.buy2).click()

	def clickInputAmount(self):
		logging.info('点击唤起键盘')
		try:
			self.findElement(self.editAmount,until='located').click()
		except Exception as err:
			myAddScreen(self,'点击唤起键盘失败')
			raise err
		# for i in range(5):
		# 	try:
		# 		self.findElements(self.editAmount,until='located')[-1].send_keys(str(money))
		# 		return
		# 	except SCEIESE:
		# 		time.sleep(1)

	# @switch_execute
	# def clickAgree_IOS(self):
	# 	self.findElement(self.btnAgree[self.PFN]).click()

	def clickAgree(self):
		logging.info('点击 勾选')
		eles=self.findElements(self.btnAgree,until='located')
		for e in eles:
			try:
				e.click()
			except:
				pass
		# time.sleep(2)
		# if self.PFN=='iOS':
		# 	self.clickAgree_IOS()
		# else:
			# self.myTap(self.findElements(self.btnAgree[self.PFN])[0])

	# @switch_execute
	# def clickAgree1_IOS(self):
	# 	# self.findElement(self.btnAgree1[self.PFN]).click()
	# 	ele=self.findElement(self.btnAgree1[self.PFN])
	# 	self.driver.tap([tuple(ele.location.values())])

	# def clickAgree1(self,n=1):
	# 	logging.info('点击 本人已阅读')
	# 	self.findElements(self.btnAgree,until='located')[n].click()
		# if self.PFN=='iOS':
		# 	self.clickAgree1_IOS()
		# else:
		# 	self.myTap(self.findElements(self.btnAgree[self.PFN])[n])

	def clickComfirmBuy(self):
		logging.info('点击 确认')
		self.findElement(self.btnComfirmBuy).click()

	def clickIknow_web(self):
		logging.info('点击 我知道了')
		try:
			self.findElement(self.iKnow).click()
		except:
			pass

	# def successMsgExists(self):
	# 	return self.isEleExists(self.eleSuccessMsg)

	def clickComfirm(self,js=None):
		# xy=(335,745)
		logging.info('点击 确定/确认')
		if js and self.PFN=='iOS':
			self.driver.execute_script('document.querySelector(".confirm").getElementsByClassName("md-button-inner")[0].click();')
			time.sleep(1)
			self.driver.execute_script('document.querySelector(".confirm").getElementsByClassName("md-button-inner")[0].click();')
		else:
			self.myTap(self.findElement(self.eleComfirm[self.PFN],screen=False))

	def textOrderName(self):
		return self.findElement(self.eleOrderName).text
