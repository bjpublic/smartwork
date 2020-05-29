import urllib3
from bs4 import BeautifulSoup

day_of_week_to_index = {
    "월요일": 0,
    "화요일": 1,
    "수요일": 2,
    "목요일": 3,
    "금요일": 4,
    "토요일": 5,
    "일요일": 6
}

def get_html_from_naver_webtoon():
    burl = "https://comic.naver.com/webtoon/weekday.nhn"
    req = urllib3.PoolManager()
    return BeautifulSoup(req.request('GET', burl).data, 'html.parser')

def parse_webtoon_list_by(bsobj, day_of_week):
    update_status = {}

    index = day_of_week_to_index[day_of_week]
    webtoons = bsobj.select('.daily_all .col')[index]
    webtoons = webtoons.select('ul li')

    for webtoon in webtoons:
        img_url = webtoon.select('img')[0].get('src')
        title = webtoon.select('.title')[0].text
        is_updated = len(webtoon.select('.ico_updt')) > 0
        update_status[title] = is_updated

    return update_status

if __name__ == "__main__":
    parsed = get_html_from_naver_webtoon()

    update_status = parse_webtoon_list_by(parsed, "월요일")
    print(update_status)