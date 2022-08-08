import logging,time
from selenium.webdriver.common.by import By
try:
	from appium.webdriver.common.appiumby import AppiumBy
except:
	AppiumBy=By
from common.tools import switch_execute
from .base import PageBase

class PageUploadPic(PageBase):
	def __init__(self,driver):
		# 上传图片相关
		super().__init__(driver)
		self.btnFiles={
			'Android':(By.XPATH,"//*[@text='文档']"),
			'iOS':(AppiumBy.IOS_PREDICATE,"name=='照片图库'")
		}
		self.andPic=(By.ID,"com.android.documentsui:id/icon_thumb")
		self.andTuku=(By.XPATH,"//*[@text='图库']")
		self.andDCIMpic=(By.ID,"com.android.gallery3d:id/gl_root_view")

		self.iosAllPics=(By.IOS_PREDICATE,"name=='所有照片'")
		self.iosOnePic=(By.IOS_PREDICATE,"name contains '照片, 横排'")
		self.iosDone=(By.IOS_PREDICATE,"name=='完成'")

	@switch_execute
	def uploadPic(self):
		_info={'Android':'文档','iOS':'照片图库'}
		logging.info(f'点击 {_info[self.PFN]}')
		time.sleep(3)
		try:
			self.findElement(self.btnFiles[self.PFN]).click()
		except AttributeError:
			pass

		if self.PFN=='Android':
			logging.info('点击选择图片')
			time.sleep(3)
			if self.isEleExists(self.andTuku,5):
				self.findElement(self.andTuku).click()
				self.findElement(self.andDCIMpic).click()
				time.sleep(3)
				self.findElement(self.andDCIMpic).click()
			else:
				self.findElement(self.andPic).click()
		else:
			self.clickAllPic()
			logging.info('点击选中一个')
			self.findElement(self.iosOnePic).click()
			logging.info('点击完成')
			self.findElement(self.iosDone).click()

	def clickAllPic(self):
		for i in range(3):
			try:
				logging.info('点击所有照片')
				self.findElement(self.iosAllPics).click()
				return 
			except Exception as err:
				if i==2:raise Exception(f'点击所有照片失败')
				logging.info('点击坐标')
				if self.driver.capabilities['deviceName']=='iPhone 11 Pro Max':
					self.driver.tap([(178,728)])
				elif self.driver.capabilities['deviceName']=='iPhone 11 Pro':
					self.driver.tap([(160,645)])
				elif self.driver.capabilities['deviceName']=='iPhone 11':
					self.driver.tap([(186,730)])