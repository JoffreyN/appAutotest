import logging
from selenium.webdriver.common.by import By
try:
	from appium.webdriver.common.appiumby import AppiumBy
except:
	AppiumBy=By
from page.base import PageBase

class PageTrade(PageBase):
	def __init__(self,driver):
		# '交易' 页面
		super().__init__(driver)
		self.loginFlag={
			'Android':(By.XPATH,"//*[@text='交易登录' or @text='Trading login']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='交易登录' or name=='Trading login'")
		}
		self.editPwd={
			'Android':(By.ID,"com.cmbi.zytx:id/input_trade_password"),
			'iOS':(AppiumBy.IOS_PREDICATE,"value contains '输入交易密码'")
		}
		self.btnStockHK={
			'Android':(By.XPATH,"//*[@text='港股' or @text='HK']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='港股' or name=='HK'")
		}
		self.btnStockUS={
			'Android':(By.XPATH,"//*[@text='美股' or @text='US']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='美股' or name=='US'")
		}
		self.btnStockA={
			'Android':(By.XPATH,"//*[@text='中华通' or @text='CN']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='中华通' or name=='CN'")
		}

		self.btnFund={
			'Android':(By.XPATH,"//*[@text='基金' or @text='Funds']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='基金' or name=='Funds'")
		}
		self.btnTrade={
			'Android':(By.XPATH,"//*[@text='股票交易' or @text='Trade']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name contains '股票交易' or name contains 'Trade'")
		}
		self.btnOrder={
			'Android':(By.XPATH,"//*[@text='订单查询' or @text='Order']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='订单查询' or name contains 'Order'")
		}
		self.btnStaticAssets={
			'Android':(By.XPATH,"//*[@text='资产总览' or @text='Asset' or @text='Portfolio']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='资产总览' or name=='Asset' or name=='Portfolio'")
		}
		self.btnInquire={
			'Android':(By.XPATH,"//*[@text='结单查询' or contains(@text,'Statement')]"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='结单查询' or name contains 'Statement'")
		}
		self.btnMore={
			'Android':(By.XPATH,"//*[contains(@text,'更多服务') or contains(@text,'More')]"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name contains '更多' or name contains 'More'")
		}
		# self.btnRegister={
		# 	'Android':(By.XPATH,"//*[@text='立即开户']"),
		# 	'iOS':(AppiumBy.IOS_PREDICATE,"name=='立即开户'")
		# }

		self.holdOne={
			'Android':(By.ID,"com.cmbi.zytx:id/data_layout"),
			'iOS':(AppiumBy.IOS_PREDICATE,'type="XCUIElementTypeCell"')
		}
		self.stockNameOne={
			'Android':(By.ID,"com.cmbi.zytx:id/text_stock_name"),
			'iOS':(By.XPATH,'//*[@type="XCUIElementTypeCell"]/XCUIElementTypeStaticText[1]')
		}
		self.drawerMarket={
			'Android':(By.ID,"com.cmbi.zytx:id/btn_detail"),
			'iOS':(By.XPATH,"//*[@type='XCUIElementTypeCell']/*[@name='行情']")
		}
		self.drawerBuy={
			'Android':(By.ID,"com.cmbi.zytx:id/btn_buy"),
			'iOS':(By.XPATH,"//*[@type='XCUIElementTypeCell']/*[@name='买入']")
		}
		self.drawerSell={
			'Android':(By.ID,"com.cmbi.zytx:id/btn_sell"),
			'iOS':(By.XPATH,"//*[@type='XCUIElementTypeCell']/*[@name='卖出']")
		}
		# 2021-09-14
		self.searchBar={
			'Android':(By.ID,"com.cmbi.zytx:id/search_bar"),
			'iOS':(By.XPATH,"")
		}
		self.searchInput={
			'Android':(By.ID,"com.cmbi.zytx:id/edit_search"),
			'iOS':(By.XPATH,"")
		}

	def inputKeyword(self,keyword):
		logging.info(f'输入关键词 {keyword}')
		self.findElement(self.searchInput[self.PFN]).send_keys(keyword)

	def clickSearch(self):
		logging.info(f'交易页面点击搜索框')
		self.findElement(self.searchBar[self.PFN]).click()

	def loginFlagExists(self):
		return self.isEleExists(self.loginFlag[self.PFN],5)

	def inputPwd(self,pwd):
		logging.info(f'输入登录密码 {pwd}')
		self.findElement(self.editPwd[self.PFN]).send_keys(pwd)

	def clickloginFlag(self):
		logging.info('点击 交易登录')
		self.findElement(self.loginFlag[self.PFN]).click()

	def clickStockHK(self):
		logging.info('点击 港股 按钮')
		self.findElement(self.btnStockHK[self.PFN]).click()

	def clickStockUS(self):
		logging.info('点击 美股 按钮')
		self.findElement(self.btnStockUS[self.PFN]).click()

	def clickStockA(self):
		logging.info('点击 中华通 按钮')
		self.findElement(self.btnStockA[self.PFN]).click()

	def clickFund(self):
		logging.info('点击 基金 按钮')
		self.findElement(self.btnFund[self.PFN]).click()

	def clickTrade(self):
		logging.info('点击 股票交易 按钮')
		if self.PFN=='iOS':
			eles=self.findElements(self.btnTrade[self.PFN],until='located')
			for ele in eles:
				try:ele.click()
				except:pass
		else:
			self.findElement(self.btnTrade[self.PFN]).click()

	def clickOrder(self):
		logging.info('点击 订单查询 按钮')
		if self.PFN=='iOS':
			eles=self.findElements(self.btnOrder[self.PFN],until='located')
			for ele in eles:
				try:ele.click()
				except:pass
		else:
			self.findElement(self.btnOrder[self.PFN]).click()

	def clickStaticAssets(self):
		logging.info('点击 资产总览 按钮')
		self.findElement(self.btnStaticAssets[self.PFN]).click()

	def clickInquire(self):
		logging.info('点击 结单查询 按钮')
		self.findElement(self.btnInquire[self.PFN]).click()

	def clickMore(self,n=0):
		logging.info('点击 更多 按钮')
		self.findElements(self.btnMore[self.PFN])[n].click()

	# def clickRegister(self):
	# 	logging.info('点击 立即开户')
	# 	self.findElement(self.btnRegister[self.PFN]).click()

	def clickHoldOne(self):
		logging.info('点击 第一个持仓股票，打开抽屉')
		self.findElement(self.holdOne[self.PFN]).click()

	def getStockNameOne(self):
		return self.findElement(self.stockNameOne[self.PFN]).text

	def clickDrawerMarket(self):
		logging.info('点击 抽屉里的行情')
		self.findElement(self.drawerMarket[self.PFN]).click()

	def clickDrawerBuy(self):
		logging.info('点击 抽屉里的买入')
		self.findElement(self.drawerBuy[self.PFN]).click()

	def clickDrawerSell(self):
		logging.info('点击 抽屉里的卖出')
		self.findElement(self.drawerSell[self.PFN]).click()
