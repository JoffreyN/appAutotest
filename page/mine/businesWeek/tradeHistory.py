import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase

class PageTradeHistory(PageBase):
	def __init__(self,driver):
		# '交易历史 页面
		super().__init__(driver)
		self.item=(By.CLASS_NAME,'item')
		self.record=(By.XPATH,'//*[text()="成交记录" or text()="Transactions"]')

	def getTradeRecord(self):
		time.sleep(2)
		return len(self.findElements(self.item,until='located'))

	def clickRecord(self):
		logging.info('点击 成交记录')
		self.findElement(self.record).click()
