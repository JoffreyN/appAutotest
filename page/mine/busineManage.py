import logging,time
from selenium.webdriver.common.by import By
try:
	from appium.webdriver.common.appiumby import AppiumBy
except:
	AppiumBy=By
from page.base import PageBase
from common.tools import switch_execute,scrollByXpath
from common.seleniumError import SCEWDE

class PageBusineManage(PageBase):
	def __init__(self,driver):
		# '业务办理' 页面
		super().__init__(driver)
		self.btnReload={
			'Android':(By.ID,'com.cmbi.zytx:id/reload_btn'),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='reload'")
		}
		self.tab_01=(By.XPATH,'//*[@alt="股票交易"]')
		self.tab_02=(By.XPATH,'//*[@alt="当前委托" or @alt="Order Query"]')
		self.tab_03=(By.XPATH,'//*[@alt="股票持仓"]')
		self.tab_04=(By.XPATH,'//*[@alt="港股ETF"]')
		self.tab_05=(By.XPATH,'//*[@alt="可融股票"]')
		self.tab_06=(By.XPATH,'//*[@alt="轮证中心"]')
		self.tab_07=(By.XPATH,'//*[@alt="我的行情"]')

		self.tab_08=(By.XPATH,'//*[@alt="新股认购" or @alt="IPOs"]')
		self.tab_09=(By.XPATH,'//*[@alt="新股订单"]')
		self.tab_10=(By.XPATH,'//*[@alt="上市申请"]')
		self.tab_11=(By.XPATH,'//*[@alt="新股日历"]')
		self.tab_12=(By.XPATH,'//*[@alt="打新计算器"]')

		self.tab_13=(By.XPATH,'//*[@alt="基金订单"]')
		self.tab_14=(By.XPATH,'//*[@alt="基金持仓"]')
		self.tab_15=(By.XPATH,'//*[@alt="基金市场"]')
		self.tab_16=(By.XPATH,'//*[@alt="货币基金"]')
		self.tab_17=(By.XPATH,'//*[@alt="债券基金"]')
		self.tab_18=(By.XPATH,'//*[@alt="股票基金"]')
		self.tab_19=(By.XPATH,'//*[@alt="配置基金"]')
		self.tab_20=(By.XPATH,'//*[@alt="基金筛选"]')
		self.tab_21=(By.XPATH,'//*[@alt="基金公司"]')

		self.tab_22=(By.XPATH,'//*[@alt="资金存入" or @alt="Deposit"]')
		self.tab_23=(By.XPATH,'//*[@alt="资金提取" or @alt="Withdraw"]')
		self.tab_24=(By.XPATH,'//*[@alt="货币兑换"]')
		self.tab_25=(By.XPATH,'//*[@alt="资金调拨"]')
		self.tab_26=(By.XPATH,'//*[@alt="资金记录" or @alt="Fund History"]')
		self.tab_27=(By.XPATH,'//*[@alt="融资申请"]')

		self.tab_28=(By.XPATH,'//*[@alt="开户专区"]')
		self.tab_29=(By.XPATH,'//*[@alt="专业投资者"]')
		self.tab_30=(By.XPATH,'//*[@alt="港美开户"]')
		self.tab_31=(By.XPATH,'//*[@alt="期货开户"]')
		self.tab_32=(By.XPATH,'//*[@alt="公司开户"]')
		self.tab_33=(By.XPATH,'//*[@alt="股权激励"]')
		self.tab_34=(By.XPATH,'//*[@alt="资产总览"]')
		self.tab_35=(By.XPATH,'//*[@alt="结单查询" or @alt="Statement"]')
		self.tab_36=(By.XPATH,'//*[@alt="开通市场"]')
		self.tab_37=(By.XPATH,'//*[@alt="银行卡管理" or contains(@alt,"Bank Account")]')
		self.tab_38=(By.XPATH,'//*[@alt="修改资料" or @alt="Personal Information"]')
		self.tab_39=(By.XPATH,'//*[@alt="风险测评" or @alt="RPQ"]')
		self.tab_40=(By.XPATH,'//*[@alt="衍生品问卷"]')
		self.tab_41=(By.XPATH,'//*[@alt="资料年审" or @alt="Annual Review"]')
		self.tab_42=(By.XPATH,'//*[@alt="W8表格"]')
		self.tab_43=(By.XPATH,'//*[@alt="CRS登记" or @alt="CRS Form"]')
		self.tab_44=(By.XPATH,'//*[@alt="公司行动"]')

		self.tab_45=(By.XPATH,'//*[@alt="壹隆小课堂"]')
		self.tab_46=(By.XPATH,'//*[@alt="我的路演"]')
		self.tab_47=(By.XPATH,'//*[@alt="路演中心"]')
		self.tab_48=(By.XPATH,'//*[@alt="IPO路演"]')
		self.tab_49=(By.XPATH,'//*[@alt="业绩路演"]')
		self.tab_50=(By.XPATH,'//*[@alt="机构活动"]')
		self.tab_51=(By.XPATH,'//*[@alt="大咖专栏"]')
		self.tab_52=(By.XPATH,'//*[@alt="金融公司"]')
		self.tab_53=(By.XPATH,'//*[@alt="科技公司"]')
		self.tab_54=(By.XPATH,'//*[@alt="生物制药"]')
		self.tab_55=(By.XPATH,'//*[@alt="热门媒体"]')
		self.tab_56=(By.XPATH,'//*[@alt="汽车能源"]')

		self.tab_57=(By.XPATH,'//*[@alt="活动中心"]')
		self.tab_58=(By.XPATH,'//*[@alt="权益中心"]')
		self.tab_59=(By.XPATH,'//*[@alt="模拟炒股" or @alt="Paper Trading"]')

		self.tab_60=(By.XPATH,'//*[@alt="通知设置" or @alt="Notification Settings"]')
		self.tab_61=(By.XPATH,'//*[@alt="有效时长"]')
		self.tab_62=(By.XPATH,'//*[@alt="密码管理"]')
		self.tab_63=(By.XPATH,'//*[@alt="股票存入" or contains(@alt,"Transfer Stock")]')
		self.tab_64=(By.XPATH,'//*[@alt="融资额度" or @alt="Margin Limit"]')
		self.xpathDict={
			1: self.tab_01,2: self.tab_02,3: self.tab_03,4: self.tab_04,5: self.tab_05,6: self.tab_06,
			7: self.tab_07,8: self.tab_08,9: self.tab_09,10:self.tab_10,11:self.tab_11,12:self.tab_12,
			13:self.tab_13,14:self.tab_14,15:self.tab_15,16:self.tab_16,17:self.tab_17,18:self.tab_18,
			19:self.tab_19,20:self.tab_20,21:self.tab_21,22:self.tab_22,23:self.tab_23,24:self.tab_24,
			25:self.tab_25,26:self.tab_26,27:self.tab_27,28:self.tab_28,29:self.tab_29,30:self.tab_30,
			31:self.tab_31,32:self.tab_32,33:self.tab_33,34:self.tab_34,35:self.tab_35,36:self.tab_36,
			37:self.tab_37,38:self.tab_38,39:self.tab_39,40:self.tab_40,41:self.tab_41,42:self.tab_42,
			43:self.tab_43,44:self.tab_44,45:self.tab_45,46:self.tab_46,47:self.tab_47,48:self.tab_48,
			49:self.tab_49,50:self.tab_50,51:self.tab_51,52:self.tab_52,53:self.tab_53,54:self.tab_54,
			55:self.tab_55,56:self.tab_56,57:self.tab_57,58:self.tab_58,59:self.tab_59,60:self.tab_60,
			61:self.tab_61,62:self.tab_62,63:self.tab_63,64:self.tab_64
		}

		self.passwordInput={
			'Android':(By.ID,"com.cmbi.zytx:id/input_trade_password"),
			'iOS':(AppiumBy.IOS_PREDICATE,'type=="XCUIElementTypeSecureTextField"')
		}
		self.confirm={
			'Android':(By.ID,"com.cmbi.zytx:id/btn_submit"),
			'iOS':(AppiumBy.IOS_PREDICATE,'name=="确定" or name=="Confirm"')
		}

	def cilckCommon_more(self,num):
		num=int(num)
		desc=self.xpathDict[num][1].split('"')[1]
		logging.info(f'点击 {desc}')
		scrollByXpath(self.driver,self.xpathDict[num][1])
		self.findElement(self.xpathDict[num]).click()

	@switch_execute
	def inputPwordIFneeded(self):
		try:
			self.findElement(self.passwordInput[self.PFN],timeout=3,screen=0).send_keys('aaaa1111')
			self.findElement(self.confirm[self.PFN],timeout=3,screen=0).click()
		except:
			pass

	# @switch_execute
	def clickReload(self):
		#业务办理页面加载极慢 经常白屏，故出此下策
		# self.inputPwordIFneeded()
		logging.info('点击 reload')
		self.findElement(self.btnReload[self.PFN]).click()
		time.sleep(5)
