import logging
from selenium.webdriver.common.by import By
try:
	from appium.webdriver.common.appiumby import AppiumBy
except:
	AppiumBy=By
from page.base import PageBase

class PageStatement(PageBase):
	def __init__(self,driver):
		# 结单查询 页面
		super().__init__(driver)
		self.statement_day=(By.XPATH,"//*[contains(text(),'日结单') or contains(text(),'Daily')]")
		self.statement_month=(By.XPATH,"//*[contains(text(),'月结单') or contains(text(),'Monthly')]")
		self.view=(By.XPATH,"//span[text()='查看' or text()='View']")
		self.flag_read={
			'Android':(By.XPATH,"//*[@text='阅读结单' or @text='Statement Details']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='阅读结单' or name=='Statement Details'")
		}

	def flagExists(self):
		return self.isEleExists(self.statement_day)

	def click_statement(self,types):
		logging.info(f'點擊 {types} 結單')
		xpathDict={'日':self.statement_day,'月':self.statement_month}
		self.findElement(xpathDict[types]).click()

	def click_view(self,n=0):
		logging.info(f'點擊查看')
		self.findElements(self.view,until='located')[n].click()

	def flagRead_Exists(self):
		return self.isEleExists(self.flag_read[self.PFN])