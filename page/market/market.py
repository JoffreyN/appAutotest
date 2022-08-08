import logging,time
from selenium.webdriver.common.by import By
try:
	from appium.webdriver.common.appiumby import AppiumBy
except:
	AppiumBy=By
from page.base import PageBase
from common.tools import swipRight
from business.others import reOpenApp

class PageMarket(PageBase):
	def __init__(self,driver):
		# 行情 页面
		super().__init__(driver)
		self.btnSearch={
			'Android':(By.ID,"com.cmbi.zytx:id/home_search_bar"),
			'iOS':(AppiumBy.IOS_PREDICATE,'name=="股票/基金" or name=="nav search"')
		}
		self.editSearch={
			'Android':(By.ID,"com.cmbi.zytx:id/edit_search"),
			'iOS':(AppiumBy.IOS_PREDICATE,'type=="XCUIElementTypeTextField"')
		}
		self.searchResult={
			'Android':(By.XPATH,'type'),
			'iOS':(AppiumBy.IOS_PREDICATE,'type=="XCUIElementTypeCell"')
		}
		self.searchResult_code={
			'Android':(By.ID,'com.cmbi.zytx:id/stock_code'),
			'iOS':(By.XPATH,'//XCUIElementTypeCell/XCUIElementTypeStaticText[2]')
		}
		self.searchResult_name={
			'Android':(By.ID,'com.cmbi.zytx:id/stock_name'),
			'iOS':(By.XPATH,'//XCUIElementTypeCell/XCUIElementTypeStaticText[1]')
		}
		self.btnCollect={
			'Android':(By.ID,"com.cmbi.zytx:id/com.cmbi.zytx:id/optional_checkbox"),
			'iOS':(AppiumBy.IOS_PREDICATE,'name=="addOptional" or name=="addedOptional"')
		}
		self.eleStockName={
			'Android':(By.ID,"com.cmbi.zytx:id/text_stock_name"),
			'iOS':(By.XPATH,'//XCUIElementTypeCell/XCUIElementTypeStaticText[1]')
		}
		self.cancel={
			'Android':(By.ID,'com.cmbi.zytx:id/text_cancel'),
			'iOS':(AppiumBy.IOS_PREDICATE,'name=="取消" or name contains "Cancel"')
		}

		# self.btnStockEdit={
		# 	'Android':(By.ID,"com.cmbi.zytx:id/stock_edit_btn"),
		# 	'iOS':(By.XPATH,'(//XCUIElementTypeButton[@name="排序"])[1]') 
		# }
		# self.btnSelectAll={
		# 	'Android':(By.ID,"com.cmbi.zytx:id/btn_select_all"),
		# 	'iOS':(AppiumBy.IOS_PREDICATE,'name=="全选"')
		# }
		# self.btnDelete={
		# 	'Android':(By.ID,"com.cmbi.zytx:id/btn_delete"),
		# 	'iOS':(AppiumBy.IOS_PREDICATE,'name=="删除"')
		# }
		# self.btnDone={
		# 	'Android':(By.ID,"com.cmbi.zytx:id/btn_done"),
		# 	'iOS':(AppiumBy.IOS_PREDICATE,'name=="完成"')
		# }

		self.btnTabMY={
			'Android':(By.XPATH,"//*[@text='自选' or @text='Watchlists']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='自选' or name=='Watchlists'")
		}
		self.btnMarket={
			'Android':(By.XPATH,"//*[@text='市场'or @text='Markets']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='市场' or name=='Markets'")
		}
		self.btnTabHK={
			'Android':(By.XPATH,"//*[@text='港股' or @text='HK']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='港股' or name=='HK'")
		}
		self.btnTabUS={
			'Android':(By.XPATH,"//*[@text='美股' or @text='US']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='美股' or name=='US'")
		}
		self.btnTabSHHK={
			'Android':(By.XPATH,"//*[@text='沪深港通' or @text='CN']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='沪深港通' or name=='CN'")
		}
		# self.btnTabSHSZ={
		# 	'Android':(By.XPATH,"//*[@text='沪深']"),
		# 	'iOS':(AppiumBy.IOS_PREDICATE,"name=='沪深'")
		# }

		self.btnStock2={
			'Android':(By.XPATH,"//*[@resource-id='com.cmbi.zytx:id/stock_listview']/android.widget.RelativeLayout[1]"),
			'iOS':(By.XPATH,"//*[contains(@name,'热门分类') or contains(@name,'Heat Stocks')]/following-sibling::XCUIElementTypeCell[1]")
		}#涨幅榜第1只
		
		self.btnStock2AH={
			'Android':(By.XPATH,"//*[@resource-id='com.cmbi.zytx:id/rl_transaction']/android.widget.RelativeLayout[2]"),
			'iOS':(By.XPATH,"//*[contains(@name,'十大成交榜') or contains(@name,'Capital Use Ranking')]/../following-sibling::XCUIElementTypeCell[2]")
			}

		self.tengxun={
			'Android':(By.XPATH,"//*[contains(@text,'00700')]"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name contains '00700'")
		}

	def clickTengxun(self):
		logging.info('点击 自选股 腾讯00700')
		self.findElement(self.tengxun[self.PFN]).click()

	def clickSearch(self):
		logging.info('点击 搜索框')
		self.findElement(self.btnSearch[self.PFN]).click()

	def inputSearch(self,kword):
		logging.info(f'输入 {kword}')
		self.findElement(self.editSearch[self.PFN]).send_keys(kword)

	def clickSearchResult(self):
		logging.info('点击 第一条搜索结果')
		self.findElement(self.searchResult[self.PFN]).click()

	def textExists(self,textList):
		for i in range(3):
			try:
				result_codes=' '.join(map(lambda ele:ele.text,self.findElements(self.searchResult_code[self.PFN],until='located')))
				result_names=' '.join(map(lambda ele:ele.text,self.findElements(self.searchResult_name[self.PFN],until='located')))
				break
			except TypeError:
				continue
		results=result_codes+result_names
		for text in textList:
			if text in results:
				flag=1
			else:
				logging.info(f'预期结果 {text} 不存在于搜索结果 {results} 中')
				return 0
		return flag

	def clickCollect(self):
		logging.info('点击 添加自选')
		time.sleep(3)
		# self.clickByRightXY((1360,560))
		self.findElement(self.btnCollect[self.PFN]).click()

	def clickCancel(self):
		logging.info('点击 取消')
		self.findElement(self.cancel[self.PFN]).click()

	def textStockName(self):
		return self.findElement(self.eleStockName[self.PFN]).text

	# def clickStockOne(self):
	# 	logging.info('点击 进入个股详情')
	# 	self.findElement(self.eleStockOne).click()

	# def clickStockEdit(self):
	# 	logging.info('点击 编辑自选')
	# 	ele=self.findElement(self.btnStockEdit[self.PFN],until='located')
	# 	x,y=ele.location.values()
	# 	h,w=ele.size.values()
	# 	self.driver.tap([(int(x+w/2),int(y+h/2))])

	# def clickSelectAll(self):
	# 	logging.info('点击 全选')
	# 	for i in range(5):
	# 		try:
	# 			self.findElement(self.btnSelectAll[self.PFN]).click()
	# 		except AttributeError:
	# 			if i==4:
	# 				reOpenApp(self.driver)
	# 				raise AttributeError('点击编辑自选无反应')
	# 			self.clickStockEdit()

	# def clickDelete(self):
	# 	logging.info('点击 删除')
	# 	self.findElement(self.btnDelete[self.PFN]).click()

	# def clickDone(self):
	# 	logging.info('点击 完成')
	# 	self.findElement(self.btnDone[self.PFN]).click()

	def clickTabMY(self):
		logging.info('点击 自选Tab')
		self.findElement(self.btnTabMY[self.PFN]).click()

	def clickMarket(self):
		logging.info('点击 市场')
		for i in range(3):
			try:
				self.findElement(self.btnMarket[self.PFN]).click()
				break
			except AttributeError:
				if i==2:raise AttributeError
				else:self.goBack()

	def clickTabHK(self):
		logging.info('点击 港股Tab')
		for i in range(5):
			try:
				self.findElement(self.btnTabHK[self.PFN]).click()
				return
			except AttributeError:
				swipRight(self.driver)


	def clickTabUS(self):
		logging.info('点击 美股Tab')
		for i in range(5):
			try:
				self.findElement(self.btnTabUS[self.PFN]).click()
				return
			except AttributeError:
				self.goBack()

	def clickTabSHHK(self):
		logging.info('点击 沪港通Tab')
		for i in range(5):
			try:
				self.findElement(self.btnTabSHHK[self.PFN]).click()
				return
			except AttributeError:
				self.goBack()
	
	def clickTabSHSZ(self):
		logging.info('点击 沪深Tab')
		for i in range(5):
			try:
				self.findElement(self.btnTabSHHK[self.PFN]).click()
				return
			except AttributeError:
				self.goBack()

	def clickStock2(self,t=0): # //*[contains(@name,'涨幅排行')]/following-sibling::XCUIElementTypeOther[1]
		logging.info('点击 涨幅榜第1只')
		if t=='AH':
			# self.findElement(self.btnStock2AH[self.PFN]).click()
			size=self.driver.get_window_size()
			w=size['width'];h=size['height']
			self.driver.tap([(int(w/2),int(h/2))])
		else:
			self.findElement(self.btnStock2[self.PFN],until='located').click()