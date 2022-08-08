import logging,time
from random import randint
from page.base import PageBase
from selenium.webdriver.common.by import By


class PageBankCard(PageBase):
	def __init__(self,driver):
		# 银行卡 页面
		super().__init__(driver)
		#第一步
		# self.eleBanks=(By.CLASS_NAME,"android.widget.ListView")
		self.btnBankAdd=(By.CLASS_NAME,"jumpTobalance")
		self.btnBankEdit=(By.XPATH,'//*[text()="编辑" or text()="Edit"]/../..')
		self.btnBankDelete=(By.XPATH,'//*[text()="删除" or text()="Delete"]/../..')
		self.bankCode=(By.CLASS_NAME,"accountNumber")

		#第二步
		self.btnChooseBank=(By.CLASS_NAME,"bankList")
		self.btnBankName=(By.XPATH,f"//*[@class='oftenUseListInner']/li[{randint(1,10)}]")
		self.keyboard=(By.ID,'myKeyboardNodot')
		self.accType=(By.CLASS_NAME,'bankTypeList')
		self.accHKD=(By.XPATH,'//*[text()="港币账户" or text()="HKD Account"]')
		self.accUSD=(By.XPATH,'//*[text()="美元账户" or text()="USD Account"]')
		self.accCNY=(By.XPATH,'//*[text()="人民币账户" or text()="CNH Account"]')
		self.submit=(By.XPATH,'//*[text()="保存" or text()="Save"]')
		self.btnComfirm=(By.XPATH,"//*[text()='确认' or text()='Confirm']/../..")

	#第一步
	def clickBankAdd(self):
		# __addBankDic={0:'港币',1:'人民币',2:'美元'}
		logging.info(f'新增 结算银行卡')
		self.driver.execute_script(f'document.getElementsByClassName("{self.btnBankAdd[1]}")[0].scrollIntoView();')
		self.findElement(self.btnBankAdd).click()

	def clickBankEdit(self):
		# __addBankDic={0:'港币',1:'人民币',2:'美元'}
		logging.info(f'点击修改 结算银行卡')
		self.findElement(self.btnBankEdit,until='located').click()

	def clickBankDelete(self):
		# __addBankDic={0:'港币',1:'人民币',2:'美元'}
		logging.info(f'点击删除 结算银行卡')
		self.findElement(self.btnBankDelete,until='located').click()

	#第二步
	def clickChooseBank(self):
		logging.info(f'点击选择收款银行')
		self.findElements(self.btnChooseBank)[1].click()
		time.sleep(0.5)

	def clickBankName(self):
		logging.info(f'随机选择一个收款银行')
		ele=self.findElement(self.btnBankName,until='located')
		text=ele.text.split()[0]
		ele.click()
		time.sleep(0.5)
		return text

	def clickKeyboard2(self):
		logging.info('点击唤起银行卡号键盘')
		self.findElement(self.keyboard).click()

	def clickaccType(self):
		logging.info('点击选择账户类型')
		self.findElement(self.accType).click()

	def chooseAcc(self,n=0):
		__addBankDic={0:'港币',1:'人民币',2:'美元'}
		logging.info(f'点击选择 {__addBankDic[n]} 账户')
		_xpath={
			0:self.accHKD,
			1:self.accCNY,
			2:self.accUSD,
		}
		self.findElement(_xpath[n]).click()

	def clickSubmit(self):
		logging.info('点击保存')
		self.findElement(self.submit).click()

	def successFlag(self,bankCode):
		return 1 if self.isEleExists((By.XPATH,f"//*[contains(text(),'{bankCode}')]")) else 0

	def getCardNum(self):
		return len(self.findElements(self.btnBankEdit,until='located'))

	def clickComfirm(self):
		logging.info(f'点击 确认')
		self.findElement(self.btnComfirm).click()

