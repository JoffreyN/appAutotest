import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase

# class PageDeal(PageBase):
# 	def __init__(self,driver):
# 		# 成交 页面
# 		super().__init__(driver)
# 		self.eleFlag=(By.XPATH,'//*[contains(@text,"暂无数据")]')
# 		self.eleFlag1=(By.XPATH,'//*[contains(@text,"已成交")]')

# 	def flagExists(self):
# 		return 1 if self.isEleExists(self.eleFlag) or self.isEleExists(self.eleFlag1) else 0
