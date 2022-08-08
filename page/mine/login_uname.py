import logging
from selenium.webdriver.common.by import By
try:
	from appium.webdriver.common.appiumby import AppiumBy
except:
	AppiumBy=By
from page.base import PageBase
from common.system_appadmin import getSwitchStatus

class PageLogin_u(PageBase):
	def __init__(self,driver):
		# 登录时要求输入账户名的页面
		super().__init__(driver)
		self.editUname={
			'Android':(By.ID,'com.cmbi.zytx:id/input_account'),
			'iOS':(AppiumBy.IOS_PREDICATE,"type=='XCUIElementTypeTextField'")
		}
		self.btnLogin={
			'Android':(By.ID,'com.cmbi.zytx:id/btn_login'),
			'iOS':(AppiumBy.IOS_PREDICATE,"(name=='注册/登录' or name=='Register/Login') and type=='XCUIElementTypeButton'")
		}
		self.btnCheckView={
			'Android':(By.ID,'com.cmbi.zytx:id/statement_check_view'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name CONTAINS '已阅读' or name contains 'read'")
		}
		self.confirm={
			'Android':(By.ID,'com.cmbi.zytx:id/btn_confirm'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name contains '确认' or name contains 'confirm'")
		}
		self.unCheckFlag={
			'Android':(By.XPATH,"//*[contains(@text,'后勾选同意') or contains(@text,'have read and agreed to')]"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name contains '后勾选同意' or name contains 'have read'")
		}
		self.forgetAcc={
			'Android':(By.XPATH,"//*[contains(@text,'忘记证券账户') or contains(@text,'Forgot')]"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name contains '忘记证券账户' or name contains 'Forgot'")
		}

	def clickForgetAcc(self):
		logging.info('点击 忘记证券账户')
		self.findElement(self.forgetAcc[self.PFN]).click()

	def clickConfirm(self):
		logging.info('点击 确认')
		self.findElement(self.confirm[self.PFN]).click()

	def unCheckFlagExists(self):
		return self.isEleExists(self.unCheckFlag[self.PFN],timeout=5)

	def inputUname(self,uname):
		logging.info(f'输入用户名 {uname}')
		self.findElement(self.editUname[self.PFN]).send_keys(uname)

	def clickLogin(self):
		logging.info('点击 注册/登录 按钮')
		self.findElement(self.btnLogin[self.PFN]).click()

	def clickCheckView(self,appVersion,env='uat',only=0):
		if only:
			logging.info('点击勾选同意')
			self.findElement(self.btnCheckView[self.PFN]).click()
		elif appVersion>'3.1.6.0000':
			if self.PFN=='Android':
				if getSwitchStatus('USER_LOGIN_PRIVACY_SWITCH',env)=='关闭':
					logging.info('点击勾选同意')
					self.findElement(self.btnCheckView[self.PFN]).click()
