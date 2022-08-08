import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase


class PageImExportHistory(PageBase):
	def __init__(self,driver):
		# '资金存取记录' 页面
		super().__init__(driver)
		self.btnImportHistory=(By.XPATH,"//*[text()='存入资金' or text()='Deposit']")
		self.btnExportHistory=(By.XPATH,"//*[text()='提取资金' or text()='Withdraw']")

		self.eleImCancels=(By.XPATH,"//*[contains(text(),'网银') or contains(text(),'Online banking')  or contains(text(),'ATM') or contains(text(),'资金存入')]")#存入
		self.eleExCancels=(By.XPATH,"//*[contains(text(),'银行') or contains(text(),'***')]")#提取
		self.btnCancel={
			'in':(By.XPATH,"//*[@id='capitalInputRecordBr']/following-sibling::div[1]//div[@class='van-list']//*[text()='撤回' or text()='Cancel']"),
			'out':(By.XPATH,"//*[@id='capitalOutRecordBr']/following-sibling::div[1]//div[@class='van-list']//*[text()='撤回' or text()='Cancel']"),
			}
		self.btnTerminated={
			'in':(By.XPATH,"//*[@id='capitalInputRecordBr']/following-sibling::div[1]//div[@class='van-list']//*[text()='已终止' or text()='Remitted']"),
			'out':(By.XPATH,"//*[@id='capitalOutRecordBr']/following-sibling::div[1]//div[@class='van-list']//*[text()='已终止' or text()='Remitted']"),
			}
		
		self.btnConfirm=(By.XPATH,"//*[text()='确认' or text()='Confirm']/../..")

	def clickImportHistory(self):
		logging.info('点击存入记录')
		self.findElement(self.btnImportHistory).click()
	
	def clickExportHistory(self):
		logging.info('点击提取资金')
		self.findElement(self.btnExportHistory).click()
		if self.PFN=='Android':
			self.clickExportHistory_And()
		time.sleep(1)

	# @switch_execute
	def clickExportHistory_And(self):
		self.myDriverTap((520,310),(1440,2960))
		# self.driver.tap([(520,310)])

	def imCancelsExists(self):
		return self.isEleExists(self.eleImCancels)

	def exCancelsExists(self):
		return self.isEleExists(self.eleExCancels)

	def getNumTerminated(self,t='in'):
		try:
			num=len(self.findElements(self.btnTerminated[t],until='located',screen=False))
		except TypeError:
			num=0
		return num

	def clickCancel(self,t='in'):
		logging.info('点击撤回')
		self.findElement(self.btnCancel[t]).click()

	def clickConfirm(self):
		logging.info('点击 确认')
		self.findElement(self.btnConfirm).click()
