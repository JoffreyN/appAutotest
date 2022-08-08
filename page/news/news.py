import logging,time
from selenium.webdriver.common.by import By
from page.base import PageBase

class PageNews(PageBase):
	def __init__(self,driver):
		# 资讯 页面
		super().__init__(driver)
		self.btnHotArticle1=(By.CLASS_NAME,"card")
		self.btnHotArticleTitle=(By.CLASS_NAME,"detailItem-title")

	#热门推荐
	def textHotTitle1(self):
		time.sleep(3)
		self.driver.execute_script('document.getElementsByClassName("card-title")[0].scrollIntoView();')
		time.sleep(1)
		text=self.driver.execute_script('return document.getElementsByClassName("card-title")[0].textContent;')
		return text

	def clickHotArticle1(self):
		logging.info('点击 热门推荐的第1篇文章')
		time.sleep(3)
		self.driver.execute_script('document.getElementsByClassName("card-title")[0].scrollIntoView();')
		time.sleep(1)
		self.myTap(self.findElement(self.btnHotArticle1))

	def textHotTitle2(self):
		time.sleep(3)
		for i in range(10):
			txt=self.findElement(self.btnHotArticleTitle).text
			if txt:return txt
			else:time.sleep(1)