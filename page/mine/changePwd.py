import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase
from common.seleniumError import SCEENVE

class PageChangePwd(PageBase):
	def __init__(self,driver):
		# 修改登录密码 页面
		super().__init__(driver)
		self.old_pwd=(By.ID,'password')
		self.new_pwd=(By.ID,'new-password')
		self.confirm_pwd=(By.ID,'confirm-password')
		self.setPassword=(By.XPATH,"//*[@onclick='postSetPassword()']")
		self.setPassword_ttl=(By.XPATH,"//*[text()='修改密码' or text()='Change password']/../..")
		self.Done=(By.XPATH,"//*[text()='完成' or text()='Done']")
		self.Done_ttl=(By.XPATH,"//*[text()='完成' or text()='Complete']/../..")

		self.type_pwd=(By.XPATH,"//*[@type='password']")


	def inputOldPwd(self,keyword,ttl=0):
		logging.info(f'输入旧密码 {keyword}')
		if ttl:
			self.findElements(self.type_pwd,until='located')[0].send_keys(keyword)
		else:
			self.findElement(self.old_pwd).send_keys(keyword)
		
		
	def inputNewPwd(self,keyword,ttl=0):
		logging.info(f'输入新密码 {keyword}')
		if ttl:
			self.findElements(self.type_pwd,until='located')[1].send_keys(keyword)
		else:
			self.findElement(self.new_pwd).send_keys(keyword)

	def inputConfirmPwd(self,keyword,ttl=0):
		logging.info(f'再次输入新密码 {keyword}')
		if ttl:
			self.findElements(self.type_pwd,until='located')[2].send_keys(keyword)
		else:
			self.findElement(self.confirm_pwd).send_keys(keyword)

	def clickSetPassword(self,ttl=0):
		logging.info('点击 修改密码')
		# time.sleep(10)
		if ttl:
			self.findElement(self.setPassword_ttl).click()
		else:
			self.findElement(self.setPassword).click()

	def clickDone(self,ttl=0):
		logging.info('点击 完成')
		for i in range(10):
			try:
				if ttl:
					self.findElement(self.Done_ttl).click()
				else:
					self.findElement(self.Done).click()
				return
			except SCEENVE as e:
				if i==9:raise e
				time.sleep(1)





