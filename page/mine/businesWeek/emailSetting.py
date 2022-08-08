import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase

class PageEmailSetting(PageBase):
	def __init__(self,driver):
		# 通知设置 页面
		super().__init__(driver)
		#第一步
		self.close=(By.CLASS_NAME,"check-box01")#关闭通知
		self.open=(By.CLASS_NAME,"check-box02")#打开通知
		self.save=(By.CLASS_NAME,"save")#保存

	def clickClose(self):
		logging.info('点击 关闭通知')
		self.myTap(self.findElement(self.close))

	def clickOpen(self):
		logging.info('点击 打开通知')
		self.myTap(self.findElement(self.open))

	def clickSave(self):
		logging.info('点击 保存')
		# self.findElement(self.save).click()
		self.driver.execute_script(f"document.getElementsByClassName('save')[0].click();")
		time.sleep(1)