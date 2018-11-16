import requests, urllib, sys, os


# FUNCS
def argController():
    global q, out_path;
    if len(sys.argv) > 1:
        if sys.argv[1] == "-h" or sys.argv[1] == "-help" or sys.argv[1] == "help":
            #  print HELP
            print("HELP \n");
            print("args:\n");
            print("\t-h or -help: call for help\n");
            print("\t-s or -search: give me photos by my search query\n");
            print("\t-out: path to out dir\n");
            print("EXAMPLE: \n");
            print("\t python pcwall.py -search cats -out C:/wallpaper\n");
            exit();
            pass

        if sys.argv[1] == "-s" or sys.argv[1] == "-search":
            q = sys.argv[2];
            pass;

        if sys.argv[3] == "-out":
            out_path = sys.argv[4];
            pass;
    else:
        exit();

    if q == "":
        print("Error, read help");
        exit();
    if out_path == "":
        print("Error, read help");
        exit();
    pass


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
    print("** GET info about photos from page " + "\n");
    for photo in res:
        photo_info = requests.get(photo["links"]["self"] + client_id);
        photo_info = photo_info.json();
        if photo_info["width"] > photo_info["height"]:
            photos.append(photo["urls"]["full"]);

    for item in photos:
        img_name = item.split("?")[0].split("/")[-1] + ".jpg";
        print("** GET photo " + item + "\n");
        img = urllib.request.urlretrieve(item, out_path + '/' + img_name);
        if img :
            photo_counter += 1;

    pass

# APP

q = "";
out_path = "";
argController();
if not os.path.exists(out_path):
    os.makedirs(out_path);
    pass

total_pages = 1;
client_id = "?client_id=111812491413a8045327ce7d8f9bdd0511c4aedfa3571b8b5133f65c79789703";
url_photo_list = "https://api.unsplash.com/search/photos/" + client_id;
page_item = 1;
photo_counter = 0;
query_str = "&query=" + q;
while page_item <= total_pages:
    loadPage(page_item);
    page_item += 1;
    print("************************\n");
    print("Go to next page if exists\n");
    pass

print("---- Photos was be downloaded ----");
print("Query: " + q + "\nCount photos: " + str(photo_counter) + "   Count pages: " + str(total_pages));
