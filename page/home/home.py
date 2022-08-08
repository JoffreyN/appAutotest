import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase
from common.tools import switch_execute

class PageHome(PageBase):
	def __init__(self,driver):
		# 首页 页面
		super().__init__(driver)
		self.btnReload={
			'Android':(By.ID,'com.cmbi.zytx:id/reload_btn'),
			'iOS':(By.IOS_PREDICATE,"name=='reload'")
		}
		self.eleRegister={
			'Android':(By.XPATH,"//*[text()='港美开户']"),
			'iOS':(By.IOS_PREDICATE,"name=='港美开户'")
		}
		self.eleCurrExchange={
			'Android':(By.XPATH,"//*[text()='货币兑换']"),
			'iOS':(By.IOS_PREDICATE,"name=='货币兑换'")
		}
		self.eleRegisterNow=(By.ID,"getAccount")

		#基金板块
		self.btnFundMore={
			'Android':(By.CLASS_NAME,"global-fund-more"),
			'iOS':(By.IOS_PREDICATE,"name=='查看更多'")
		}
		self.eleFund1={
			'Android':(By.CLASS_NAME,"global-fund-name"),
			'iOS':(By.IOS_PREDICATE,"name=='近一年收益率'")
		}
		self.eleFund1Name=(By.CLASS_NAME,"global-fund-name")
		#深度推荐板块 
		self.btnArticleOne={
			'Android':(By.CLASS_NAME,"card"),
			'iOS':(By.XPATH,"//*[@name='关注']/../following-sibling::*[1]")
		}
		self.eleArticleTitle=(By.CLASS_NAME,"detailItem-title")

		self.passwordInput={
			'Android':(By.ID,'com.cmbi.zytx:id/input_trade_password'),
			'iOS':(By.IOS_PREDICATE,"type=='XCUIElementTypeSecureTextField'")
		}
		self.confirm={
			'Android':(By.ID,'com.cmbi.zytx:id/btn_submit'),
			'iOS':(By.IOS_PREDICATE,"name=='确定'")
		}

	@switch_execute
	def inputPwordIFneeded(self):
		try:
			self.findElement(self.passwordInput[self.PFN],timeout=3,screen=0).send_keys('aaaa1111')
			self.findElement(self.confirm[self.PFN],timeout=3,screen=0).click()
		except:
			pass

	# @switch_execute
	def clickReload(self):
		logging.info('点击 reload')
		self.findElement(self.btnReload[self.PFN]).click()
		time.sleep(5)

	def clickRegister(self):
		logging.info('点击 港美开户')
		if self.PFN=='Android':
			self.myTap(self.findElement(self.eleRegister[self.PFN]))
		else:
			self.clickRegister_IOS()

	@switch_execute
	def clickRegister_IOS(self):
		self.findElement(self.eleRegister[self.PFN]).click()

	@switch_execute
	def clickCurrExchange_IOS(self):
		self.findElement(self.eleCurrExchange[self.PFN]).click()

	def clickCurrExchange(self):
		logging.info('点击 货币兑换')
		if self.PFN=='Android':
			self.myTap(self.findElement(self.eleCurrExchange[self.PFN]))
		else:
			self.clickCurrExchange_IOS()
		time.sleep(3)
		self.inputPwordIFneeded()

	def clickRegisterNow(self):
		logging.info('点击 立即开户')
		self.myTap(self.findElement(self.eleRegisterNow))

	#基金板块
	def clickFundMore(self):
		logging.info('点击基金板块 更多 按钮')
		self.driver.execute_script(f'document.getElementById("hotTitle").scrollIntoView();')
		if self.PFN=='Android':
			self.myTap(self.findElement(self.btnFundMore[self.PFN]))
		else:
			self.clickFundMore_IOS()

	@switch_execute
	def clickFundMore_IOS(self):
		self.findElement(self.btnFundMore[self.PFN]).click()

	def textFund1(self):
		self.driver.execute_script('document.querySelector(".hot-fund-img").scrollIntoView();')
		txt=self.findElement(self.eleFund1Name,until='located').get_attribute("innerText")
		return txt

	def clickFund1(self):
		logging.info('点击基金板块中的第1个基金')
		if self.PFN=='Android':
			self.myTap(self.findElement(self.eleFund1[self.PFN]))
		else:
			self.clickFund1_IOS()

	@switch_execute
	def clickFund1_IOS(self):
		self.findElement(self.eleFund1[self.PFN]).click()

	#深度推荐板块
	def textArticleOne(self):
		time.sleep(3)
		self.driver.execute_script('document.getElementsByClassName("card-title")[0].scrollIntoView();')
		time.sleep(1)
		text=self.driver.execute_script('return document.getElementsByClassName("card-title")[0].textContent;')
		return text

	def clickArticleOne(self):
		logging.info('点击深度推荐板块中的第1篇文章')
		time.sleep(3)
		self.driver.execute_script('document.getElementsByClassName("card-title")[0].scrollIntoView();')
		time.sleep(1)
		if self.PFN=='Android':
			self.myTap(self.findElement(self.btnArticleOne[self.PFN]))
		else:
			self.clickArticleOne_IOS()
		
	@switch_execute
	def clickArticleOne_IOS(self):
		self.findElement(self.btnArticleOne[self.PFN]).click()

	def textArticleTitle(self):
		for i in range(10):
			txt=self.findElement(self.eleArticleTitle).text
			if txt:return txt
			else:time.sleep(1)


