import logging,time
from page.base import PageBase
from selenium.webdriver.common.by import By
try:
	from appium.webdriver.common.appiumby import AppiumBy
except:
	AppiumBy=By
from common.seleniumError import SCESERE,SCEWDE
from common.tools import swipeUp,switch_execute,scrollByXpath

class PageOrders(PageBase):
	def __init__(self,driver):
		# 新版交易查看委托页面
		super().__init__(driver)
		# http://uat-app.cmbi.online/appweb/trade/entrust?changesetting=re...
		self.todayOrders=(By.XPATH,"//*[text()='今日订单' or contains(text(),'Today')]")
		# self.eleFlag=(By.XPATH,'//*[text()="订单查询"]')

		# self.__xpath='//*[@resource-id="app"]/android.view.View[2]/android.view.View[2]/android.view.View[1]/android.view.View[2]'
		# self.__xpath2='//*[@resource-id="app"]/android.view.View[2]/android.view.View[2]/android.view.View[2]/android.view.View[2]'

		self.btnStockInfo={
			'Android':(By.XPATH,"//*[text()='行情' or text()='Quotes']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='行情' or name=='Quotes'")
		}#行情
		self.btnOrderDetail={
			'Android':(By.XPATH,"//*[text()='详情' or text()='Details']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='详情' or name=='Details'")
		}#详情
		self.btnChangeOrder={
			'Android':(By.XPATH,"//*[contains(text(),'修改') or contains(text(),'Modify')]"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name contains '修改' or name contains 'Modify'")
		}#改单
		self.btnCancelOrder={
			'Android':(By.XPATH,"//*[text()='撤单' or text()='Cancel']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='撤单' or name=='Cancel'")
		}#撤单

		self.eleChangeDetail=(By.CSS_SELECTOR,".change-item")#改单记录 1
		self.stockCode=(By.XPATH,'//*[@class="entrust-item active"]//div[@class="item-name"]//span[1]')# 股票代码
		self.stockName=(By.XPATH,'//*[@class="entrust-item active"]//div[@class="item-name"]/p[1]')# 股票名称

		self.PYPL=(By.XPATH,"//*[text()='02018']/../..")
		self.PYPL_edit=(By.XPATH,"//*[text()='02018']/../../../div[2]/span[3]")
		self.flagDetil=(By.XPATH,"//*[text()='委托状态' or text()='Order Status']")

		# 新改单界面
		self.price_jian={
			'Android':(By.CSS_SELECTOR,'.item.minus'),# webview
			'iOS':(By.XPATH,'//XCUIElementTypeOther[@name="改单"]/XCUIElementTypeOther[11]'),# 切换至原生仍然无法点击
		}
		self.changeRecords=(By.XPATH,"//*[text()='撤改记录' or text()='Modify Record']/..")
		self.changeRecords_ios=(By.XPATH,'//*[@name="撤改记录" or @name="Modify Record"]')

	# @switch_execute
	def clickPriceMinus_order(self,n=3):
		logging.info(f'点击价格减{n}次')# 
		if self.PFN=='iOS':
			for i in range(n):
				time.sleep(0.5)
				self.myDriverTap([297,215],[375,768])
		else:
			for i in range(3):
				time.sleep(0.5)
				self.myTap(self.findElements(self.price_jian[self.PFN],until='located')[0])
		time.sleep(1)
		# ele=self.findElement(self.price_jian[self.PFN],until='located')
		# for i in range(3):
		# 	self.myTap(ele)

	def detilFlagExists(self):
		return self.isEleExists(self.flagDetil)

	def openPYPL(self):
		logging.info('点击打开 02018')
		ele=self.findElement(self.PYPL)
		if self.PFN=='Android':
			self.myTap(ele)
		else:
			x,y=ele.location.values()
			h,w=ele.size.values()
			self.driver.tap([(int(x+w/2),int(y+h))])

	def getStockCode(self,i=0):
		return self.findElements(self.stockCode)[i].text

	def getStockName(self,i=0):
		return self.findElements(self.stockName)[i].text

	def clickTodayOrders(self):
		logging.info('点击 今日订单')
		self.findElement(self.todayOrders).click()

	def flagExists(self):
		return self.isEleExists(self.todayOrders)

	def clickOrderDetail(self):
		time.sleep(3)
		logging.info('点击 详情 按钮')
		if self.PFN=='Android':
			for i in range(5):
				try:
					self.myTap(self.findElement(self.btnOrderDetail[self.PFN]))
					return
				except SCEWDE:
					time.sleep(1)
		else:
			context=self.driver.current_context
			self.driver.switch_to.context(self.driver.contexts[0])
			self.findElement(self.btnOrderDetail[self.PFN]).click()
			self.driver.switch_to.context(context)

	def clickStockInfo(self):
		time.sleep(2)
		logging.info('点击 行情 按钮')
		if self.PFN=='Android':
			self.myTap(self.findElement(self.btnStockInfo[self.PFN]))
		else:
			context=self.driver.current_context
			self.driver.switch_to.context(self.driver.contexts[0])
			self.findElement(self.btnStockInfo[self.PFN]).click()
			self.driver.switch_to.context(context)

	def clickChangeOrder(self):
		time.sleep(2)
		logging.info('点击 修改 按钮')
		if self.PFN=='Android':
			self.myTap(self.findElement(self.btnChangeOrder[self.PFN]))
		else:
			context=self.driver.current_context
			self.driver.switch_to.context(self.driver.contexts[0])
			self.findElement(self.btnChangeOrder[self.PFN]).click()
			self.driver.switch_to.context(context)

	def clickCancelOrder(self):
		time.sleep(2)
		logging.info('点击 撤单 按钮')
		if self.PFN=='Android':
			self.myTap(self.findElement(self.btnCancelOrder[self.PFN]))
		else:
			context=self.driver.current_context
			self.driver.switch_to.context(self.driver.contexts[0])
			self.findElement(self.btnCancelOrder[self.PFN]).click()
			self.driver.switch_to.context(context)

	@switch_execute
	def clickChangeRecords_ios(self):
		ele=self.findElement(self.changeRecords_ios)
		self.clickByEleXY(ele)

	def clickChangeRecords(self):
		time.sleep(2)
		logging.info(f'点击撤改记录')
		ele=self.findElement(self.changeRecords,until='located')
		self.driver.execute_script("arguments[0].scrollIntoView();",ele)
		time.sleep(2)
		if self.PFN=='iOS':
			self.clickChangeRecords_ios()
		else:
			self.myTap(ele)

	def changeDetailExists(self):
		return self.isEleExists(self.eleChangeDetail)

	def cancelDetailExists(self):
		eles=self.findElements(self.eleChangeDetail,until='located')
		return 1 if len(eles)>1 else 0

	def getOrderPrice(self):
		for i in range(10):
			try:
				price=float(self.driver.execute_script('return document.querySelector(".active").getElementsByClassName("item-content")[0].getElementsByTagName("span")[1].textContent;').strip())
				return str(round(price+0.6))
			except SCEWDE:
				if i==9:raise SCEWDE('获取订单价格失败！')
				time.sleep(1)