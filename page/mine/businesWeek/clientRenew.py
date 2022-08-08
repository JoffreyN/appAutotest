import logging,time
from selenium.webdriver.common.by import By
try:
	from appium.webdriver.common.appiumby import AppiumBy
except:
	AppiumBy=By
from page.base import PageBase

class PageClientrenew(PageBase):
	def __init__(self,driver):
		# 资料年审 页面
		# http://uat-app.cmbi.online/servicefo/static/client-renew.html
		super().__init__(driver)
		self.start=(By.XPATH,"//span[contains(text(),'开始') or contains(text(),'Start')]/..")
		self.passport=(By.XPATH,"//input[@name='passport_expire_date']")
		self.closepicker=(By.CLASS_NAME,"close-picker")
		self.next1=(By.XPATH,'//button[contains(text(),"下一步，个人资料") or contains(text(),"personal")]')
		self.email=(By.XPATH,"//input[@name='email2']")
		self.next2=(By.XPATH,'//button[contains(text(),"下一步，工作财务") or contains(text(),"employment")]')
		self.next3=(By.XPATH,'//button[contains(text(),"下一步，税务财务") or contains(text(),"Tax")]')
		self.next4=(By.XPATH,'//button[contains(text(),"确认及签署") or contains(text(),"Confirm and sign")]')
		self.checkBox_crs=(By.XPATH,'//input[@type="checkbox" and @name="confirm_crs"]')
		self.checkBox_fatca=(By.XPATH,'//input[@type="checkbox" and @name="confirm_fatca"]')
		self.checkBox_agreement=(By.XPATH,'//input[@type="checkbox" and @name="confirm_account_agreement"]')
		self.ttcanvas=(By.ID,'ttcanvas')
		self.next5=(By.XPATH,'//button[contains(text(),"简易投资目标") or contains(text(),"Simple investment")]')
		self.next6=(By.XPATH,'//button[contains(text(),"身份披露") or contains(text(),"identity")]')
		self.next7=(By.XPATH,'//button[contains(text(),"提交资料") or contains(text(),"Submit")]')
		self.flag=(By.XPATH,'//div[contains(text(),"审核中") or contains(text(),"Verifying")]')
		self.withdraw=(By.XPATH,'//button[contains(text(),"撤回申请") or contains(text(),"Withdraw")]')
		self.Yes=(By.XPATH,'//span[contains(text(),"确认") or contains(text(),"Yes")]')
		self.close={
			'Android':(By.ID,'com.cmbi.zytx:id/btn_close'),
			'iOS':(AppiumBy.ID,'close black')
		}

	def clientRenew_sign(self):
		logging.info(f'开始签名')
		canvas=self.findElement(self.ttcanvas)
		x1,y1=canvas.location.values()
		h,w=canvas.size.values()
		x2,y2=x1+w,y1+h
		self.driver.swipe(x1+100,y1+100,x2-100,y2-100,200)

	def clickYes(self):
		logging.info(f'点击确认')
		eles=self.findElements(self.Yes,until='located')
		for e in eles:
			try:
				e.click()
			except:
				pass