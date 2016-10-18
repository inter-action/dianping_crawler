from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
# my lib
from driver import chrome_driver as mydriver


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

def get_review(id="309382395"):
    """
    返回大众点评单个review
    {'rate': {'id': '309382395',  # 评论ID
        'image_ls': ['http://www.dianping.com/photos/600819018/member',
        'http://www.dianping.com/photos/600819019/member',
        'http://www.dianping.com/photos/600819020/member',
        'http://www.dianping.com/photos/600819021/member'],
        'rating': 5.0,
        'time': '16-10-16 12:37'},
        'shop': {'addr': '海淀区万泉河路68号紫金庄园7号楼-12A09',
        'id': '/www.dianping.com/shop/24820793',
        'name': '回未轰趴馆(人大店)',
        'tel': '15810026196'}}
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
        return e

    def shop():
        e = {}
        na = shopbox.find_element_by_css_selector("h1>a")
        e["name"] = na.text
        e["id"] = na.get_attribute("href")[6:]
        e["addr"] = shopbox.find_element_by_css_selector("dl:nth-child(3) > dd > a").text
        e["tel"] = shopbox.find_element_by_css_selector(" dl:nth-child(4) > dd").text
        return e

    return {"rate": rate(), "shop": shop()}

def pagination_has_next():
    pg = mydriver.find_element(".pages-num")
    try:
        pg.find_element_by_css_selector(".page-next")
        return True
    except NoSuchElementException:
        return False

def next_page():
    pg = mydriver.find_element(".pages-num")
    pg.find_element_by_css_selector(".page-next").click()   

def get_ls():
    ls = mydriver.find_elements(".mode-tc.comm-photo > a")
    return ls 

def kick_start(id="5016495"):
    url = "http://www.dianping.com/member/%s/reviews" % id
    rs = []
    driver = mydriver.get_driver()
    driver.get(url)
    while pagination_has_next():
        ls = get_ls()

        for i in range(0, len(ls)):
            # fix Message: stale element reference 
            ls = get_ls()
            l = ls[i]

            rid = l.get_attribute("href").split("/")[-1]
            l.click()
            rs.append( get_review(rid) )
            driver.back()
        
        next_page()
    return rs

def main():
    driver = webdriver.Chrome()
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    driver.close()

if __name__ == '__main__':
    import sys
    sys.exit(int(main() or 0))