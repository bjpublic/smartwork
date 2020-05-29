import urllib3
import schedule
import time
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

class WebtoonNotExist(Exception): pass

def check_webtoon_update_by_name(update_status, target_title):
    for title in update_status:
        if target_title in title:
            print(target_title+'업데이트 상태:' + str(update_status[target_title]))
            return update_status

    raise WebtoonNotExist(target_title + ' 라는 웹툰은 존재하지 않습니다')

def job(week_of_day, target_title):
    parsed = get_html_from_naver_webtoon()
    update_status = parse_webtoon_list_by(parsed, week_of_day)

    try:
        update = check_webtoon_update_by_name(update_status, target_title)
        if update:
            print('웹툰 ' + target_title + '이 업데이트 되었습니다.')
            return schedule.CancelJob
    except WebtoonNotExist as e:
        print(e)

def every_minute_job_until_the_day(week_of_day, target_title, interval=1):
    minute_job = schedule.every(interval).minutes.do(job, week_of_day, target_title)
    schedule.every().day.do(cancel_job_after_midnight, minute_job)

def cancel_job_after_midnight(target_job):
    schedule.cancel_job(target_job)
    return schedule.CancelJob

if __name__ == '__main__':
    schedule.every().monday.do(every_minute_job_until_the_day, '월요일', '신의 탑', 1)
    schedule.every().tuesday.do(every_minute_job_until_the_day, '화요일', '사신소년', 60)
    schedule.every().thursday.do(every_minute_job_until_the_day, '목요일', '더 복서', 5)

    schedule.run_all()
    while True:
        schedule.run_pending()