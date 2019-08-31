"""
    Watch user likers stories!
    This script could be very useful to attract someone's audience to your account.
    If you will not specify the user_id, the script will use your likers as targets.
    Dependencies:
        pip install -U instabot
    Notes:
        You can change file and add there your comments.
"""

import os
import sys
import time
import random

# in case if you just downloaded zip with sources
sys.path.append(os.path.join(sys.path[0], '../../'))
from instabot import Bot

bot = Bot()
bot.login()

if len(sys.argv) >= 2:
    bot.logger.info(
        """
            Going to get '%s' likers and watch their stories (and stories of their likers too).
        """ % (sys.argv[1])
    )
    user_to_get_likers_of = bot.convert_to_user_id(sys.argv[1])
else:
    bot.logger.info(
        """
            Going to get your likers and watch their stories (and stories of their likers too).
            You can specify username of another user to start (by default we use you as a starting point).
        """
    )
    user_to_get_likers_of = bot.user_id

current_user_id = user_to_get_likers_of

text_file = open('id_smotr.txt', 'r')
lines = text_file.read().splitlines()
a = 0

while True:
    try:

        b = a + 10
        liker_ids = lines[a:b]

        # WATCH USERS STORIES
        if bot.watch_users_reels(liker_ids):
            bot.logger.info("Total stories viewed: %d" % bot.total["stories_viewed"])

        # CHOOSE RANDOM LIKER TO GRAB HIS LIKERS AND REPEAT
        current_user_id = random.choice(liker_ids)
        a += 10

        if random.random() < 0.05:
            current_user_id = user_to_get_likers_of
            bot.logger.info("Sleeping and returning back to original user_id=%s" % current_user_id)
            time.sleep(90 * random.random() + 60)
        if b == len(lines):
            print('Завершение программы, весь список пройден')
            break

    except Exception as e:
        # If something went wrong - sleep long and start again
        bot.logger.info(e)
        current_user_id = user_to_get_likers_of
        time.sleep(240 * random.random() + 60)
