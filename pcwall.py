# usage:
# python pcwall.py -s searchWord -out H:walpaper/images -n 10 # -n default is 1 for every word

# /usr/bin/python3 pcwall.py -s people wall dog -n 3 -o /home/oleg/img

import requests, urllib, sys, os
import argparse
import time

def createParser ():
	parser = argparse.ArgumentParser(
		description='''This is very useful program that allows you to get some new walpapers from www.unsplash.com.''',
		epilog='''(c) Eugene and Oleg 2018. This app was wrote during boring weekends.'''
	)
	# in case of problems with Windows install Ubuntu ;-) or just change '.' for windows style of folder path
	# '.' - mean current folder in Linux based OS from which pcwall.py script was launched
	parser.add_argument('-o', '--out', default=".")
	parser.add_argument('-n', '--number', nargs='?', type=int, default=1)
	parser.add_argument('-s', '--search', nargs='+', type=str, required=True)  # -s wall sex drugs "rock n roll"

	return parser


def loadPage(page_item, maxPhotosAmount):
	global total_pages, photo_counter
	page_num = "&page=" + str(page_item)
	get_photo_list_link = url_photo_list + page_num + query_str
	# print("** Try to get the page with photo " + get_photo_list_link + "\n")
	response = requests.get(get_photo_list_link)
	if response.status_code != 200:
		print("! Something wrong, I can`t access to server")
		return -1
	if response.headers['X-Ratelimit-Remaining'] == 0:
		print("Rate Limit Exceeded. Try one more time in an hour.")
		return -1
	print("** " + str(response.headers['X-Ratelimit-Remaining']) + " requests left");
	res = response.json()
	total_pages = res["total_pages"]
	res = res['results']
	photos = []
	for photo in res:
		img_name = photo["urls"]["full"].split("?")[0].split("/")[-1] + ".jpg"
		path_to_img_for_check_on_exists = out_path + '/' + img_name
		if not os.path.exists(path_to_img_for_check_on_exists):
			if photo["width"] > photo["height"]:
				photos.append(photo["urls"]["full"])

	for item in photos:
		img_name = item.split("?")[0].split("/")[-1] + ".jpg"
		print("*** GET photo [" + str(photo_counter + 1) + '] ' + item)
		img = urllib.request.urlretrieve(item, out_path + '/' + img_name)
		if img:
			photo_counter += 1

		if photo_counter >= maxPhotosAmount:
			return -1

if __name__ == '__main__':

	start_time = time.time()

	parser = createParser()
	params = parser.parse_args(sys.argv[1:])
	topics = params.search
	out_path = params.out
	maxPhotosAmount = params.number

	if out_path is not None:
		if not os.path.exists(out_path):
			os.makedirs(out_path)

	total_pages = 1
	client_id = "?client_id=111812491413a8045327ce7d8f9bdd0511c4aedfa3571b8b5133f65c79789703"
	url_photo_list = "https://api.unsplash.com/search/photos/" + client_id
	page_item = 1
	photo_counter = 0
	general_count = 0
	total_total_pages = 0

	print("Images source is www.unsplash.com\n")

	if topics:
		for topic in topics:
			photo_counter = 0
			query_str = "&query=" + topic
			print("Query: " + str(topic) + "\n")
			while page_item <= total_pages:
				if loadPage(page_item, maxPhotosAmount) == -1:  # photos amount
					break
				page_item += 1

			print("\n")

			general_count += photo_counter
			total_total_pages += total_pages

	print("Photos downloaded: " + str(general_count) + " from " + str(total_total_pages * 10) + " images")

	elapsed_time = time.time() - start_time
	print("Time spent: %.2fs" % elapsed_time)