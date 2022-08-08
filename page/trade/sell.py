import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase

from common.tools import switch_execute,scrollByXpath
from common.seleniumError import SCEECIE

class PageSell(PageBase):
	def __init__(self,driver):
		# '新版卖出' 页面
		super().__init__(driver)
		self.tradeSell=(By.XPATH,"//*[contains(text(),'切换卖出') or contains(text(),'Sell')]/..")
		self.editStock=(By.TAG_NAME,'input')#第0个
		self.eleStockOne=(By.CSS_SELECTOR,'.item.van-hairline--top')
		self.elePrices=(By.XPATH,"//*[@class='control-range-sell amount--font']/div[1]")#5档行情
		self.input=(By.TAG_NAME,'input')
		self.btnSell=(By.CSS_SELECTOR,'.precast-btn.sell')
		self.sellNum=(By.CSS_SELECTOR,'.sell-num')
		# self.eleResultStockCode=(By.XPATH,"//*[@class='hold-content']/div[1]/div[2]/div[1]/span[5]")#当前委托第一条里的股票代码
		
		# self.eleTradeType={
		# 	'Android':(By.XPATH,"//*[contains(@text,'限价单')]"),
		# 	'iOS':(By.IOS_PREDICATE,"name contains '限价单'")
		# }
		# self.selectLessPan={
		# 	'Android':(By.XPATH,"//*[contains(@text,'碎股单')]"),
		# 	'iOS':(By.IOS_PREDICATE,"name=='碎股单'")
		# }

		# 新版交易页面
		self.input_new={
			'Android':(By.CLASS_NAME,'search-text'),# webview
			'iOS':(By.XPATH,"//*[contains(@name,'请输入股票代码') or contains(@name,'name to search')]")# ios 点击无反应，需要切换至原生
		}
		self.eleBuyPrices_new=(By.XPATH,"//*[@class='control-range-buy']/div[1]")#买1
		self.eleSellPrices_new=(By.XPATH,"//*[@class='control-range-sell']/div[1]")#卖1
		self.eleResultStockCode_new=(By.XPATH,'//*[@class="order-box"]/div[1]//div[@class="item-name"]//span')#当前委托第一条里的股票代码
		self.eleNumOne={
			'Android':(By.XPATH,"//*[text()='1手' or text()='1Lot']"),
			'iOS':(By.XPATH,"//*[@name='1手' or @name='1Lot']")
		}
		self.orderType=(By.CLASS_NAME,'control-info-type')
		self.maxSell={
			'iOS':(By.XPATH,'//XCUIElementTypeOther[@name="股票交易"]/XCUIElementTypeOther[19]/XCUIElementTypeOther[1]'),
			'Android':(By.XPATH,"//*[@resource-id='app']/android.view.View[2]/android.view.View[5]")
		}
		self.input_num=(By.XPATH,"//*[@class='num']//span")#输入股数的输入框

		self.btnPan={# 点击切换单
			'Android':(By.XPATH,'//*[@resource-id="app"]/android.view.View[2]/android.view.View[2]/android.view.View[2]/android.view.View[2]'),
			'iOS':(By.XPATH,'//*[@name="股票交易"]/XCUIElementTypeOther[9]/XCUIElementTypeOther[2]')
		}
		self.panName1={# 增强限价单
			'Android':(By.XPATH,'//*[@resource-id="app"]/android.view.View[4]/android.view.View[2]'),
			'iOS':(By.XPATH,'//*[@name="股票交易"]/XCUIElementTypeOther[33]')		
		}
		self.panName2={# 限价单
			'Android':(By.XPATH,'//*[@resource-id="app"]/android.view.View[4]/android.view.View[3]'),
			'iOS':(By.XPATH,'//*[@name="股票交易"]/XCUIElementTypeOther[34]')		
		}
		self.panName3={# 特殊限价单
			'Android':(By.XPATH,'//*[@resource-id="app"]/android.view.View[4]/android.view.View[4]'),
			'iOS':(By.XPATH,'//*[@name="股票交易"]/XCUIElementTypeOther[35]')		
		}
		self.panName4={# 竞价限价单
			'Android':(By.XPATH,'//*[@resource-id="app"]/android.view.View[4]/android.view.View[5]'),
			'iOS':(By.XPATH,'//*[@name="股票交易"]/XCUIElementTypeOther[36]')		
		}
		self.panName5={# 竞价单
			'Android':(By.XPATH,'//*[@resource-id="app"]/android.view.View[4]/android.view.View[6]'),
			'iOS':(By.XPATH,'//*[@name="股票交易"]/XCUIElementTypeOther[37]')		
		}
		self.panName6={# 碎股单
			'Android':(By.XPATH,'//*[@resource-id="app"]/android.view.View[4]/android.view.View[6]'),
			'iOS':(By.XPATH,'//*[@name="股票交易"]/XCUIElementTypeOther[38]')		
		}
		self.eleFlag1=(By.XPATH,'//pns(text(),"不支持")]')

	def flag1Exists(self):
		return self.isEleExists(self.eleFlag1)

	@switch_execute
	def changePan(self,panName):
		logging.info(f'点击打开单菜单')
		self.findElement(self.btnPan[self.PFN],until='located').click()

		xpathDict={
			'增强限价单':self.panName1,
			'限价单':self.panName2,
			'特殊限价单':self.panName3,
			'竞价限价单':self.panName4,
			'竞价单':self.panName5,
			'碎股单':self.panName5,
		}
		logging.info(f'点击选择 {panName}')
		self.findElement(xpathDict[panName][self.PFN]).click()
		
	@switch_execute
	def clickmaxSell(self):
		logging.info('点击 最大可卖')
		self.findElement(self.maxSell[self.PFN],until='located').click()

	def get_input_num(self):
		return float(self.findElement(self.input_num).text.replace(',','').strip())


	def getorderType(self):
		return self.findElement(self.orderType).text.strip()

	def getMaxSellNum(self):
		text=self.findElement(self.sellNum).text.replace(',','').strip()
		logging.info(f'最大可卖为: {text}')
		return float(text)

	def flagExists(self):
		return self.isEleExists(self.btnSell)

	@switch_execute
	def clickNumOne_ios(self):
		self.findElement(self.eleNumOne[self.PFN]).click()

	def clickNumOne(self):
		logging.info('点击 1手')
		if self.PFN=='Android':
			self.myTap(self.findElement(self.eleNumOne[self.PFN]))
		else:
			self.clickNumOne_ios()

	def clickTradeSell(self):
		logging.info('点击 切换卖出')
		self.myTap(self.findElement(self.tradeSell))
		if self.PFN=="Android":time.sleep(3)

	@switch_execute
	def clickInput_ios(self):
		self.findElement(self.input_new[self.PFN]).click()

	def clickInput(self):
		logging.info('点击输入框')
		if self.PFN=='Android':
			self.myTap(self.findElement(self.input_new[self.PFN]))
		else:
			self.clickInput_ios()

	def inputStock(self,stockCode):
		logging.info(f'输入股票代码 {stockCode}')
		self.findElement(self.editStock).send_keys(stockCode)

	def clickStockOne(self,stockCode):
		logging.info('点击 出现的股票列表中的第一个')
		self.findElement(self.eleStockOne).click()

	def clickPriceOne(self):
		logging.info('点击 卖1价')
		try:
			self.findElement(self.elePrices).click()
		except SCEECIE:
			try:self.driver.switch_to.context(self.driver.contexts[0])
			except AttributeError:pass
			logging.info(f'已切换为原生context')
			addImage(self.driver.get_screenshot_as_base64(),msg,traceback.format_exc())
			raise SCEECIE('元素无法点击')

	def inputNum(self,n=2):
		logging.info(f'输入数量 {n}')
		self.findElements(self.input)[-1].send_keys(n)

	# @switch_execute
	# def chooseLessPan(self):
	# 	logging.info('点击选择碎骨单')
	# 	for i in range(5):
	# 		self.findElement(self.eleTradeType[self.PFN]).click()
	# 		try:
	# 			self.findElement(self.selectLessPan[self.PFN]).click()
	# 			return
	# 		except AttributeError:
	# 			if i==4:raise AttributeError('切换碎骨单失败，无法唤出下拉列表')
	# 			continue

	def clickSell(self):
		logging.info('点击 卖出')
		self.clickByScript(self.findElement(self.btnSell,until='located'))


	def textResultStockCode(self,xpath=1):
		for i in range(3):
			time.sleep(5)
			try:
				scrollByXpath(self.driver,self.eleResultStockCode_new[1])
				return self.findElement(self.eleResultStockCode_new,until='located').text.strip()
			except AttributeError:
				continue
		return '获取委托列表中第一条记录失败'