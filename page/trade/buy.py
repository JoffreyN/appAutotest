import logging,time
from page.base import PageBase
from selenium.webdriver.common.by import By
try:
	from appium.webdriver.common.appiumby import AppiumBy
except:
	AppiumBy=By
from common.tools import myAddScreen,switch_execute,scrollByXpath,pressKeyboard

class PageBuy(PageBase):
	def __init__(self,driver):
		# '新版买入' 页面
		super().__init__(driver)
		self.tradeBuy=(By.CSS_SELECTOR,'.btn.buy')
		self.input=(By.TAG_NAME,'input')
		self.eleStockOne=(By.CSS_SELECTOR,'.item.van-hairline--top')
		self.eleBuyPrices=(By.XPATH,"//*[@class='control-range-buy']/div[1]/span[1]")#买1
		self.eleBuyPrices2=(By.XPATH,"//*[@class='control-range-buy']/div[2]/span[1]")#买2
		self.eleBuyPrices3=(By.XPATH,"//*[@class='control-range-buy']/div[3]/span[1]")#买3
		self.eleBuyPrices4=(By.XPATH,"//*[@class='control-range-buy']/div[4]/span[1]")#买4
		self.eleBuyPrices5=(By.XPATH,"//*[@class='control-range-buy']/div[5]/span[1]")#买5

		self.eleSellPrices=(By.XPATH,"//*[@class='control-range-sell']/div[1]/span[1]")#卖1
		self.eleSellPrices2=(By.XPATH,"//*[@class='control-range-sell']/div[2]/span[1]")#卖2
		self.eleSellPrices3=(By.XPATH,"//*[@class='control-range-sell']/div[3]/span[1]")#卖3
		self.eleSellPrices4=(By.XPATH,"//*[@class='control-range-sell']/div[4]/span[1]")#卖4
		self.eleSellPrices5=(By.XPATH,"//*[@class='control-range-sell']/div[5]/span[1]")#卖5
		# self.elePriceMinus={
		# 	'Android':(By.XPATH,"//*[@class='control-input']/div[1]/div[2]"),
		# 	'iOS':(AppiumBy.IOS_PREDICATE,"name=='价格'")
		# }#价格减 按钮
		self.input_price={
			'Android':(By.XPATH,'//*[@resource-id="app"]/android.view.View[2]/android.view.View[3]//android.widget.EditText[1]'),
			'iOS':(By.XPATH,'//*[@name="股票交易"]/XCUIElementTypeOther[10]/XCUIElementTypeTextField')
		}# 价格输入框
		self.input_Done_iOS=(By.XPATH,'//XCUIElementTypeButton[@name="完成"]')

		self.btnBuy=(By.CSS_SELECTOR,'.precast-btn.buy')
		self.buyNum=(By.CSS_SELECTOR,'.buy-num')
		
		# self.eleResultStockCode=(By.XPATH,"//*[@class='hold-content']/div[1]/div[2]/div[1]/span[5]")#当前委托第一条里的股票代码

		self.editPwd={
			'Android':(By.XPATH,'//*[contains(@text,"密码") or contains(@text,"password")]'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name contains '密码' or name contains 'password'")
		}
		self.btnClose={
			'Android':(By.ID,'com.cmbi.zytx:id/btn_close'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='关闭 s'")
		}

		# 新版交易页面
		self.input_new={
			'Android':(By.CLASS_NAME,'search-text'),# webview
			'iOS':(By.XPATH,"//*[contains(@name,'请输入股票代码') or contains(@name,'name to search')]")# ios 点击无反应，需要切换至原生
		}
		self.eleBuyPrices_new=(By.XPATH,"//*[@class='control-range-buy']/div[1]")#买1
		self.eleSellPrices_new=(By.XPATH,"//*[@class='control-range-sell']/div[1]")#卖1
		self.eleResultStockCode_new=(By.XPATH,'//*[@class="order-box"]/div[1]//div[@class="item-name"]//span')#当前委托第一条里的股票代码
		self.eleNumOne={
			'Android':(By.XPATH,"//*[text()='1手' or text()='1Lot']"),
			'iOS':(By.XPATH,"//*[@name='1手' or @name='1Lot']")
		}
		self.orderType=(By.CLASS_NAME,'control-info-type')

		self.btnPan={# 点击切换单
			'Android':(By.XPATH,'//*[@resource-id="app"]/android.view.View[2]/android.view.View[2]/android.view.View[2]/android.view.View[2]'),
			'iOS':(By.XPATH,'//*[@name="股票交易"]/XCUIElementTypeOther[9]/XCUIElementTypeOther[2]')
		}
		self.panName1={# 增强限价单
			'Android':(By.XPATH,'//*[@resource-id="app"]/android.view.View[4]/android.view.View[2]'),
			'iOS':(By.XPATH,'//*[@name="股票交易"]/XCUIElementTypeOther[32]')
		
		}
		self.panName2={# 限价单
			'Android':(By.XPATH,'//*[@resource-id="app"]/android.view.View[4]/android.view.View[3]'),
			'iOS':(By.XPATH,'//*[@name="股票交易"]/XCUIElementTypeOther[33]')
		
		}
		self.panName3={# 特殊限价单
			'Android':(By.XPATH,'//*[@resource-id="app"]/android.view.View[4]/android.view.View[4]'),
			'iOS':(By.XPATH,'//*[@name="股票交易"]/XCUIElementTypeOther[34]')
		
		}
		self.panName4={# 竞价限价单
			'Android':(By.XPATH,'//*[@resource-id="app"]/android.view.View[4]/android.view.View[5]'),
			'iOS':(By.XPATH,'//*[@name="股票交易"]/XCUIElementTypeOther[35]')
		
		}
		self.panName5={# 竞价单
			'Android':(By.XPATH,'//*[@resource-id="app"]/android.view.View[4]/android.view.View[6]'),
			'iOS':(By.XPATH,'//*[@name="股票交易"]/XCUIElementTypeOther[36]')
		
		}

		self.price=(By.CSS_SELECTOR,'.product-price') #最上方现价
		self.increase=(By.XPATH,"//*[contains(@class,'product-price')]/following-sibling::span[1]")#最上方涨跌幅
		self.refreshIcon=(By.CLASS_NAME,'refresh-icon')
		self.eleFlag1=(By.XPATH,'//p[contains(text(),"不支持")]')# 当前时间不支持竞价单下单
		self.stockName=(By.CLASS_NAME,'search-text')

	def getstockName(self):
		return self.findElement(self.stockName).text.strip()

	def flag1Exists(self):
		return self.isEleExists(self.eleFlag1)

	@switch_execute
	def changePan(self,panName):
		logging.info(f'点击打开单菜单')
		self.findElement(self.btnPan[self.PFN],until='located').click()

		xpathDict={
			'增强限价单':self.panName1,
			'限价单':self.panName2,
			'特殊限价单':self.panName3,
			'竞价限价单':self.panName4,
			'竞价单':self.panName5,
		}
		logging.info(f'点击选择 {panName}')
		self.findElement(xpathDict[panName][self.PFN]).click()

	def buy_sell_price_exists(self,bs,n):
		bs_dict={'b':'买','s':'卖'}
		bs_ele_dict={
			'b':{
				1:self.eleBuyPrices,
				2:self.eleBuyPrices2,
				3:self.eleBuyPrices3,
				4:self.eleBuyPrices4,
				5:self.eleBuyPrices5,
			},
			's':{
				1:self.eleSellPrices,
				2:self.eleSellPrices2,
				3:self.eleSellPrices3,
				4:self.eleSellPrices4,
				5:self.eleSellPrices5,
			}
		}
		logging.info(f'判断{bs_dict[bs]}{n}是否存在')
		return self.isEleExists(bs_ele_dict[bs][n])

	def refreshIcon_exists(self):
		return self.isEleExists(self.refreshIcon)
		
	def getprice(self):
		try:
			price=float(self.findElement(self.price).text.strip())
		except ValueError:
			price=None
		logging.info(f'现价: {price}')
		return price

	@switch_execute
	def inputPrice(self,price):
		logging.info(f'输入价格 {price}')
		if self.PFN=='Android':
			ele=self.findElement(self.input_price[self.PFN])
			ele.send_keys('')
			ele.click()
			pressKeyboard(self.driver,str(price))
		else:
			ele=self.findElement(self.input_price[self.PFN])
			ele.clear()
			ele.send_keys(str(price))
			self.findElement(self.input_Done_iOS).click()


	def getincrease(self):
		try:
			increase=float(self.findElement(self.increase).text.strip().replace('%',''))
		except ValueError:
			increase=None
		logging.info(f'涨跌幅: {increase}%')
		return increase

	def getorderType(self):
		return self.findElement(self.orderType).text.strip()

	def getMaxBuyNum(self):
		text=self.findElement(self.buyNum).text.replace(',','').strip()
		logging.info(f'最大可买为: {text}')
		return float(text)


	def flagExists(self):
		return self.isEleExists(self.btnBuy)

	def clickTradeBuy(self):
		logging.info('点击 买')
		self.findElement(self.tradeBuy).click()

	@switch_execute
	def clickInput_ios(self):
		self.findElement(self.input_new[self.PFN]).click()

	def clickInput(self):
		logging.info('点击输入框')
		if self.PFN=='Android':
			self.myTap(self.findElement(self.input_new[self.PFN]))
		else:
			self.clickInput_ios()

	def inputStock(self,stockCode):
		logging.info(f'输入股票代码 {stockCode}')
		self.findElement(self.input).send_keys(stockCode)

	def clickStockOne(self,stockCode):
		logging.info('点击 出现的股票列表中的第一个')
		self.findElement(self.eleStockOne).click()

	def clickBuyPriceOne(self):
		logging.info('点击 买1价')
		self.findElement(self.eleBuyPrices_new).click()

	# def clickSellPriceOne(self):
	# 	logging.info('点击 卖1价')
	# 	self.findElement(self.eleSellPrices).click()

	def buyPriceOneExists(self):
		try:
			scrollByXpath(self.driver,self.eleBuyPrices[1])
			price=float(self.findElement(self.eleBuyPrices,until='located').text.split()[-1])
			logging.info(f'买一档价格: {price}')
			# myAddScreen(self,f'买一档价格: {price}')
			return 1
		except ValueError:
			return 0

	def sellPriceOneExists(self):
		try:
			scrollByXpath(self.driver,self.eleSellPrices[1])
			price=float(self.findElement(self.eleSellPrices,until='located').text.split()[-1])
			logging.info(f'卖一档价格: {price}')
			# myAddScreen(self,f'卖一档价格: {price}')
			return 1
		except ValueError:
			return 0

	def inputNum(self,n=2):
		# if appVersion>'3.0.4.0000':
		pass
		# else:
		# 	logging.info(f'输入数量 {n}')
		# 	ele=self.findElements(self.input,until='located')[-1]
		# 	ele.clear()
		# 	ele.send_keys(n)

	# def inputPrice(self,amount):
	# 	logging.info(f'输入价格 {amount}')
	# 	ele=self.findElements(self.input,until='located')[1]
	# 	ele.clear()
	# 	ele.send_keys(str(amount))

	@switch_execute
	def clickNumOne_ios(self):
		self.findElement(self.eleNumOne[self.PFN]).click()

	def clickNumOne(self):
		logging.info('点击 1手')
		if self.PFN=='Android':
			self.myTap(self.findElement(self.eleNumOne[self.PFN]))
		else:
			self.clickNumOne_ios()

	# def clickPriceMinus(self):
	# 	logging.info('点击 价格减 按钮 5 次')
	# 	if self.PFN=='Android':
	# 		ele=self.findElement(self.elePriceMinus[self.PFN])
	# 		for i in range(5):
	# 			self.myTap(ele)
	# 	elif self.PFN=='iOS':
	# 		context=self.driver.current_context
	# 		self.driver.switch_to.context(self.driver.contexts[0])

	# 		rect=eval(self.findElement(self.elePriceMinus[self.PFN]).get_attribute('rect'))
	# 		x=int(rect['x']+rect['width']+26)
	# 		y=int(rect['y']+rect['height']/2)
	# 		for i in range(5):
	# 			self.driver.tap([(x,y)])
	# 			time.sleep(0.5)
				
	# 		self.driver.switch_to.context(context)

	def clickBuy(self):
		logging.info('点击 买入')
		self.clickByScript(self.findElement(self.btnBuy,until='located'))

	def textResultStockCode(self):
		for i in range(3):
			time.sleep(3)
			try:
				scrollByXpath(self.driver,self.eleResultStockCode_new[1])
				return self.findElement(self.eleResultStockCode_new,until='located').text.strip()
			except AttributeError:
				continue
		return '获取委托列表中第一条记录失败'

	def isEditPwdExists(self):
		return self.isEleExists(self.editPwd[self.PFN])

	def clickClose(self):
		logging.info('点击 关闭')
		self.findElement(self.btnClose[self.PFN]).click()
