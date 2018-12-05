# usage:
# python pcwall.py -s searchWord -out H:walpaper/images

# /usr/bin/python3 pcwall.py -s people -n 3 -t topics.txt # in this case -s not used because you have topics.txt

import requests, urllib, sys, os
import argparse
import time


# FUNCS
def createParser ():
	parser = argparse.ArgumentParser(
		description = '''This is very useful program that allows you to get some new walpapers.
		e.x. windows: 
		python pcwall.py -s nature -out H:walpaper/nature 
		or 
		python pcwall.py -s nature -out walpaper/nature
		for linux''',
		epilog = '''(c) Eugene and Oleg 2018. Developers are not responsible for anything happen in case of this script usage  -)''')
	parser.add_argument('-s', '--search', required=True)
	parser.add_argument('-o', '--out', default='img')
	parser.add_argument('-n', '--number', nargs='?', type=int, default=10)
	parser.add_argument('-t', '--topics', nargs='?', type=str)  # topics.txt e.x.

	return parser


def loadPage(page_item, maxPhotosAmount):
	global total_pages, photo_counter
	page_num = "&page=" + str(page_item)
	get_photo_list_link = url_photo_list + page_num + query_str
	print("** Try to get the page with photo " + get_photo_list_link + "\n")
	response = requests.get(get_photo_list_link)
	if response.status_code != 200:
		print("! Something wrong, I can`t access to server")
		return -1;
	if response.headers['X-Ratelimit-Remaining'] == 0:
		print("! End of the number of requests")
		return -1;
	print("** " + str(response.headers['X-Ratelimit-Remaining']) + " requests left\n");
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
		print("** GET photo [" + str(photo_counter + 1) + '] ' + item + "\n")
		img = urllib.request.urlretrieve(item, out_path + '/' + img_name)
		if img:
			photo_counter += 1

		if photo_counter >= maxPhotosAmount:
			return -1

def loadTopics(topics_path):
	if topics_path is None:
		return 0

	try:
		with open(topics_path, 'r', encoding='utf-8') as f:
			str1 = f.read()
			str2 = str1.rstrip("\n")
	except IOError:
		# print("Could not open file!") if params.topics != "topics.txt" else params.topics
		print("Could not open file!")
		return 0

	topics = str2.split(', ')
	return topics

# APP

if __name__ == '__main__':

	start_time = time.time()

	parser = createParser()
	params = parser.parse_args(sys.argv[1:])

	q = params.search
	out_path = params.out
	maxPhotosAmount = params.number

	topics = loadTopics(params.topics)

	if not os.path.exists(out_path):
		os.makedirs(out_path)

	total_pages = 1
	client_id = "?client_id=111812491413a8045327ce7d8f9bdd0511c4aedfa3571b8b5133f65c79789703"
	url_photo_list = "https://api.unsplash.com/search/photos/" + client_id
	page_item = 1
	photo_counter = 0
	general_count = 0
	total_total_pages = 0

	# Please, rewrite down section in a proper way if you can/want.

	if topics and len(topics) > 1:
		# print(len(topics))
		# print(topics)
		for q in topics:
			photo_counter = 0
			query_str = "&query=" + q
			while page_item <= total_pages:
				if loadPage(page_item, maxPhotosAmount) == -1:  # photos amount
					break
				page_item += 1

			general_count += photo_counter
			total_total_pages += total_pages
		print("Query: " + str(topics))
	else:
		# print(q)
		query_str = "&query=" + q
		while page_item <= total_pages:
			if loadPage(page_item, maxPhotosAmount) == -1:  # photos amount
				break
			page_item += 1
		general_count = photo_counter
		total_total_pages += total_pages
		print("Query: " + q)

	print("Count photos: " + str(general_count) + " from Total images " + str(total_total_pages * 10))

	elapsed_time = time.time() - start_time
	print("Total time: %.2fs" % elapsed_time)