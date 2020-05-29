import urllib3
from bs4 import BeautifulSoup

def get_html_from_naver_search(keyword):
    burl = 'https://search.naver.com/search.naver?query='
    surl = burl + keyword
    req = urllib3.PoolManager()
    return req.request('GET', surl).data

class power_link:
    def __init__(self, title, url, desc, promo):
        self.title = title
        self.url = url
        self.desc = desc
        self.promo = promo

    def __str__(self):
        str_list = []
        str_list.append('타이틀: ' + self.title)
        str_list.append('주소: ' + self.url)
        str_list.append('설명: ' + self.desc)
        str_list.append('이벤트: ' + self.promo if self.promo != '' else  "없음")
        return ' / '.join(str_list)

    def __repr__(self):
        return self.__str__()

class blog:
    def __init__(self, title, upload_date, desc, author, url):
        self.title = title
        self.upload_date = upload_date
        self.desc = desc
        self.author = author
        self.url = url

    def __str__(self):
        str_list = []
        str_list.append('타이틀: ' + self.title)
        str_list.append('주소: ' + self.url)
        str_list.append('설명: ' + self.desc)
        str_list.append('저자: ' + self.author)
        str_list.append('업로드 일자: ' + self.upload_date)
        return ' / '.join(str_list)

    def __repr__(self):
        return self.__str__()

def parse_power_links(bsobj):
    power_links = []
    power_link_items = bsobj.select('#power_link_body .lst_type .lst')

    for power_link_item in power_link_items:
        title = power_link_item.select('.inner > a')[0].text
        url = power_link_item.select('.url_area > a')[0].text
        desc = power_link_item.select('.inner .ad_dsc:not(.promotion)')[0].text.strip()

        promotions = power_link_item.select('.inner .promotion')
        promotion = promotions[0].text.strip() if len(promotions) > 0 else ''

        new_power_link = power_link(title, url, desc, promotion)
        power_links.append(new_power_link)

    return power_links

def parse_blogs(bsobj):
    blogs = []
    blog_items = bsobj.select('.blog .type01 .sh_blog_top')

    for blog_item in blog_items:
        title = blog_item.select('dl > dt > a')[0].text
        upload_date = blog_item.select('.txt_inline')[0].text
        desc = blog_item.select('.sh_blog_passage')[0].text
        author = blog_item.select('.txt_block .inline > a')[0].text
        url = blog_item.select('.thumb > a')[0].attrs.get('href')

        new_blog = blog(title, upload_date, desc, author, url)
        blogs.append(new_blog)

    return blogs

if __name__ == "__main__":
    result = get_html_from_naver_search('파이썬')
    parsed = BeautifulSoup(result, 'html.parser')

    print('파워링크 수집 결과')
    print(*parse_power_links(parsed), sep='\n')

    print('\n블로그 수집 결과')
    print(*parse_blogs(parsed), sep='\n')