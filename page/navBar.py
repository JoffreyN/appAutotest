import logging,time,urllib3,traceback
from selenium.webdriver.common.by import By
try:
	from appium.webdriver.common.appiumby import AppiumBy
except:
	AppiumBy=By
from common.tools import swipLeft,swithToRightWeb
from common.seleniumError import SCEIESE

from .base import PageBase
from business.others import reOpenApp

class PageBar(PageBase):
	def __init__(self,driver):
		# '下方导航条' 页面
		super().__init__(driver)
		self.wayDic={
			'Android':'id',
			'iOS':'ios_predicate'}
		self.btnHome={
			'Android':(By.ID,'com.cmbi.zytx:id/text_bottom_home_page'),
			'iOS':(AppiumBy.IOS_PREDICATE,"type=='XCUIElementTypeButton' and (name=='首页' or name=='Home')")
		}#首页按钮
		self.btnTrade={
			'Android':(By.ID,'com.cmbi.zytx:id/text_bottom_trade'),
			'iOS':(AppiumBy.IOS_PREDICATE,"type=='XCUIElementTypeButton' and (name=='交易' or name=='Trade')")
		}#交易按钮
		self.btnMy={
			'Android':(By.ID,'com.cmbi.zytx:id/text_bottom_personal'),
			'iOS':(AppiumBy.IOS_PREDICATE,"type=='XCUIElementTypeButton' and (name=='我的' or name=='Me')")
		}#我的按钮
		self.btnNews={
			'Android':(By.ID,'com.cmbi.zytx:id/text_bottom_viewpoint'),
			'iOS':(AppiumBy.IOS_PREDICATE,"type=='XCUIElementTypeButton' and (name=='资讯' or name=='News')")
		}#资讯按钮
		self.btnMarket={
			'Android':(By.ID,'com.cmbi.zytx:id/text_bottom_found'),
			'iOS':(AppiumBy.IOS_PREDICATE,"type=='XCUIElementTypeButton' and (name=='行情' or name=='Quotes')")
		}#行情按钮
		self.eleCookieOut={
			'Android':(By.XPATH,"//*[@text='登录过期' or contains(@text,'expiration') or contains(@text,'expired')]"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='登录过期' or name contains 'expiration' or name contains 'expired'")
		}
		self.eleRelogin={
			'Android':(By.XPATH,"//*[@text='重新登录']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='重新登录'")
		}
		self.btnConfirm={
			'Android':(By.XPATH,"//*[@text='确定' or @text='Confirm' or @text='OK']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='确定' or name=='Confirm' or name=='OK'")
		}

		self.btnClose=(By.ID,'com.cmbi.zytx:id/btn_close')
		self.alertconfirm={
			'Android':(By.XPATH,"//*[@text='确定' or @text='确认' or @text='Confirm']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='确定' or name=='确认' or name=='Confirm'")
		}

	def clickAlert(self):
		#此处点击所有启动之后即出现的弹窗
		try:
			self.findElement(self.alertconfirm[self.PFN],screen=False,timeout=3).click()
			logging.info('点击了弹窗 确定')
		except AttributeError:
			pass

	def clickMy(self,timeout=10,screen=True,swipe=0):
		swithToRightWeb(self.driver,0)
		logging.info('点击 我的')
		time.sleep(0.5)
		# try:
		# 	page_source=self.driver.page_source
		# except urllib3.exceptions.MaxRetryError:
		# 	reOpenApp(self.driver)
		# 	raise urllib3.exceptions.MaxRetryError(f'获取页面源码失败：\n{traceback.format_exc()}')
		# while True:
		# 	if '始终允许' in page_source:
		# 		self.driver.switch_to.alert.accept()
		# 		time.sleep(0.5)
		# 	else:
		# 		break
		for i in range(5):
			try:
				__=True if i==4 else False
				self.waitTo(loc=self.btnMy[self.PFN],operate='click',timeout=timeout,reopen=__,screen=screen)
				self.clickAlert()
				break
			except TimeoutError:
				if self.PFN!='iOS':
					try:self.findElement(self.btnClose,timeout=3,screen=0).click()
					except:pass
				if swipe:swipLeft(self.driver,n=4);swipe=0
				elif self.isEleExists(self.eleCookieOut[self.PFN],timeout=3):
					self.findElement(self.btnConfirm[self.PFN]).click()
				elif self.isEleExists(self.eleRelogin[self.PFN],timeout=3):
					self.findElement(self.eleRelogin[self.PFN]).click()
				else:
					try:
						self.goBack()
					except SCEIESE as err:
						if 'is not running' in str(err):
							reOpenApp(self.driver)
						else:
							raise err

	def clickTrade(self):
		swithToRightWeb(self.driver,0)
		logging.info('点击 交易')
		for i in range(5):
			try:
				__=True if i==4 else False
				self.waitTo(loc=self.btnTrade[self.PFN],operate='click',reopen=__)
				break
			except TimeoutError:
				self.goBack()

	def clickHome(self):
		swithToRightWeb(self.driver,0)
		logging.info('点击 首页')
		for i in range(5):
			try:
				__=True if i==4 else False
				self.waitTo(loc=self.btnHome[self.PFN],operate='click',reopen=__)
				break
			except TimeoutError:
				self.goBack()

	def clickNews(self):
		swithToRightWeb(self.driver,0)
		logging.info('点击 资讯')
		for i in range(5):
			try:
				__=True if i==4 else False
				self.waitTo(loc=self.btnNews[self.PFN],operate='click',reopen=__)
				break
			except TimeoutError:
				self.goBack()

	def clickMarket(self):
		swithToRightWeb(self.driver,0)
		logging.info('点击 行情')
		for i in range(5):
			try:
				__=True if i==4 else False
				self.waitTo(loc=self.btnMarket[self.PFN],operate='click',reopen=__)
				break
			except TimeoutError:
				self.goBack()
