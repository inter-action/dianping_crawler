from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
# my lib
from ..driver import chrome_driver as mydriver

class Crawler:
    @staticmethod
    def get_followed(id="5016495"):
        """
        [('宇宙无敌大羙麗', '15443091'),
        ('啦啦啦_27057', '1079941710'),
        ('点小评@北京', '1040611273'),...
        """
        url = "http://www.dianping.com/member/%s/follows" % id
        li_selector = "div.modebox.fllow-list ul > li div.tit > h6 > a"
        mydriver.navi_to(url)
        ls = mydriver.find_elements(li_selector)
        return [(e.text.strip("..."), e.get_attribute("user-id")) for e in ls]

    @staticmethod
    def get_review(id="309382395"):
        """
        返回大众点评单个review
        {'shop': {'tel': '17710850213', 
            'id': '67862761', 
            'name': 'AUV真人机械密室逃脱体验馆(芍药居店)', 
            'addr': '朝阳区芍药居北里309号B1楼'}
            'href': '..',
         'rate': {'id': '309382395',  # 评论ID
            'image_ls': ['http://www.dianping.com/photos/600819018/member',
            'http://www.dianping.com/photos/600819019/member',
            'http://www.dianping.com/photos/600819020/member',
            'http://www.dianping.com/photos/600819021/member'],
            'rating': 5.0,
            'time': '16-10-16 12:37'},
            'shop': {'addr': '海淀区万泉河路68号紫金庄园7号楼-12A09',
            'id': '/www.dianping.com/shop/24820793',
            'name': '回未轰趴馆(人大店)',
            'tel': '15810026196'},
            'href': '..'}
        """
        # url = "http://www.dianping.com/review/%s" % id
        # mydriver.navi_to(url)
        markbox = mydriver.find_element("div.box.remarkDet")
        shopbox = mydriver.find_element("div.box.reviewShop")


        def rate():
            def time():
                e = markbox.find_element_by_css_selector(".contList-fn li:nth-child(1)")
                return e.text

            def rating():
                e = markbox.find_element_by_css_selector("ul.contList-info > li > span")
                cls = e.get_attribute("class")
                if cls != None and cls.startswith("msstar") is True:
                    return 	float(cls[6:])/10
                return 0.0

            def image_ls():
                es = markbox.find_elements_by_css_selector("#dp_c > li.item > p > a")
                return [e.get_attribute("href") for e in es]

            def comment():
                e = markbox.find_element_by_css_selector(".contList-con > p")
                return e.text

            e = {}
            e["time"] = time()
            e["rating"] = rating()
            e["image_ls"] = image_ls()
            e["comment"] = comment()
            e["id"] = id
            e["href"] = "http://www.dianping.com/review/{}".format(id)
            return e

        def shop():
            e = {}
            na = shopbox.find_element_by_css_selector("h1>a")
            e["name"] = na.text
            e["href"] = na.get_attribute("href")
            e["id"] = na.get_attribute("href").split("/")[-1]
            e["addr"] = shopbox.find_element_by_css_selector("dl:nth-child(3) > dd > a").text
            e["tel"] = shopbox.find_element_by_css_selector(" dl:nth-child(4) > dd").text
            return e

        return {"rate": rate(), "shop": shop()}

    @staticmethod
    def pagination_has_next():
        pg = mydriver.find_element(".pages-num")
        try:
            pg.find_element_by_css_selector(".page-next")
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    def next_page():
        pg = mydriver.find_element(".pages-num")
        pg.find_element_by_css_selector(".page-next").click()

    @staticmethod
    def get_ls():
        ls = mydriver.find_elements(".mode-tc.comm-photo > a")
        return ls

    @staticmethod
    def get_user_reivews(id="5016495"):
        url = "http://www.dianping.com/member/%s/reviews" % id
        rs = []
        driver = mydriver.get_driver()
        driver.get(url)
        while Crawler.pagination_has_next():
            ls = Crawler.get_ls()

            for i in range(0, len(ls)):
                # fix Message: stale element reference
                ls = Crawler.get_ls()
                l = ls[i]

                rid = l.get_attribute("href").split("/")[-1]
                l.click()
                rs.append( Crawler.get_review(rid) )
                driver.back()

            Crawler.next_page()
        return rs

