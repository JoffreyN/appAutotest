import logging
from selenium.webdriver.common.by import By
from page.base import PageBase

class PageStaticAssets(PageBase):
	def __init__(self,driver):
		# 静态资产 页面
		super().__init__(driver)
		self.flag=(By.XPATH,"//*[contains(text(),'资产总值') or contains(text(),'Asset')]")

	def flagExists(self):
		return self.isEleExists(self.flag,screen=1)