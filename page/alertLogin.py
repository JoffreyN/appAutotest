import logging,time
from selenium.webdriver.common.by import By
try:
	from appium.webdriver.common.appiumby import AppiumBy
except:
	AppiumBy=By
from common.tools import switch_execute
from .base import PageBase

class PageAlertLogin(PageBase):
	def __init__(self,driver):
		# 登录态失效出现的弹窗
		super().__init__(driver)
		self.loginButton={
			'Android':(By.ID,'com.cmbi.zytx:id/btn_determine2'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='交易登录' or name=='Trading login'")
		}
		self.passwordInput={
			'Android':(By.ID,'com.cmbi.zytx:id/input_trade_password'),
			'iOS':(AppiumBy.IOS_PREDICATE,"type=='XCUIElementTypeSecureTextField'")
		}


	@switch_execute
	def inputPwordIFneeded(self,pwd):
		if self.isEleExists(self.loginButton[self.PFN],timeout=5):
			logging.info(f'点击 交易登录')
			self.findElement(self.loginButton[self.PFN]).click()
			logging.info(f'输入密码 {pwd}')
			self.findElement(self.passwordInput[self.PFN]).send_keys(pwd)
			logging.info(f'点击 交易登录')
			self.findElement(self.loginButton[self.PFN]).click()
			time.sleep(2)
