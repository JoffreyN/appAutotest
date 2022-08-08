import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase
from common.tools import swipeUp
from selenium.webdriver.support.select import Select
from common.seleniumError import SCEENVE,SCEENIE,SCEECIE

class PageCurrExchangeWeb(PageBase):
	def __init__(self,driver):
		# 货币兑换Boss端
		super().__init__(driver)
		self.allMoney=(By.XPATH,"//*[text()='今日兑出:']/following-sibling::span[1]")

		self.orderStatus=(By.NAME,'orderStatus')
		self.query=(By.XPATH,"//a[text()='清空']/preceding-sibling::button")#查询按钮
		self.limit=(By.CLASS_NAME,'pagination_limit')
		self.next=(By.XPATH,"//a[text()='下一页']")

		self.currencyIn=(By.NAME,'currencyIn')#汇率兑换选择左边
		self.currencyOut=(By.NAME,'currencyOut')#汇率兑换选择左边
		self.amountIn=(By.ID,'amountIn')
		self.amount=(By.ID,'amount')
		self.queryExchange=(By.CLASS_NAME,'rate-refresh2')#查询汇率按钮
		self.exchangeInfo=(By.CLASS_NAME,'exchange-rate')#
		self.updateTime=(By.CLASS_NAME,'update-time')#

		self.faPlus=(By.CLASS_NAME,'fa-plus')#新增兑汇
		self.accountId=(By.NAME,'accountId')#第1个
		self.btnModalSave=(By.CLASS_NAME,'btn-modal-save')
		self.modalCancel=(By.CLASS_NAME,'modal-cancel')
		self.firstAmountOut=(By.XPATH,"//table//td[3]")#第一条记录兑出金额
		self.firstAmountIn=(By.XPATH,"//table//td[4]")#第一条记录兑入金额
		self.firstRate=(By.XPATH,"//table//td[5]")#第一条记录汇率
		self.firstStatus=(By.XPATH,"//table//td[6]")#第一条订单状态

		self.errMsg=(By.ID,'errorMessage')#第1个
		self.unfocus1=(By.TAG_NAME,'h1')
		self.unfocus2=(By.XPATH,"//*[text()='户口号码：']")

	def loseFocus1(self):
		self.findElement(self.unfocus1,until='located').click()

	def loseFocus2(self):
		self.findElement(self.unfocus2,until='located').click()

	def getallHKD(self):
		return float(self.findElements(self.allMoney)[0].text.replace(',',''))

	def getallUSD(self):
		return float(self.findElements(self.allMoney)[1].text.replace(',',''))

	def getallRMB(self):
		return float(self.findElements(self.allMoney)[2].text.replace(',',''))

	def selectOrderStatus(self,status):
		Select(self.findElement(self.orderStatus)).select_by_visible_text(status)

	def clickquery(self):
		logging.info('点击 查询')
		self.findElement(self.query).click()

	def selectlimit(self):
		Select(self.findElement(self.limit)).select_by_visible_text("50")

	def getAllAmount(self):
		today=time.mktime(time.strptime(f'{time.strftime("%Y-%m-%d")} 09:00:00', '%Y-%m-%d %X'))
		amountsUSD=[]
		amountsHKD=[]
		amountsCNY=[]
		flag=1
		while flag:
			n=0
			for tr in self.findElements((By.TAG_NAME,'tr')):
				try:
					if today>=time.mktime(time.strptime(tr.find_elements_by_tag_name('td')[8].text,'%Y-%m-%d %X')):
						flag=0;break
					else:
						n+=1
						amount=tr.find_elements_by_tag_name('td')[2].text.replace('\n',' ').replace(',','')
						if 'USD' in amount:
							amountsUSD.append(float(amount.split()[0]))
						elif 'HKD' in amount:
							amountsHKD.append(float(amount.split()[0]))
						elif 'CNY' in amount:
							amountsCNY.append(float(amount.split()[0]))
						if n==50:
							logging.info('点击下一页')
							self.findElement(self.next).click()
							time.sleep(3)
				except IndexError:
					pass
		return {'USD':round(sum(amountsUSD),2),'HKD':round(sum(amountsHKD),2),'CNY':round(sum(amountsCNY),2)}

	def selectInCur(self,cur):
		for i in range(5):
			try:
				Select(self.findElement(self.currencyIn)).select_by_visible_text(cur)
			except (SCEENVE,SCEENIE):
				time.sleep(1)
				if i==4:raise SCEECIE(f'选择货币失败')

	def selectOutCur(self,cur):
		for i in range(5):
			try:
				Select(self.findElement(self.currencyOut)).select_by_visible_text(cur)
			except (SCEENVE,SCEENIE):
				time.sleep(1)
				if i==4:raise SCEECIE(f'选择货币失败')


	def selectInCur1(self,cur):
		for i in range(5):
			try:
				Select(self.findElements(self.currencyIn)[1]).select_by_visible_text(cur)
			except (SCEENVE,SCEENIE):
				time.sleep(1)
				if i==4:raise SCEECIE(f'选择货币失败')


	def selectOutCur1(self,cur):
		for i in range(5):
			try:
				Select(self.findElements(self.currencyOut)[1]).select_by_visible_text(cur)
			except (SCEENVE,SCEENIE):
				time.sleep(1)
				if i==4:raise SCEECIE(f'选择货币失败')


	def inputAmountIn(self,amount):
		logging.info(f'输入兑换金额 {amount}')
		self.findElement(self.amountIn).clear()
		self.findElement(self.amountIn).send_keys(amount)

	def clickqueryExchange(self):
		logging.info('点击 查询汇率')
		for i in range(5):
			try:
				self.findElement(self.queryExchange).click()
				return
			except SCEECIE:
				time.sleep(1)
				if i==4:raise SCEECIE(f'点击查询汇率失败')

	def textexchangeInfo(self):
		return self.findElement(self.exchangeInfo).text

	def textupdateTime(self):
		return self.findElement(self.updateTime).text

	def clickfaPlus(self):
		logging.info('点击 新增兑汇')
		self.findElement(self.faPlus).click()

	def inputaccountId(self,account):
		logging.info(f'输入账户号 {account}')
		self.findElement(self.accountId).clear()
		self.findElement(self.accountId).send_keys(account)

	def inputaccountId1(self,account):
		logging.info(f'输入账户号 {account}')
		for i in range(5):
			try:
				self.findElements(self.accountId,screen=False)[1].send_keys(account)
				return
			except IndexError:
				time.sleep(1)
				if i==4:raise IndexError(f'未找到第二个 {self.accountId} 元素')
			except (SCEENVE,SCEENIE):
				time.sleep(1)
				if i==4:raise IndexError(f'账户无法输入')

	def inputAmountIn1(self,amount):
		logging.info(f'输入金额 {amount}')
		for i in range(5):
			try:
				self.findElement(self.amount).clear()
				self.findElement(self.amount).send_keys(amount)
				return
			except (SCEENIE,SCEENVE):
				time.sleep(2)
				if i==4:raise SCEENIE(f'无法输入兑换金额')

	def clickbtnModalSave(self):
		logging.info('点击 保存')
		for i in range(5):
			try:
				self.findElement(self.btnModalSave).click()
				break
			except SCEECIE:
				if i==4:raise SCEECIE(f'点击保存失败')
				time.sleep(1)

	def clickmodalCancel(self):
		logging.info('点击 取消')
		self.findElement(self.modalCancel).click()

	def textfirstStatus(self):
		return self.findElement(self.firstStatus).text.strip()

	def textfirstAmountOut(self):
		return self.findElement(self.firstAmountOut).text.split()[0]

	def textfirstRate(self):
		return float(self.findElement(self.firstRate).text)

	def texterrMsg(self):
		return self.findElement(self.errMsg).text.strip()

	def getalert(self,driverWeb):
		alertext=driverWeb.switch_to.alert.text
		driverWeb.switch_to.alert.accept()
		return alertext

	def getAccMoney(self,driverWeb,account):
		import requests
		cookie=";".join([item["name"]+"="+item["value"] for item in driverWeb.get_cookies()])
		url=f'http://0.0.0.0/admin/currencyExchange/accountinfo?accountId={account}'
		head={
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
			'Cookie':cookie,
			'X-Requested-With':'XMLHttpRequest',
		}
		resp=requests.get(url,headers=head)
		moneys=resp.json()['data']['power']
		for k,v in moneys.items():
			moneys[k]=float(v.replace(',',''))
		# {'HKD': 19798097.22, 'USD': 79406.05, 'CNY': 11084614.61}
		return moneys


