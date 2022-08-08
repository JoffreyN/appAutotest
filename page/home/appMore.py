import logging
from selenium.webdriver.common.by import By
from page.base import PageBase

class PageMore(PageBase):
	def __init__(self,driver):
		# 更多 页面
		super().__init__(driver)
		self.flag=(By.CLASS_NAME,"more")

	def flagExists(self):
		return self.isEleExists(self.flag)