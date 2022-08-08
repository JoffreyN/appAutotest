import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase

class PageCRS(PageBase):
	def __init__(self,driver):
		# CRS 页面
		super().__init__(driver)
		#第一步
		self.btnperson=(By.XPATH,"//*[text()='个人账户登记']")
		self.btnCompany=(By.XPATH,"//*[text()='公司实体登记']")

		#第二步
		self.btnName=(By.ID,"form-crs-title")
		self.btnComfirm=(By.XPATH,"//*[text()='确定']")
		self.eleAddr=(By.ID,"form-crs-stay")
		self.eleCity=(By.ID,"form-crs-staycity")
		self.eleState=(By.ID,"form-crs-staystate")
		self.eleCountry=(By.ID,"form-crs-staycountry")
		self.country_china=(By.XPATH,"//*[@class='country-code-container']/div[1]")

		self.TaxNumber=(By.ID,"form-no1-card")
		self.cardid=(By.ID,"form-crs-hkid-passport")
		self.btnSubmit=(By.XPATH,"//*[text()='提交CRS表格']/../..")

		self.email=(By.ID,"form-company-email")
		self.btnSubmitCompany=(By.XPATH,"//*[text()='获取公司实体CRS表格']/../..")

		#第三步
		self.btnMsg=(By.XPATH,"//*[contains(text(),'处理中') or contains(text(),'查收邮件')]")

	#第一步
	def clickperson(self):
		logging.info('点击 个人账户登记')
		self.findElement(self.btnperson,until='located').click()

	def clickCompany(self):
		logging.info('点击 公司实体登记')
		self.findElement(self.btnCompany,until='located').click()
	
	#第二步
	def clickName(self):
		logging.info('点击 称呼')
		self.findElement(self.btnName).click()

	def clickComfirm(self):
		logging.info('点击 确定')
		self.findElement(self.btnComfirm).click()

	def inputAddr(self):
		logging.info('输入 住址')
		self.findElement(self.eleAddr).send_keys('万象天地')

	def inputCity(self):
		logging.info('输入 城市')
		self.findElement(self.eleCity).send_keys('深圳市')

	def inputState(self):
		logging.info('输入 省份')
		self.findElement(self.eleState).send_keys('广东省')

	def inputCountry(self):
		logging.info('点击 国家 并选择中国')
		ele=self.findElement(self.eleCountry)
		self.driver.execute_script("arguments[0].scrollIntoView();",ele)
		ele.click()
		self.findElement(self.country_china).click()

	def inputTaxNumber(self):
		logging.info('输入 税务编号')
		self.findElement(self.TaxNumber).send_keys('123456')

	def inputIDcrad(self):
		logging.info('输入 证件号')
		self.findElement(self.cardid).send_keys('123451654466')

	def clickSubmit(self):
		logging.info('点击 提交CRS表格')
		self.findElement(self.btnSubmit).click()

	def inputEmail(self):
		logging.info('输入邮箱')
		time.sleep(3)
		self.findElement(self.email).clear()
		self.findElement(self.email).send_keys('2806646694@qq.com')

	def clickSubmitCompany(self):
		logging.info('点击 获取公司实体CRS表格')
		self.findElement(self.btnSubmitCompany).click()

	#第三步
	def msgExists(self):
		# n=0 公司；n=1 个人
		for i in range(10):
			text=self.findElement(self.btnMsg,until='located').text
			if text:
				return text
			else:
				time.sleep(1)
		return ''

	def msgCompanyExists(self):
		for i in range(10):
			if self.isEleExists(self.btnMsgCompany):
				return 1
			else:
				time.sleep(1)
		return 0