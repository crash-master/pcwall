# usage:
# python pcwall.py -s searchWord -out H:walpaper/images

import requests, urllib, sys, os
import argparse


# FUNCS
def createParser ():
	parser = argparse.ArgumentParser(
		description = '''This is very useful program that allows you to get some new walpapers.
		e.x. windows: 
		python pcwall.py -s nature -out H:walpaper/nature 
		or 
		python pcwall.py -s nature -out walpaper/nature
		for linux''',
		epilog = '''(c) Zeny and Oleg 2018. developers are not responsible for anything happen in case of this script usage  ;-)''')
	parser.add_argument('-s', '--search', required=True)
	parser.add_argument('-o', '--out', default='img')
	parser.add_argument('-n', '--number', nargs='?', type=int, default=10)

	return parser


def loadPage(page_item):
	global total_pages, photo_counter;
	page_num = "&page=" + str(page_item);
	get_photo_list_link = url_photo_list + page_num + query_str;
	print("** Try to get the page with photo " + get_photo_list_link + "\n");
	response = requests.get(get_photo_list_link);
	if response.status_code != 200:
		print("!!!!!!!!!! Something wrong, I can`t access to server !!!!!!!!!!!");
		exit();
	res = response.json();
	total_pages = res["total_pages"];
	res = res['results'];
	length = len(res);
	photos = [];
	for photo in res:
		img_name = photo["urls"]["full"].split("?")[0].split("/")[-1] + ".jpg";
		path_to_img_for_check_on_exists = out_path + '/' + img_name;
		if not os.path.exists(path_to_img_for_check_on_exists):
			if photo["width"] > photo["height"]:
				photos.append(photo["urls"]["full"]);

	for item in photos:
		img_name = item.split("?")[0].split("/")[-1] + ".jpg";
		print("** GET photo [" + str(photo_counter + 1) + '] ' + item + "\n");
		img = urllib.request.urlretrieve(item, out_path + '/' + img_name);
		if img :
			photo_counter += 1;
		if photo_counter >= maxPhotosAmmount:
			return -1

# APP

if __name__ == '__main__':
	parser = createParser()
	params = parser.parse_args(sys.argv[1:])

	q = params.search
	out_path = params.out
	maxPhotosAmmount = params.number

	if not os.path.exists(out_path):
		os.makedirs(out_path);

	total_pages = 1;
	client_id = "?client_id=111812491413a8045327ce7d8f9bdd0511c4aedfa3571b8b5133f65c79789703";
	url_photo_list = "https://api.unsplash.com/search/photos/" + client_id;
	page_item = 1;
	photo_counter = 0;
	query_str = "&query=" + q;
	while page_item <= total_pages:
		if loadPage(page_item) == -1: # photos ammount
			break
		page_item += 1;
		print("************************\n");
		print("Go to next page if exists\n");

	print("---- Photos were downloaded ----");
	print("Query: " + q + "\nCount photos: " + str(photo_counter) + "   Count pages: " + str(page_item) + "   Total pages" + str(total_pages));
