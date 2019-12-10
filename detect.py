from sms import send_text
import sqlite3
from datetime import datetime
import time as time
import praw
import threading
from config import *

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,client_secret=REDDIT_CLIENT_SECRET,user_agent='USERAGENT', username=REDDIT_USERNAME, password=REDDIT_PASSWORD)

class Detector():

	def __init__(self, subreddit_name, query, scrape_frequency=5, database_file_name=None):
		self.subreddit_name = subreddit_name
		self.subreddit = subreddit = reddit.subreddit(subreddit_name)
		self.query = query
		self.scrape_frequency = scrape_frequency

		# database file name defaults to subredditname.db
		self.database_file_name = database_file_name if database_file_name is not None else subreddit_name + '.db'
		self.db = sqlite3.connect(self.database_file_name, check_same_thread=False)
		self.db.execute('CREATE TABLE IF NOT EXISTS posts(url UNIQUE, user, timestamp);')

	def get_new(self, limit=1):
		return self.subreddit.new(limit=limit)

	def save_post(self, post):
		try:
			post_url = Detector.get_url(post)
			author_url = Detector.get_author_url(post)
			post_timestamp = Detector.get_timestamp(post)
			pretty_timestamp = Detector.get_pretty_date(post_timestamp)
			self.db.execute('INSERT INTO posts VALUES ((?), (?), (?))', [post_url, author_url, pretty_timestamp])
		except sqlite3.OperationalError:
			pass
		finally:
			self.db.commit()

	def post_exists(self, post_link):
		query_result = self.db.execute('SELECT link FROM posts WHERE link=(?)', [post_link]).fetchall()
		return bool(query_result)

	def sms_scrape(self):
		post = next(self.get_new(1))

		post_title = Detector.get_title(post)
		post_url = Detector.get_url(post)
		author_name = Detector.get_author_name(post)
		author_url = Detector.get_author_url(post)
		post_timestamp = Detector.get_timestamp(post)
		pretty_timestamp = Detector.get_pretty_date(post_timestamp)
		elapsed_time = Detector.get_pretty_elapsed(post_timestamp)

		if self.meets_query(post):
			# print('Meets Query')
			if not self.post_saved(post):
				print('It\'s a new post!')
				send_text('{0} {1} {2}'.format(post_title, post_url, elapsed_time + ' ago'))
				print('Text sent')

				self.save_post(post)
				print('Post saved!')

	def meets_query(self, post):
		text = Detector.get_title(post).lower()
		q = self.query.lower().split()
		for string in q:
			if string in text:
				return True
		return False

	def post_saved(self, post):
		post_url = Detector.get_url(post)
		query_result = self.db.execute('SELECT url FROM posts WHERE url=(?)', [post_url]).fetchall()
		return bool(query_result)

	def get_title(post):
		return post.title
	def get_url(post):
		return post.url
	def get_author_name(post):
		return post.author.name
	def get_author_url(post):
		return 'https://www.reddit.com/user/'.format(Detector.get_author_name(post))
	def get_timestamp(post):
		return post.created_utc
	def get_pretty_date(utc_timestamp):
		return datetime.utcfromtimestamp(utc_timestamp).strftime('%Y-%m-%d %H:%M:%S')
	def get_elapsed_seconds(utc_timestamp):
		now_timestamp = Detector.utc_now()
		return now_timestamp - utc_timestamp
	def get_pretty_elapsed(utc_timestamp):
		return pretty_time_delta(Detector.get_elapsed_seconds(utc_timestamp))
	def utc_now():
		return int(time.time())


	def get_posts(self):
		return self.db.execute('SELECT * FROM posts;').fetchall()
	def loop(self):
		try:
			self.sms_scrape()
		except Exception as e:
			print(e)
		finally:
			print('Searching for new posts in r/{0}...'.format(self.subreddit_name))
			threading.Timer(self.scrape_frequency, self.loop).start()
		# self.sms_scrape()
		# threading.Timer(2.0, self.loop).start()

def pretty_time_delta(seconds):
	# https://gist.github.com/thatalextaylor/7408395
	sign_string = '-' if seconds < 0 else ''
	seconds = abs(int(seconds))
	days, seconds = divmod(seconds, 86400)
	hours, seconds = divmod(seconds, 3600)
	minutes, seconds = divmod(seconds, 60)
	if days > 0:
		return '%s%dd%dh%dm%ds' % (sign_string, days, hours, minutes, seconds)
	elif hours > 0:
		return '%s%dh%dm%ds' % (sign_string, hours, minutes, seconds)
	elif minutes > 0:
		return '%s%dm%ds' % (sign_string, minutes, seconds)
	else:
		return '%s%ds' % (sign_string, seconds)