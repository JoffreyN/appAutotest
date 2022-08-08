import logging,time
from selenium.webdriver.common.by import By
# from common.tools import switch_execute
from .base import PageBase

class PageFlagExists(PageBase):
	def __init__(self,driver):
		# 判断页面是否跳转成功
		super().__init__(driver)
		self.moreTab_01=(By.XPATH,"//*[contains(text(),'请输入股票代码')]")# 股票交易页面 appweb/trade
		self.moreTab_02=(By.XPATH,"//*[contains(text(),'历史订单')]")# 订单查询页面 trade/entrust
		self.moreTab_03=(By.XPATH,"//*[contains(text(),'------')]")# 股票持仓  
		self.moreTab_04=(By.XPATH,"//*[contains(text(),'发行商')]")# 港股ETF appweb/quote
		self.moreTab_05=(By.XPATH,"//*[contains(text(),'可融股票')]")# 可融股票 /quote/marginRatio
		self.moreTab_06=(By.XPATH,"//*[contains(text(),'轮证中心')]")# 轮证中心 /quote/demonstration
		self.moreTab_07=(By.XPATH,"//*[contains(text(),'我的行情')]")# 我的行情 /helperpage/market
		self.moreTab_08=(By.XPATH,"//*[contains(text(),'新股中心')]")# 新股认购 /appweb/eipo
		self.moreTab_09=(By.XPATH,"//*[contains(text(),'认购')]")# 新股订单 /eipo/orderList 多一次返回
		self.moreTab_10=(By.XPATH,"//*[contains(text(),'上市申请')]")# 上市申请 /eipo/marketList
		self.moreTab_11=(By.XPATH,"//*[contains(text(),'新股日历')]")# 新股日历 /eipo/calendar
		self.moreTab_12=(By.XPATH,"//*[contains(text(),'打新计算器')]")# 打新计算器 /eipo/ipoCounter
		self.moreTab_13=(By.XPATH,"//*[contains(text(),'基金')]")# 基金订单 /fund-sys/records
		self.moreTab_14=(By.XPATH,"//*[contains(text(),'------')]")# 基金持仓  
		self.moreTab_15=(By.XPATH,"//*[contains(text(),'------')]")# 基金市场    
		self.moreTab_16=(By.XPATH,"//*[contains(text(),'货币基金')]")# 货币基金 /fund-sys/fundList
		self.moreTab_17=(By.XPATH,"//*[contains(text(),'债券基金')]")# 债券基金 /fund-sys/fundList
		self.moreTab_18=(By.XPATH,"//*[contains(text(),'股票基金')]")# 股票基金 /fund-sys/fundList
		self.moreTab_19=(By.XPATH,"//*[contains(text(),'配置基金')]")# 配置基金 /fund-sys/fundList
		self.moreTab_20=(By.XPATH,"//*[contains(text(),'基金列表')]")# 基金筛选 /fund-sys/fundList
		self.moreTab_21=(By.XPATH,"//*[contains(text(),'基金公司')]")# 基金公司 /fund-sys/fundCompany
		self.moreTab_22=(By.XPATH,"//*[contains(text(),'资金存入')]")# 资金存入 /deposit
		self.moreTab_23=(By.XPATH,"//*[contains(text(),'资金提取')]")# 资金提取 /withdraw
		self.moreTab_24=(By.XPATH,"//*[contains(text(),'兑换币种')]")# 货币兑换 /currency
		self.moreTab_25=(By.XPATH,"//*[contains(text(),'资金调拨')]")# 资金调拨 /capitalallocation
		self.moreTab_26=(By.XPATH,"//*[contains(text(),'存入资金')]")# 资金记录 /fundsHistory
		self.moreTab_27=(By.XPATH,"//*[contains(text(),'融资额度')]")# 融资申请 /settle/margin
		self.moreTab_28=(By.XPATH,"//*[contains(text(),'壹隆环球开户专区')]")# 开户专区 resource
		self.moreTab_29=(By.XPATH,"//*[contains(text(),'专业投资者认证')]")# 专业投资者 /piUpgrade
		self.moreTab_30=(By.XPATH,"//*[contains(text(),'在线开户')]")# 港美开户 /form/s_start
		self.moreTab_31=(By.XPATH,"//*[contains(text(),'在线开户')]")# 期货开户 /appkh/futures
		self.moreTab_32=(By.XPATH,"//*[contains(text(),'企业开户')]")# 公司开户 /open-propaganda
		self.moreTab_33=(By.XPATH,"//*[contains(text(),'港美股ESOP')]")# 股权激励 /esop/promotion/app
		self.moreTab_34=(By.XPATH,"//*[contains(text(),'资产总值')]")# 资产总览 /staticPortfolio
		self.moreTab_35=(By.XPATH,"//*[contains(text(),'日结单')]")# 结单查询 /checkInquire
		self.moreTab_36=(By.XPATH,"//*[contains(text(),'开通市场')]")# 开通市场 /openMarket
		self.moreTab_37=(By.XPATH,"//*[contains(text(),'结算账户')]")# 银行卡管理 /bankcard
		self.moreTab_38=(By.XPATH,"//*[contains(text(),'证件信息维护')]")# 修改资料 /profile
		self.moreTab_39=(By.XPATH,"//*[contains(text(),'投资风险')]")# 风险测评 /rpqTest
		self.moreTab_40=(By.XPATH,"//*[contains(text(),'衍生产品问卷')]")# 衍生品问卷 /derTest
		self.moreTab_41=(By.XPATH,"//*[contains(text(),'资料年审')]")# 资料年审 /client-renew
		self.moreTab_42=(By.XPATH,"//*[contains(text(),'W8表格登记')]")# W8表格 /w8Table
		self.moreTab_43=(By.XPATH,"//*[contains(text(),'个人账户登记')]")# CRS登记 /crsRegister
		self.moreTab_44=(By.XPATH,"//*[contains(text(),'征集中')]")# 公司行动 /companyMovement
		self.moreTab_45=(By.XPATH,"//*[contains(text(),'壹隆小课堂')]")# 壹隆小课堂 /detail/1219739
		self.moreTab_46=(By.XPATH,"//*[contains(text(),'我的路演')]")# 我的路演 /myroadshowCore
		self.moreTab_47=(By.XPATH,"//*[contains(text(),'路演中心')]")# 路演中心 /roadshowCore
		self.moreTab_48=(By.XPATH,"//*[contains(text(),'IPO路演')]")# IPO路演 /roadshowCore
		self.moreTab_49=(By.XPATH,"//*[contains(text(),'业绩路演')]")# 业绩路演 /roadshowCore
		self.moreTab_50=(By.XPATH,"//*[contains(text(),'机构活动')]")# 机构活动 /roadshowCore
		self.moreTab_51=(By.XPATH,"//*[contains(text(),'大咖说')]")# 大咖专栏 /roadshowCore
		self.moreTab_52=(By.XPATH,"//*[contains(text(),'金融类知名公司')]")# 金融公司 /roadshowCore
		self.moreTab_53=(By.XPATH,"//*[contains(text(),'科技类知名公司')]")# 科技公司 /roadshowCore
		self.moreTab_54=(By.XPATH,"//*[contains(text(),'生物制药')]")# 生物制药 /roadshowCore
		self.moreTab_55=(By.XPATH,"//*[contains(text(),'媒体类知名公司')]")# 热门传媒 /roadshowCore
		self.moreTab_56=(By.XPATH,"//*[contains(text(),'汽车能源类公司')]")# 汽车能源 /roadshowCore
		self.moreTab_57=(By.XPATH,"//*[contains(text(),'热门活动')]")# 活动中心 /act-center
		self.moreTab_58=(By.XPATH,"//*[contains(text(),'可用权益')]")# 权益中心 /act_award
		self.moreTab_59=(By.XPATH,"//*[contains(text(),'模拟港股交易')]")# 模拟炒股 /simulate
		self.moreTab_60=(By.XPATH,"//*[contains(text(),'邮件通知')]")# 通知设置 /emailSetting
		self.moreTab_61=(By.XPATH,"//*[contains(text(),'8小时')]")# 有效时长 /effectiveDuration
		self.moreTab_62=(By.XPATH,"//*[contains(text(),'找回密码')]")# 密码管理 /reset
		self.moreTab_xpathDict={
			'01':self.moreTab_01,'02':self.moreTab_02,'03':self.moreTab_03,'04':self.moreTab_04,'05':self.moreTab_05,
			'06':self.moreTab_06,'07':self.moreTab_07,'08':self.moreTab_08,'09':self.moreTab_09,'10':self.moreTab_10,
			'11':self.moreTab_11,'12':self.moreTab_12,'13':self.moreTab_13,'14':self.moreTab_14,'15':self.moreTab_15,
			'16':self.moreTab_16,'17':self.moreTab_17,'18':self.moreTab_18,'19':self.moreTab_19,'20':self.moreTab_20,
			'21':self.moreTab_21,'22':self.moreTab_22,'23':self.moreTab_23,'24':self.moreTab_24,'25':self.moreTab_25,
			'26':self.moreTab_26,'27':self.moreTab_27,'28':self.moreTab_28,'29':self.moreTab_29,'30':self.moreTab_30,
			'31':self.moreTab_31,'32':self.moreTab_32,'33':self.moreTab_33,'34':self.moreTab_34,'35':self.moreTab_35,
			'36':self.moreTab_36,'37':self.moreTab_37,'38':self.moreTab_38,'39':self.moreTab_39,'40':self.moreTab_40,
			'41':self.moreTab_41,'42':self.moreTab_42,'43':self.moreTab_43,'44':self.moreTab_44,'45':self.moreTab_45,
			'46':self.moreTab_46,'47':self.moreTab_47,'48':self.moreTab_48,'49':self.moreTab_49,'50':self.moreTab_50,
			'51':self.moreTab_51,'52':self.moreTab_52,'53':self.moreTab_53,'54':self.moreTab_54,'55':self.moreTab_55,
			'56':self.moreTab_56,'57':self.moreTab_57,'58':self.moreTab_58,'59':self.moreTab_59,'60':self.moreTab_60,
			'61':self.moreTab_61,'62':self.moreTab_62,
		}


	def moreTab_exists(self,num):
		return self.isEleExists(self.moreTab_xpathDict[num],screen=1)
		
