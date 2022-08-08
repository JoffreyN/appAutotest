import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase

class PageFakeTrade(PageBase):
	def __init__(self,driver):
		# 模拟炒股 页面
		super().__init__(driver)
		self.eleAmount=(By.CLASS_NAME,"total")
		self.getFakerMoney=(By.XPATH,'//*[text()="立即领取"]')

	def clickgetFakerMoney(self):
		try:
			self.findElement(self.getFakerMoney,screen=0,timeout=5).click()
		except AttributeError:
			pass

	def textAmount(self):
		return self.findElement(self.eleAmount,until='located').text
