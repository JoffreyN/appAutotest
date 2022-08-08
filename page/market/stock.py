import logging
from selenium.webdriver.common.by import By
from page.base import PageBase
from common.seleniumError import SCESERE

class PageStock(PageBase):
	def __init__(self,driver):
		# 个股详情 页面
		super().__init__(driver)
		self.btnDayK={
			'Android':(By.ID,"com.cmbi.zytx:id/chart_fragment_container"),
			'iOS':(By.IOS_PREDICATE,"name=='分时'")
		}
		self.btnTrade={
			'Android':(By.ID,"com.cmbi.zytx:id/btn_stock_detail_trade"),# btn_stock_detail_trade
			'iOS':(By.IOS_PREDICATE,"name=='交易' or name=='Trade'")
		}
		self.stockName={
			'Android':(By.ID,"com.cmbi.zytx:id/text_stock_name"),
			'iOS':(By.XPATH,'//*[@type="XCUIElementTypeNavigationBar"]/XCUIElementTypeStaticText[1]')
		}
		
		self.btnAnalysis=(By.XPATH,"//*[text()='分析']")
		self.btnNotice=(By.XPATH,"//*[text()='公告']")
		self.btnFinance=(By.XPATH,"//*[text()='财务']")
		self.btnProfile=(By.XPATH,"//*[text()='简况']")
		self.btnNews=(By.XPATH,"//*[text()='新闻']")

		self.btnListTitle=(By.CLASS_NAME,'list-T')
		self.datailTitle=(By.CLASS_NAME,'detailItem-title')

		self.bmpText={
			'Android':(By.XPATH,"//*[contains(@text,'BMP行情，需要手动刷新') or contains(@text,'BMP quotes need manual refresh')]"),
			'iOS':(By.IOS_PREDICATE,"name contains 'BMP行情，需要手动刷新' or name contains 'BMP quotes need manual refresh'")
		}

	def BMPflagExists(self):
		return self.isEleExists(self.bmpText[self.PFN])		

	def clickTrade(self):
		logging.info('点击 交易')
		for i in range(5):
			try:
				self.findElement(self.btnTrade[self.PFN]).click()
				return
			except SCESERE:
				if i==4:raise SCESERE('点击交易按钮失败')
				time.sleep(1)

	def flagExists(self):
		return self.isEleExists(self.btnDayK[self.PFN])

	def clickAnalysis(self):
		logging.info('点击 分析Tab')
		self.findElement(self.btnAnalysis).click()

	def clickNotice(self):
		logging.info('点击 公告Tab')
		self.findElement(self.btnNotice).click()

	def clickFinance(self):
		logging.info('点击 财务Tab')
		self.findElement(self.btnFinance).click()

	def clickProfile(self):
		logging.info('点击 简况Tab')
		self.findElement(self.btnProfile).click()

	def clickNews(self):
		logging.info('点击 新闻Tab')
		self.findElement(self.btnNews).click()

	def listOneTitle(self):
		return self.findElement(self.btnListTitle).text

	def clickListOne(self):
		logging.info('点击第一条新闻')
		self.findElement(self.btnListTitle).click()

	def getDetailTitle(self):
		return self.findElement(self.datailTitle).text
 
	def getStockName(self):
		return self.findElement(self.stockName[self.PFN]).text
