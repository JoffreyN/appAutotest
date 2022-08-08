import logging
from selenium.webdriver.common.by import By
try:
	from appium.webdriver.common.appiumby import AppiumBy
except:
	AppiumBy=By
from page.base import PageBase

class PageLogin_p(PageBase):
	def __init__(self,driver):
		# 登录时要求输入密码的页面
		super().__init__(driver)
		self.editPword={
			'Android':(By.ID,'com.cmbi.zytx:id/input_password'),
			'iOS':(By.XPATH,'//*[@name="明码关"]/../XCUIElementTypeSecureTextField')

		}
		self.btnConfirm={
			'Android':(By.ID,'com.cmbi.zytx:id/btn_confirm'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='确认' or name=='Confirm'")
		}

		self.btnSMS={
			'Android':(By.ID,'com.cmbi.zytx:id/btn_sms_quickly_login'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='短信快捷验证' or name contains 'SMS verification'")
		}#短信快捷验证按钮
		self.editSMS={
			'Android':(By.ID,'com.cmbi.zytx:id/input_sms_code'),
			'iOS':(AppiumBy.IOS_PREDICATE,"value contains '输入验证码' or value=='verification code'")
		}#短信验证码输入框

		self.forgetpwd={
			'Android':(By.ID,'com.cmbi.zytx:id/btn_forget_password'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='忘记密码？' or name contains 'Forgot'")
		}

	def inputPword(self,pword):
		logging.info(f'输入密码 {pword}')
		self.findElement(self.editPword[self.PFN]).send_keys(pword)

	def clickConfirm(self):
		logging.info('点击 确认 按钮')
		self.findElement(self.btnConfirm[self.PFN]).click()

	def clickSMS(self):
		logging.info('点击 短信快捷验证 按钮')
		self.findElement(self.btnSMS[self.PFN]).click()

	def inputSMS(self,smsCode):
		logging.info('输入 短信验证码，用于手机短信登录')
		# self.findElement(self.editSMS[self.PFN]).click()
		self.findElement(self.editSMS[self.PFN]).send_keys(smsCode)

	def clickForgetpwd(self):
		logging.info('点击 忘记密码')
		self.findElement(self.forgetpwd[self.PFN]).click()