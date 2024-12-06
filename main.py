import requests
import re
import json
import csv


with open('config.json', 'r') as config_file:
    config = json.load(config_file)

nrOfPosts = config['nrOfPosts']
hashtag = config['hashtag']
sessiontoken = config['sessiontoken']
ds_user_id = re.search(r'(.*?)%',sessiontoken).group(1)



def getCookiesAndTokens(sessiontoken, ds_user_id):
    headers = {'cookie': f'ds_user_id={ds_user_id}; sessionid={sessiontoken}; wd=740x809'}
    get1 = requests.get("https://www.instagram.com/", headers=headers)


    csrftoken = re.search(r'"csrf_token":"(.*?)"', get1.text).group(1)
    mid = re.search(r'mid":{"value":"(.*?)"', get1.text).group(1)
    datr = re.search(r'"_js_datr":{"value":"(.*?)"', get1.text).group(1)
    ig_did = re.search(r'"_js_ig_did":{"value":"(.*?)"', get1.text).group(1)
    app_id = re.search(r'"app_id":"(.*?)"', get1.text).group(1)
    claim = re.search(r'"claim":"(.*?)"', get1.text).group(1)

    return [csrftoken,mid,datr,ig_did,app_id,claim]



def scrapeHashtag(nrOfPosts, hashtag, sessiontoken, ds_user_id):
    [csrftoken,mid,datr,ig_did,app_id,claim] = getCookiesAndTokens(sessiontoken,ds_user_id)

    posts = []
    urlTail = ""

    while (len(posts)<nrOfPosts):
        headers = {
            'authority': 'www.instagram.com',
            'method': 'GET',
            'path': f'/api/v1/fbsearch/web/top_serp/?query=%23{hashtag}{urlTail}',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': f'mid={mid}; ig_did={ig_did}; datr={datr}; csrftoken={csrftoken}; ds_user_id={ds_user_id}; sessionid={sessiontoken}; wd=1387x809',
            'dpr': '2',
            'priority': 'u=0, i',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.86", "Chromium";v="131.0.6778.86", "Not_A Brand";v="24.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"macOS"',
            'sec-ch-ua-platform-version': '"15.1.1"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'viewport-width': '745',
            'x-asbd-id': '129477',
            'x-csrftoken': csrftoken,
            'x-ig-app-id': app_id,
            'x-ig-www-claim': claim,
            'x-requested-with': 'XMLHttpRequest'
        }
        params = {
            'query': f'#{hashtag}'
        }
        firstPostsSet = requests.get(f'https://www.instagram.com/api/v1/fbsearch/web/top_serp/?query=%23{hashtag}{urlTail}',headers=headers)
        
        postsre = re.findall(r'"media":(\s*\{[^}]*\})',firstPostsSet.text)
        
        if postsre:
            for media in postsre:
                typeMatch = re.search(r'"media_type":(.*?),',media)
                type = ""
                if typeMatch:
                    type = "Photo" if re.search(r'"media_type":(.*?),',media).group(1)=="1" else "Video" if re.search(r'"media_type":(.*?),',media).group(1)=="2" else "Carousel"
                imgUrlMatch = re.search(r'"image_versions2":{"candidates":\[{"width":.*?,"height":.*?,"url":"(.*?)"},',media)
                imgUrl = imgUrlMatch.group(1) if imgUrlMatch else ""
                videoUrlMatch = re.search(r'"video_versions"\:\[\{"height":1600,"id":"669485047419144v","type":101,"url":"(.*?)","',media)
                videoUrl = videoUrlMatch.group(1) if videoUrlMatch else ""
                commentCount = re.search(r'"fb_aggregated_comment_count":(.*?),',media)
                likeCount = re.search(r'"fb_aggregated_like_count":(.*?),',media)
                post = {
                        "Post Url": f"https://www.instagram.com/p/{re.search(r'"code":"(.*?)"',media).group(1) if re.search(r'"code":"(.*?)"',media) else ""}",
                        "Profile Url": f'https://www.instagram.com/{re.search(r'"username":"(.*?)"',media).group(1)}',
                        "Username": re.search(r'"username":"(.*?)"',media).group(1) if re.search(r'"username":"(.*?)"',media) else "",
                        "Full Name": re.search(r'"full_name":"(.*?)"',media).group(1) if re.search(r'"full_name":"(.*?)"',media) else "",
                        "Comment Count": commentCount.group(1) if commentCount else "",
                        "Like Count": likeCount.group(1) if likeCount else "",
                        "Pub Date": re.search(r'"taken_at":(.*?),',media).group(1) if re.search(r'"taken_at":(.*?),',media) else "",
                        "Description": re.search(r'"caption":\s*\{[^{}]*"text":\s*"([^"]+)"',media).group(1) if re.search(r'"caption":\s*\{[^{}]*"text":\s*"([^"]+)"',media) else "",
                        "Img Url": imgUrl,
                        "Type": type,
                        "Location": re.search(r'"city":"(.*?)"',media).group(1) if re.search(r'"city":"(.*?)"',media) else "",
                        "Video Url": videoUrl,
                        "View Count": re.search(r'"view_count":(.*?),',media).group(1) if re.search(r'"view_count":(.*?),',media) else ""
                    }
                
                posts.append(post)
                print(len(posts))
            
        next_max_id = re.search(r'"next_max_id": "(.*?)"',firstPostsSet.text)
        rank_token = re.search(r'""rank_token": "(.*?)"',firstPostsSet.text)
        urlTail = f'&next_max_id={next_max_id}&rank_token={rank_token}'


    return posts



def writePosts(posts):
    if posts:
        csv_columns = [
            "Post Url", "Profile Url", "Username", "Full Name", "Comment Count", "Like Count",
            "Pub Date", "Description", "Img Url", "Type", "Location", "Video Url", "View Count"
        ]

        csv_file = "output.csv"
        try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                writer.writerows(posts)
            print(f"{len(posts)} posts were successfully written to {csv_file}")
        except IOError as e:
            print(f"Error writing to CSV file: {e}")


posts = scrapeHashtag(nrOfPosts,hashtag,sessiontoken,ds_user_id)
writePosts(posts)