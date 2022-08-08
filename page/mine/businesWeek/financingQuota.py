import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase

class PageFinancingQuota(PageBase):
	def __init__(self,driver):
		# 融资额度申请 页面
		super().__init__(driver)
		self.editAmount=(By.CLASS_NAME,"md-input-item-input")
		self.btnSubmit=(By.CSS_SELECTOR,".submit")
		self.eleRespMsg=(By.ID,"resp-message-text")
		self.btnCancel=(By.XPATH,"//*[text()='撤销申请']")
		self.btnComfirm=(By.XPATH,"//*[text()='确定']")
		self.eleCancelMsg=(By.XPATH,"//*[text()='提交申请']")

		#新页面
		self.marketHKD=(By.XPATH,"//*[contains(text(),'港股市场')]")
		self.marketUSD=(By.XPATH,"//*[contains(text(),'美股市场')]")


	def clickmarketHKD(self):
		logging.info('点击 港股市场')
		self.findElement(self.marketHKD).click()

	def clickmarketUSD(self):
		logging.info('点击 美股市场')
		self.findElement(self.marketUSD).click()

	def inputAmount(self):
		logging.info('输入申请额度')
		for i in range(5):
			try:
				self.findElement(self.editAmount).send_keys('1000')
				return
			except AttributeError:
				time.sleep(1)
				if i==4:raise AttributeError('输入融资金额失败')

	def clickSubmit(self):
		logging.info('点击 提交申请')
		self.findElement(self.btnSubmit).click()

	def textRespMsg(self):
		return self.findElement(self.eleRespMsg).text

	def clickCancel(self):
		logging.info('点击 撤销申请')
		self.findElement(self.btnCancel).click()

	def clickComfirm(self):
		logging.info('点击 确定')
		self.findElement(self.btnComfirm).click()

	def cancelMsgExists(self):
		return 1 if self.isEleExists(self.eleCancelMsg) else 0

