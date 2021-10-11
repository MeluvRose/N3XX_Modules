import time
import re
from bs4 import BeautifulSoup
from bs4.element import ContentMetaAttributeValue
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# add selenium browser option
options = webdriver.ChromeOptions()
options.add_argument("--window-size=960,960");
browser = webdriver.Chrome("../chromedriver", options=options)
interval = 2

def crawlingSools():
    sools = list()

    # 모든 술의 정보 가져오기
    for page in range(1, 100):
        # open web page "thesool.com"
        url = f"https://thesool.com/front/find/M000000082/list.do?searchType=2&searchKey=&searchKind=&levelType=&searchString=&productId=&pageIndex={page}&categoryNm=&kind="
        browser.get(url);

        # get product information
        elem = browser.find_elements_by_class_name("item");

        # 한 페이지의 모든 술의 상세 정보 긁어오기
        for e in elem:
            # get image link
            try:
                image = e.find_element_by_tag_name("img").get_attribute("src")
                product_num = image.split('=')[1].split('&')[0]
            except:
                continue;
            # define BeautifulSoup object of current page
            soup = BeautifulSoup(e.text, "lxml")
            sool = soup.find('p').get_text()
            info = sool.split('\n')
            # info add in dict
            name = info[0]
            if ("(중복)" in name) | ("(단종)" in name):
                continue;
            ingredient = info[2].split('주원료 ')[1]
            ingredient = ingredient.strip(" 등").split(", ")
            proof = info[3].split('/')[2]
            if len(info) > 5:
                feature = info[5]
            else:
                feature = "";
            # sools[idx] = {"image":image, "product_num":product_num,
            #         "name":name, "ingredient":ingredient,
            #      "proof":proof.strip(), "intro":feature}

            sools.append({"image":image, "product_num":product_num,
                    "name":name, "ingredient":ingredient,
                 "proof":proof.strip(), "intro":feature})
            # idx+=1;
        time.sleep(interval);

    # browser.close(); #Hmm...why can't close or quit
    return sools;


# # 각 제품의 블로그 포스팅을 검색
def crawlingPosts(names):
    lst_posts = list()

    for n in names:
        url_search = f"https://search.naver.com/search.naver?query={n}&nso=&where=blog&sm=tab_opt"
        browser.get(url_search)

        # 현재 문서(페이지) 높이를 가져와서 저장
        prev_height = browser.execute_script("return document.body.scrollHeight")
        time.sleep(interval);

        cnt = 0
        while True:
            # 스크롤을 내림
            # (스크롤을 한 번 다 내렸을 경우, 30개의 포스트를 더 불러올 수 있음)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight)");
            # 페이지 로딩 대기
            time.sleep(interval);

            # 현재 문서 높이를 가져와서 저장
            curr_height = browser.execute_script("return document.body.scrollHeight");
            # 5번을 시행 했거나, 더이상 스크롤을 내릴 수 없을 때, 종료
            if (cnt > 4) | (curr_height == prev_height):
                break;
            cnt+=1;

        # 포스팅 된 글을 BeautifulSoup 객체를 통해 받아온다.
        soup = BeautifulSoup(browser.page_source, "lxml");
        posts = soup.find_all("li", attrs={"id":re.compile("^sp_blog_")})

        # with open("blog.html", 'w', encoding="utf-8") as f:
        #     f.write(soup.prettify())

        for p in posts:
            date = p.find("span", attrs={"class":"sub_time sub_txt"}).get_text() # 포스팅된 날짜
            title = p.find("a", attrs={"class":"api_txt_lines total_tit"}).get_text() # 포스팅된 글의 제목
            short = p.find(attrs={"api_txt_lines dsc_txt"}).get_text() # 포스팅된 글의 내용 일부
            thumb_count = p.find("span", attrs={"class":"thumb_count"}) # 포스팅에 사용된 이미지
            # check 'number of images is more than one'
            if thumb_count:
                thumb_count = int(thumb_count.get_text())
            else:
                thumb_count = 0
            # 성의 없거나, 광고일 것 같은 글 제외
            if (thumb_count < 6) | (thumb_count > 19):
                continue;
            lst_posts.append({"date":date, "title":title,
                "shorts":short, "thumb_count":thumb_count, "name":n})
            if len(lst_posts) % 20 == 0:
                break;

    return lst_posts;

def window_quit():
    browser.quit();
