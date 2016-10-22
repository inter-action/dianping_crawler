#core
import re
import time
import sys

# third lib
from selenium.common.exceptions import NoSuchElementException
# my lib
from ..driver import chrome_driver as mydriver
from ..logging import LOG

class Crawler:
    @staticmethod
    def get_followed(id):
        def next_link():
            return mydriver.find_element("a.page-next")

        def has_next_page():
            try:
                next_link()
                return True
            except NoSuchElementException:
                return False

        """
        [('宇宙无敌大羙麗', '15443091'),
        ('啦啦啦_27057', '1079941710'),
        ('点小评@北京', '1040611273'),...
        """
        url = "http://www.dianping.com/member/%s/follows" % id
        li_selector = "div.modebox.fllow-list ul > li div.tit > h6 > a"
        mydriver.navi_to(url)
        result = []
        while True:
            ls = mydriver.find_elements(li_selector)
            result.extend( [(e.text.strip("..."), e.get_attribute("user-id")) for e in ls] )
            if has_next_page():
                next_link().click()
            else: break

        return result

    @staticmethod
    def get_detailed_review(id):
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
        url = "http://www.dianping.com/review/{}".format(id)
        mydriver.navi_to(url)
        markbox = mydriver.find_element("div.box.remarkDet")
        shopbox = mydriver.find_element("div.box.reviewShop")

        def chats():
            def getto(root):
                try:
                    a = root.find_element_by_css_selector(".contList-con > a")
                    to_id = a.get_attribute("href").split("/")[-1]
                    return to_id
                except NoSuchElementException:
                    return None

            try:
                result = []
                dls = mydriver.find_elements("#followNote > dl")
                for dl in dls:
                    comment = {}
                    canchor = dl.find_element_by_css_selector("cite > a")
                    comment["uid"] = canchor.get_attribute("href").split("/")[-1]
                    comment["uname"] = canchor.text
                    comment["content"] = dl.find_element_by_css_selector(".contList-con > span").text
                    comment["time"] = dl.find_element_by_css_selector(".contList-fn > .date").text
                    to = getto(dl)
                    if to is not None:
                        comment["resp_to"] = to
                    result.append(comment)

                return result
            except NoSuchElementException:
                return []

        def rate():
            def time():
                e = markbox.find_element_by_css_selector(".contList-fn li:nth-child(1)")
                return e.text

            def rating():
                try:
                    e = markbox.find_element_by_css_selector("ul.contList-info > li > span")
                    cls = e.get_attribute("class")
                    if cls is not None and cls.startswith("msstar") is True:
                        return float(cls[6:]) / 10
                    return 0.0
                except NoSuchElementException:
                    return 0.0

            def image_ls():
                try:
                    es = markbox.find_elements_by_css_selector("#dp_c > li.item > p > a")
                    return [e.get_attribute("href") for e in es]
                except NoSuchElementException:
                    return []

            def comment():
                e = markbox.find_element_by_css_selector(".contList-con > p")
                return e.text

            e = {}
            e["time"] = time()
            e["rating"] = rating()
            e["image_ls"] = image_ls()
            e["comment"] = comment()
            e["id"] = id
            e["href"] = url
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

        return {"rate": rate(), "shop": shop(), "chats": chats()}

    @staticmethod
    def get_simple_review(parent_node):
        """
        这个不需要了, 放在这里， 这段代码，直接根据id跳到点评详情页面然后get_detailed_review用这个函数去搞
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

        :param parent_node:
        :return:
        """
        def rating():
            star_node_class = parent_node.find_element_by_css_selector(".mode-tc.comm-rst > span").get_attribute("class")
            matchObj = re.match(r"irr-star(\d+)", star_node_class, re.I)
            if matchObj:
                return float(matchObj.group(1)) / 10
            else:
                return 0.0

        shop = {}
        shop_a = parent_node.find_element_by_css_selector("h6>a")
        shop["href"] = shop_a.get_attribute("href")
        shop["id"] = shop["href"].split("/")[-1]
        shop["name"] = shop_a.text
        shop["addr"] = parent_node.find_element_by_css_selector(".mode-tc.addres > p").text

        rate = {}
        rate_info_node = parent_node.find_element_by_css_selector(".mode-tc.info")
        rate["id"] = rate_info_node.find_element_by_css_selector("a.aheart").get_attribute("data-id")
        rate["rating"] = rating()
        rate["time"] = rate_info_node.find_element_by_css_selector("span.col-exp").text[3:]
        rate["comment"] = parent_node.find_element_by_css_selector(".mode-tc.comm-entry").text
        

        return {"shop": shop, "rate": rate}


    @staticmethod
    def pagination_has_next():
        try:
            pg = mydriver.find_element(".pages-num")
            pg.find_element_by_css_selector(".page-next")
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    def get_detail_anchor(parent_node):
        # 这个函数也不用了, 留个尸体在这里
        try:
            return parent_node.find_element_by_css_selector('.mode-tc.comm-photo')
        except NoSuchElementException:
            return None

    @staticmethod
    def next_page():
        pg = mydriver.find_element(".pages-num")
        pg.find_element_by_css_selector(".page-next").click()

    @staticmethod
    def get_review_lis():
        return mydriver.find_elements(".comm-list .pic-txt > ul > li")

    @staticmethod
    def get_user_reivews(id):
        url = "http://www.dianping.com/member/%s/reviews" % id
        rs = []
        driver = mydriver.get_driver()
        driver.get(url)

        counter = 0
        try:
            while True:
                review_lis = Crawler.get_review_lis()
                for i in range(0, len(review_lis)):
                    # fix Message: stale element reference
                    review_lis = Crawler.get_review_lis()
                    li = review_lis[i]
                    heart_achor_id = li.find_element_by_css_selector("a.aheart").get_attribute("data-id")

                    try:
                        rs.append(Crawler.get_detailed_review(heart_achor_id))
                        driver.back()
                    except NoSuchElementException as e:
                        LOG.warn("encounting error, pause for now...", e)
                        print("\a") #play a beep
                        time.sleep(60)
                    time.sleep(0.2)

                counter += 1
                if counter % 10 == 0:
                    secs = 10
                    LOG.info("just in case.. reaching threshold, sleep for {} seconds".format(secs))
                    time.sleep(secs)

                if Crawler.pagination_has_next():
                    Crawler.next_page()
                    LOG.info("next page..")
                else:
                    break

        except:
            LOG.error("recovering failed...exiting..., page: {}, review_id: {} ".format(counter+1, id), sys.exc_info()[0])


        return rs

