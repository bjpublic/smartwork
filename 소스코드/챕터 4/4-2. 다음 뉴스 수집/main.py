import urllib3
import argparse
from bs4 import BeautifulSoup

news_baseURL = "https://media.daum.net/"
news_categories = {
    "사회": "society",
    "정치": "politics",
    "경제": "economic",
    "국제": "foreign",
    "문화": "culture",
    "IT": "digital" }

def get_html_from_daum_news(category):
    surl = news_baseURL + news_categories[category]
    req = urllib3.PoolManager()
    return req.request('GET', surl).data

def get_common_news(news_obj):
    img_url = news_obj.select('.thumb_g')[0].get('src').split('//')[1]

    title = news_obj.select('.tit_thumb a')[0].text
    url = news_obj.select('.tit_thumb a')[0].get('href')
    ref = news_obj.select('.info_thumb')[0].text.split('댓글 수')[0]
    ref = ref.replace('•', '').strip()
    news = main_news(title, url, ref, img_url)
    rel_links = news_obj.select('.relate_news .item_relate')

    for rel_link in rel_links:
        rel_link_title = rel_link.select('a')[0].text
        rel_link_url = rel_link.select('a')[0].get('href')
        rel_link_ref = rel_link.select('.info_news')[0].text
        news.add_rel_link(rel_link_title, rel_link_url, rel_link_ref)

    return news

def parse_head_news(bsobj):
    headline_news_tag = bsobj.select('.item_mainnews')[0]
    return get_common_news(headline_news_tag)

def parse_main_news(bsobj):
    main_news_list = []
    m_news_tag_list = bsobj.select('.list_mainnews li')

    for m_news_tag in m_news_tag_list:
        main_news = get_common_news(m_news_tag)
        main_news_list.append(main_news)

    return main_news_list

def parse_side_news(bsobj):
    s_news_tag_list = bsobj.select('.list_mainnews2 li')
    side_news_list = []

    for s_news_tag in s_news_tag_list:
        title = s_news_tag.select('.tit_mainnews .link_txt')[0].text
        url = s_news_tag.select('.tit_mainnews .link_txt')[0].get('href')
        ref = s_news_tag.select('.info_mainnews')[0].text.split('•')[0].strip()

        side_news = basic_news(title, url, ref)
        side_news_list.append(side_news)

    return side_news_list

def parse_IT():
    result = get_html_from_daum_news('IT')
    parsed = BeautifulSoup(result, 'html.parser')
    headline_news = parse_head_news(parsed)
    main_news_list = parse_main_news(parsed)
    side_news_list = parse_side_news(parsed)

    print('헤드라인 뉴스: ' + headline_news)
    print('메인 뉴스: ' + str(main_news_list))
    print('사이드 뉴스: ' + str(side_news_list))

def parse_ALL():
    for category in news_categories:
        c = news_categories[category]
        result = get_html_from_daum_news(c)
        parsed = BeautifulSoup(result, 'html.parser')
        headline_news = parse_head_news(parsed)
        main_news_list = parse_main_news(parsed)
        side_news_list = parse_side_news(parsed)

        print('카테고리: ' + category)
        print('헤드라인 뉴스: ' + headline_news)
        print('메인 뉴스: ' + str(main_news_list))
        print('사이드 뉴스: ' + str(side_news_list))

def main():
    parse_IT()
    parse_ALL()

def arg_main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--categories', nargs='+', help='카테고리 목록을 공백을 두고 나열', required=True)
    args = parser.parse_args()
    categories = args.categories

    for category in categories:
        result = get_html_from_daum_news(news_categories[category])
        parsed = BeautifulSoup(result, 'html.parser')

        headline_news = parse_head_news(parsed)
        main_news_list = parse_main_news(parsed)
        side_news_list = parse_side_news(parsed)

        print('카테고리: ' + category)
        print('헤드라인 뉴스: ' + headline_news)
        print('메인 뉴스: ' + str(main_news_list))
        print('사이드 뉴스: ' + str(side_news_list))

if __name__ == 'main':
    main()
    # arg_main() #파싱하고자 하는 카테고리를 프로그램 시작시 지정 가능
