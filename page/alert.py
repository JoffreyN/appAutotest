import logging,time
from selenium.webdriver.common.by import By
try:
	from appium.webdriver.common.appiumby import AppiumBy
except:
	AppiumBy=By
from common.tools import switch_execute
from .base import PageBase

class PageAlert(PageBase):
	def __init__(self,driver):
		# 专治各种弹窗，影响代码执行的那种
		super().__init__(driver)
		self.confirm={
			'Android':(By.ID,'com.cmbi.zytx:id/btn_determine2'),# //*[@text='确定' or @text='确认']
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='确定' or name=='确认'")
		}

		self.passwordInput={
			'Android':(By.ID,'com.cmbi.zytx:id/input_trade_password'),
			'iOS':(AppiumBy.IOS_PREDICATE,"type=='XCUIElementTypeSecureTextField'")
		}
		self.confirmPwd={
			'Android':(By.ID,'com.cmbi.zytx:id/btn_submit'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='确定'")
		}
		self.allow={
			'Android':(By.ID,'com.android.packageinstaller:id/permission_allow_button'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='允许'")
		}
		self.alert_close={
			'Android':(By.ID,'com.cmbi.zytx:id/close_btn'),
			'iOS':(AppiumBy.ID,"关闭 s")
		}
		self.alert_iKnow={
			'Android':(By.XPATH,"//*[@text='我知道了']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='我知道了'")
		}

	def clickAlert_iKnow(self):
		try:
			self.findElement(self.alert_iKnow[self.PFN],screen=False,timeout=5).click()
			logging.info('点击关闭弹窗 我知道了')
		except AttributeError:
			pass

	def clickAlert_close(self):
		try:
			self.findElement(self.alert_close[self.PFN],screen=False,timeout=1).click()
			logging.info('点击关闭弹窗')
		except AttributeError:
			pass

	@switch_execute
	def inputPwordIFneeded(self):
		try:
			self.findElement(self.passwordInput[self.PFN],timeout=2,screen=0).send_keys('aaaa1111')
			self.findElement(self.confirmPwd[self.PFN],timeout=2,screen=0).click()
		except:
			pass

	@switch_execute
	def clickAlert(self):
		#此处点击所有启动之后即出现的弹窗
		try:
			self.findElement(self.confirm[self.PFN],screen=False,timeout=1).click()
			logging.info('点击了弹窗 确定')
		except AttributeError:
			pass
		# self.clickAlert_close()

	@switch_execute
	def clickAllow(self):
		try:
			self.findElement(self.allow[self.PFN],screen=False,timeout=1).click()
			logging.info('点击了弹窗 允许')
			return 1
		except AttributeError:
			return 0