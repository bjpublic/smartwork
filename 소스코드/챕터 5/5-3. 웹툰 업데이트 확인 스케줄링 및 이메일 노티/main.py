from bs4 import BeautifulSoup
import urllib3
import schedule
import smtplib
import mimetypes

from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from_addr = '보낼 메일 주소'
to_addr = ['받을 메일 주소 1', '받을 메일 주소 2', ...]

day_of_week_to_index = {
    "월요일": 0,
    "화요일": 1,
    "수요일": 2,
    "목요일": 3,
    "금요일": 4,
    "토요일": 5,
    "일요일": 6
}

def sendmail(from_addr, to, title, img_url, link_url):
    with open('announcement.txt', 'r') as file:
        filedata = file.read()

    filedata = filedata.replace('[제목]', title)
    filedata = filedata.replace('[이미지주소]', img_url)
    filedata = filedata.replace('[주소]', link_url)

    message = MIMEMultipart('alternative')
    message['Subject'] = '네이버 웹툰 <' + title + '> 업데이트 알림'
    message['From'] = from_addr 
    message['To'] = to_addr

    message.attach(MIMEText(filedata, 'html'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.ehlo()
        server.login('메일 계정 아이디', '앱 비밀번호') #자신의 것으로 대체 해 줘야함
        server.sendmail(from_addr, to, message.as_string())

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
        title = webtoon.select('.title')[0].text
        link_url = webtoon.select('.title')[0].get('href')
        img_url = webtoon.select('img')[0].get('src')
        is_updated = len(webtoon.select('.ico_updt')) > 0
        update_status[title] = (is_updated, link_url, link_url)

    return update_status

class WebtoonNotExist(Exception): pass

def check_webtoon_update_by_name(update_status, target_title):
    for title in update_status:
        if target_title in title:
           print(target_title+'업데이트 상태:'+str(update_status[target_title]))
           return update_status[target_title]

    raise WebtoonNotExist(target_title + ' 라는 웹툰은 존재하지 않습니다.')

def job(week_of_day, target_title):
    parsed = get_html_from_naver_webtoon()
    update_status = parse_webtoon_list_by(parsed, week_of_day)

    try:
        update, link_url, img_url = check_webtoon_update_by_name(update_status, target_title)
        if update is True:
            print('웹툰 ' + target_title + '이 업데이트 되었습니다.')
            sendmail(from_addr, ', '.join(to), target_title, link_url, img_url)
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
    schedule.every().thursday.do(every_minute_job_until_the_day, '목요일', '더 복서', 1).run()

    while True:
        schedule.run_pending()