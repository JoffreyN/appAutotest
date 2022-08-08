import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase
from common.tools import switch_execute

class PageCurrExchange(PageBase):
	def __init__(self,driver):
		# 货币兑换
		super().__init__(driver)
		# self.eleOrders=(By.XPATH,"//*[text()='兑换记录']")#兑换记录
		# self.curName=(By.CLASS_NAME,'currency-type-text')#0 左边币种名称;1 右边币种名称
		# self.curSwitch=(By.CLASS_NAME,'direction')#0 左;1 右 币种切换按钮
		# self.curList=(By.CLASS_NAME,'currency-list')#0 左;1 右 币种下拉选项
		# self.curListRMB=(By.XPATH,"//*[text()='人民币']")#币种下拉人民币选项
		# self.curListUSD=(By.XPATH,"//*[text()='美元']")
		self.amount_input=(By.ID,'myKeyboardNodot')#金额输入，点击出现键盘
		self.submit=(By.ID,"subimitApply")
		# self.help=(By.XPATH,"//*[text()='业务说明']")#
		# self.helpFlag=(By.XPATH,"//*[text()='货币兑换常见问题']")#
		self.confirm=(By.CSS_SELECTOR,".van-dialog__confirm")
		self.successFlag=(By.XPATH,"//*[contains(text(),'委托成功')]")#
		self.done=(By.XPATH,"//*[text()='完成']")#
		# self.allStatus=(By.XPATH,"//*[@class='record-page']//div[@class='direction']")
		# self.todo=(By.XPATH,'//li[text()="待处理"]')#
		# self.doing=(By.XPATH,'//li[text()="处理中"]')#
		# self.success=(By.XPATH,'//li[text()="兑换成功"]')#
		# self.fail=(By.XPATH,'//li[text()="兑换失败"]')#
		# self.canceled=(By.XPATH,'//li[text()="已撤单"]')#
		# self.order1=(By.XPATH,'//*[@id="goodWrapper"]//div[5]//span[1]')#第1条兑换记录
		# self.noTradeFlag=(By.XPATH,"//*[contains(text(),'非交易时段')]")#
		# self.iKnow=(By.XPATH,"//*[text()='知道了']/..")#
		# self.cancel=(By.XPATH,"//*[text()='撤单']")#

		#New
		self.btn_change={
			'out':(By.XPATH,"//*[@class='btn_change']/div[1]"),
			'in':(By.XPATH,"//*[@class='btn_change']/div[2]")
		}
		self.currency_type=(By.CLASS_NAME,'currency-type-inner')

	def clickAlert_confirm(self):
		try:
			self.findElement(self.confirm,screen=False,timeout=1).click()
			logging.info('点击了弹窗 确定')
		except AttributeError:
			pass

	def clickChangeCurr(self,in_out='in'):
		in_out_msg={'in':'兑入','out':'兑出'}
		logging.info(f'点击 {in_out_msg[in_out]}金额')
		self.findElement(self.btn_change[in_out]).click()

	def chooseCurr(self,curr_L='港币',curr_R='美元'):
		# curr: 港币、美元、人民币
		L_R_msg={'L':'左边','R':'右边'}
		logging.info(f'点击选择货币: {curr_L} --> {curr_R}')
		ele_L,ele_R=self.findElements(self.currency_type)
		ele_L.click()
		time.sleep(0.5)
		self.findElement((By.XPATH,f"//ul[@class='currency-list']/li[text()='{curr_L}']")).click()
		time.sleep(0.5)
		
		ele_R.click()
		time.sleep(0.5)
		self.findElements((By.XPATH,f"//ul[@class='currency-list']/li[text()='{curr_R}']"),until='located')[-1].click()

	def inputAmount(self,amount):
		logging.info(f'输入金额 {amount}')
		self.findElement(self.amount_input).click()
		keybordDic={'1':0,'2':1,'3':2,'4':3,'5':4,'6':5,'7':6,'8':7,'9':8,'.':9,'0':10,}
		for i in str(amount):
			js=f'document.getElementsByClassName("keyboard-number-list")[0].getElementsByClassName("keyboard-number-item")[{keybordDic[i]}].click();'
			time.sleep(0.5)
			self.driver.execute_script(js)

	def getAmount(self):
		return self.findElement(self.amount_input).text

	def clickkbConfirm(self):
		logging.info('点击 确定键')
		self.driver.execute_script('document.getElementsByClassName("keyboard-operate-list")[0].querySelector(".confirm").click();')

	def clicksubmit(self):
		logging.info('点击 提交')
		self.findElement(self.submit).click()

	# def clickhelp(self):
	# 	logging.info('点击 参考说明')
	# 	self.findElement(self.help).click()

	# def gethelpFlag(self):
	# 	return 1 if self.findElement(self.helpFlag,until='located') else 0

	def clickconfirm(self,js=0):
		logging.info('点击 确认')
		if js:
			self.driver.execute_script(f'document.querySelector("{self.confirm[1]}").click();')
		else:
			self.findElements(self.confirm,until='located')[-1].click()

	def getsuccessFlag(self):
		return self.isEleExists(self.successFlag)

	def clickdone(self):
		logging.info('点击 完成')
		self.findElement(self.done).click()

	# def clickallStatus(self):
	# 	logging.info('点击 全部状态')
	# 	time.sleep(3)
	# 	self.clickByScript(self.findElement(self.allStatus))

	# def clicktodo(self):
	# 	logging.info('点击 待处理')
	# 	self.findElement(self.todo).click()

	# def clickdoing(self):
	# 	logging.info('点击 处理中')
	# 	self.findElement(self.doing).click()

	# def clicksuccess(self):
	# 	logging.info('点击 兑换成功')
	# 	self.findElement(self.success).click()

	# def clickfail(self):
	# 	logging.info('点击 兑换失败')
	# 	self.findElement(self.fail).click()

	# def clickcanceled(self):
	# 	logging.info('点击 已撤单')
	# 	self.findElement(self.canceled).click()

	# def flagorder1(self):
	# 	return self.findElement(self.order1,until='located').text