import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase
from common.tools import scrollByXpath

class PageImportMoney(PageBase):
	def __init__(self,driver):
		# '资金存入' 页面
		super().__init__(driver)
		# 第一步页面 选择币种
		self.btnCNY=(By.XPATH,"//*[contains(text(),'CNY') or contains(text(),'CNH')]")
		self.btnHKD=(By.XPATH,"//*[contains(text(),'HKD')]")
		self.btnUSD=(By.XPATH,"//*[contains(text(),'USD')]")
		#第二步页面 选择银行 
		self.btnHKbankCard=(By.XPATH,"//*[contains(text(),'已持有')]")
		self.btnOtherBank=(By.XPATH,"//*[contains(text(),'其他香港银行') or contains(text(),'Remittance from other')]")
		#第三步页面 选择汇入银行
		self.btnNext=(By.XPATH,"//*[text()='已汇款，下一步' or contains(text(),'Remittance completed')]")
		self.btnYes=(By.XPATH,"//*[text()='是的' or text()='Yes']")
		#第四步页面 填写信息
		self.btnExportBank=(By.XPATH,'//*[text()="存款银行" or text()="Remittance bank"]')
		self.btnWingLungBank=(By.XPATH,"//*[contains(text(),'香港上海汇丰银行') or contains(text(),'WING LUNG BANK LTD')]")
		self.Keyboard=(By.ID,'myKeyboardNodot')
		self.Keyboard2=(By.ID,'myKeyboardNodot2')
		self.uploadPic=(By.TAG_NAME,'input')
		# self.btnChoosePic=(By.XPATH,"//*[@content-desc='选择文件']")
		# self.btnFiles=(By.XPATH,"//*[@text='文档']")
		self.btnPic=(By.ID,"com.android.documentsui:id/icon_thumb")
		# self.btnLoading=(By.XPATH,"//*[@text='读取中']")
		self.btnSubmit=(By.XPATH,"//*[text()='提交' or text()='Submit']")
		self.btnIknow=(By.XPATH,"//*[text()='知道了' or text()='Got it']")
		# self.btnDone=(By.XPATH,"//*[text()='完成']")
		#第六步页面 查看提交状态
		self.eleStatus=(By.XPATH,"//*[contains(text(),'已提交') or contains(text(),'submitted')]")

		self.fieldCheck=(By.XPATH,"//*[contains(@class,'account')]/div[1]")#存入账户
		self.fieldCheck2=(By.XPATH,"//*[contains(@class,'depositNo')]/div[1]")#存款账号

	def getField(self):
		return self.findElement(self.fieldCheck).text

	def getField2(self):
		return self.findElement(self.fieldCheck2).text

	# 第一步
	def clickCurr(self,curr):
		logging.info(f'点击 {curr}')
		_xpath={
			'HKD':self.btnHKD,
			'USD':self.btnUSD,
			'CNY':self.btnCNY,
		}
		self.findElement(_xpath[curr],timeout=30).click()

	def clickHKbankCard(self):
		logging.info('点击 已持有香港银行卡')
		self.findElement(self.btnHKbankCard,until='located').click()

	def clickOtherBank(self):
		logging.info('点击 其他香港银行汇出')
		self.findElement(self.btnOtherBank).click()

	#第三步
	def clickNext(self):
		logging.info('点击 已汇款，下一步')
		self.findElement(self.btnNext).click()

	def clickYes(self):
		logging.info('点击 是的')
		self.findElement(self.btnYes).click()
	#第四步
	def clickExportBank(self):
		logging.info('点击选择存款银行')
		self.findElement(self.btnExportBank).click()

	def clickWingLungBank(self):
		logging.info('点击选择香港上海汇丰银行')
		self.findElement(self.btnWingLungBank).click()

	def clickKeyboard(self,t=1):
		tDic={1:'金额',0:'银行卡号'}
		KeyboardDic={1:self.Keyboard,2:self.Keyboard2}
		logging.info(f'点击输入 {tDic[t]}')
		# self.findElement(KeyboardDic[t]).click()
		self.findElements(self.Keyboard)[t].click()

	def clickUploadPic(self):
		logging.info('点击选择文件')
		scrollByXpath(self.driver,self.btnSubmit[1])
		if self.PFN=='Android':
			self.findElement(self.uploadPic,until='located').click()
			# self.driver.execute_script(f"document.getElementsByTagName('{self.uploadPic[1]}')[0].click();")
		else:
			self.clickByRightXY((70,715))
			# 70,726 ios
		time.sleep(1)

	def clickPic(self):
		logging.info('点击选择图片')
		time.sleep(3)
		self.findElement(self.btnPic).click()

	# def loadingEnd(self):
	# 	from common.seleniumError import SCENSEE
	# 	time.sleep(4)
	# 	while 1:
	# 		try:
	# 			if self.driver.find_element(*self.btnLoading):continue
	# 		except SCENSEE:
	# 			return 1

	def clickSubmit(self):
		logging.info('点击 提交')
		self.findElement(self.btnSubmit).click()

	def clickIknow(self):
		logging.info('点击 知道了')
		try:
			self.findElement(self.btnIknow,screen=0).click()
		except:
			pass

	# def clickDone(self):
	# 	logging.info('点击 完成')
	# 	self.findElement(self.btnDone).click()

	# 第六步
	def textStatus(self):
		return self.isEleExists(self.eleStatus)

	def clickView(self):
		logging.info('点击 查看存取资金记录')
		self.findElement(self.eleView).click()