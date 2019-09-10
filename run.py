from InstagramAPI import InstagramAPI
from random import randint
from datetime import date
from time import sleep
import schedule
import sys


instauser = 'XXXX'
instapass = 'XXXX'
whitelist = ['lackwardsbanguage', 'putln2']
schedule_time = '09:00'
daily_limit = 100
min_sleep = 15
max_sleep = 30
test_mode = 1


class C:
    W, G, R, P, Y, C = '\033[0m', '\033[92m', '\033[91m', '\033[95m', '\033[93m', '\033[36m'


def get_ids(api, user_id):
    gotcha = []
    next_max_id = True
    while next_max_id:
        if next_max_id is True:
            next_max_id = ''
        api.getUserFollowings(user_id, maxid=next_max_id)
        gotcha.extend(api.LastJson.get('users', []))
        next_max_id = api.LastJson.get('next_max_id', '')
    return gotcha


def instaspam(api, limit):
    today = date.today()
    now = today.strftime("%d/%m/%Y")
    print(f'{C.C}{now}{C.W}')
    user_id = api.username_id
    users = get_ids(api, user_id)
    a = 0
    b = len(users)
    c = len(whitelist)
    if b - c == 0:
        print(f'{C.G}\nDONE!\n{C.W}')
        sys.exit()
    else:
        for user in users:
            pk = user['pk']
            username = user['username']
            if not test_mode:
                api.unfollow(pk)
            if username in whitelist:
                print(f'-/-/-: {username} - WHITELISTED')
            else:
                print(f'{C.G}{a+1}{C.W}/{C.Y}{limit}{C.W}/{C.P}{b}{C.W} {username}')
                if not test_mode:
                    api.unfollow(pk)
                    break
                    sleep(randint(min_sleep, max_sleep))
                else:
                    sleep(0.2)
                a += 1
                if a >= limit:
                    break


def main():
    if test_mode:
        tm = f'{C.R}TEST MODE{C.W}'
    else:
        tm = ''
    print(f"""{C.Y}
╦ ╦╔╗╔╔═╗╔═╗╦  ╦  ╔═╗╦ ╦╔╗ ╔═╗╔╦╗
║ ║║║║╠╣ ║ ║║  ║  ║ ║║║║╠╩╗║ ║ ║
╚═╝╝╚╝╚  ╚═╝╩═╝╩═╝╚═╝╚╩╝╚═╝╚═╝ ╩ {C.C}v1{C.W} {tm}

Unfollowing {C.G}{daily_limit}{C.W} users every day at {C.G}{schedule_time}{C.W}
    """)
    api = InstagramAPI(instauser, instapass)
    api.login()
    if not test_mode:
        instaspam(api, daily_limit)
        schedule.every().day.at(schedule_time).do(
            instaspam, api=api, limit=daily_limit)
        while True:
            schedule.run_pending()
            sleep(1)
    else:
        instaspam(api, 10)


if __name__ == '__main__':
    main()
