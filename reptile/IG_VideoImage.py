# 如果你是從無到有開始爬IG的話，以下請注意:
# 注意cookies
# 請查看一下get IG後的回傳HTML內容，他的回傳內容可能不如你所想
# IG資訊是JSON格式，你可以使用處理JSON格式的方法來取資訊
# 請注意IG翻頁的部分
# 請注意處理圖層與影片的部分，
#### ==========================================  該程式使用說明  =================================================================
# 本程式用來下載某IG帳戶的所有圖片與影片 (只能下載帳戶沒鎖，或是你有權限可觀看的帳戶)
#### 1. create_file()該函數是根據目標帳戶的名稱來建立資料夾與設定工作目錄
####
#### 2. 本程式主要枝幹函式 getwb()，這個函式用來進入目標對象的IG頁面，造訪所有頁面將發文的資訊記錄下來。(基本上每個頁面含有12個發文資訊)
####    進入IG網頁時，夾帶'sessionid':'xxxxxxxxxx'的訊息當成 cookies，請一定要先用自己的帳號在網頁上登錄IG，用網頁管理員查看cookies中
####     sessionid這項資訊，設定後會以我們的帳戶進入IG，這樣也可爬取我們有追蹤的人的頁面。
####
#### 3. 在getwb()這函數中，會提取出所有發文的連結資訊，接著呼叫getinfo_GraphSidecar()和getinfo_GraphVideo()這2個函式來處理
####    圖層(__typename=GraphSidecar)、影片(__typename=GraphVideo)的發文，因為這兩種型態需要進入文章的頁面後，才能進一步提
####    取我們需要的資訊。例如，圖層的發文:進入圖層頁面後才可以取到圖層中所有圖片的url; 而影片則是進入頁面後才能找到可下載的url。
####    當所有發文的資訊都整理完畢，會存在total_img_info該變數中，這個變數提供網址列表給get_img()函式下載所有圖片與影片。
####
#### 4. 將get_img()的inputdata設定成total_img_info，便可下載所有圖片，下載影像的迴圈也寫在裡面(但先標註起來不執行，這是為了避免下載
####    太大量的資料下來)
####
#### Note:
####    1.執行該程式，會發現處理圖層這類發文的時間很耗時，這是因為許多帳戶都有大量的圖層發文，但每篇圖層發文需要先進入圖層的網頁後，
#### 才可拿到該圖層中所有圖片的資訊; 而造訪每個圖層，我都讓程式休息5秒(測試的經驗是，若不休息5秒，很容易被強制關閉連線，10054 ERROR)。
#### 因此，光是處理圖層的資訊就會耗上大量的時間。例如:一位帳戶有800篇文，假設當中有400篇是圖層，代表光是進出每個圖層的網頁，就要
#### 花上400*5秒的時間，也就是將近35分鐘後，才取到圖層中所有圖片的資訊，完成這些步驟後，程式才會開始下載圖片。
####    2.這份程式目前還不寫try except來處理一些特殊的expection，這是為了讓程式比較簡單易讀，之後有空可能會再作改善，有問題再請提出。
#### ============================================================================================================================

import requests
from bs4 import BeautifulSoup
import json
from urllib import request, parse
import os
import time
import shutil

# === 設定 header
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}

# === 設定cookies，請先用自己的帳號在網頁上登錄，再用網頁管理員查看cookies，並使用sessionid這項資訊設定cookies，這項資訊也會代表我們的帳號，因此可以看到我們追蹤人的內文
cookies = {'sessionid':'21458365508%3AjhxkhPCqxYYp5x%3A9'}

# === create_file(target): 這個函式根據目標帳戶的名稱來創建資料夾並設定工作目錄，(之後圖片載下來會存在該資料夾)
def create_file(target):
    # set target account
    account_name = str(target)
    # set path
    fpath = r'.\{}'.format(account_name.strip())
    if not os.path.exists(fpath):
        os.mkdir(fpath)
    os.chdir(fpath)
    return os.getcwd()

# === getinfo_GraphSidecar(): 處理發文為圖層(__typename = GraphSidecar)的函數，將回傳圖層中所有圖片或影片的資訊
def getinfo_GraphSidecar(shortcode):
    #設定造訪每篇文的網頁，網址寫成: 'https://www.instagram.com/p/' + str(shortcode)
    url = 'https://www.instagram.com/p/' + str(shortcode)

    html = requests.get(url, headers=headers, cookies=cookies)
    response = BeautifulSoup(html.text, 'html.parser')
    a = response.select('script[type="text/javascript"]')
    #所需資料在window.__additionalDataLoaded當中，又在a中的第15個
    data_str = str(a[14].text)  # window.__additionalDataLoaded的字串檔
    ###做json前先預處理data的字串
    data_str = '{' + data_str.split("',{")[-1].strip(';').strip(')').strip()
    data_dict = json.loads(data_str)
    #dict_a就是圖層中，每張圖片的資訊區域
    dict_a = data_dict['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
    # ========= 紀錄每張相片資訊:  將在dict_a裏頭的img的型態/網址/short_code提出來 ===========
    sd_img_info = []
    img_info = [0, 0, 0]
    for item in dict_a:
        img_info[0] = item['node']['__typename']  # type of the img 將會是 GraphImage(圖片) or GraphVideo(影片)
        img_info[1] = item['node']['shortcode']  # shortcode可以用來造訪發文的網頁，網址寫成: 'https://www.instagram.com/p/'+img_info[1]
        if img_info[0] == 'GraphVideo': # 如果圖層中的某一個影像是影片時，將img_info[2]存成video_url
            img_info[2] = item['node']['video_url']
        else:  # 一般影像的處理
            img_info[2] = item['node']['display_url']  # 將img_info[2]存成img_url
        sd_img_info.append(img_info[:])
    time.sleep(5)  # 休息5秒，測試的經驗: 這邊需要休息5秒，不然很容易被強制關閉，產生10054的error
    #將圖層中所有資訊回傳出去
    return sd_img_info
# === getinfo_GraphVideo(): 處理發文為影片(__typename = GraphVideo)的函數，將回傳可下載影片的網址
def getinfo_GraphVideo(shortcode):
    # 設定造訪每篇文的網頁，網址寫成: 'https://www.instagram.com/p/' + str(shortcode)
    url = 'https://www.instagram.com/p/' + str(shortcode)
    html = requests.get(url, headers=headers, cookies=cookies)
    response = BeautifulSoup(html.text, 'html.parser')
    a = response.select('script[type="text/javascript"]')
    data_str = str(a[14].text) # 所需資料在window.__additionalDataLoaded當中，又在a中的第15個
    data_str = '{' + data_str.split("',{")[-1].strip(';').strip(')').strip()
    data_dict = json.loads(data_str)
    #v_url是影片可下載的播放網址
    v_url = data_dict['graphql']['shortcode_media']['video_url']
    time.sleep(1)  # 休息1秒
    # 將資訊回傳出去
    return v_url

# === getweb(): 造訪目標帳戶的主要函式，造訪帳戶的每一個頁面並提取資訊，會呼叫getinfo_GraphSidecar()和getinfo_GraphVideo()函式，
# === 最終整理出供下載的資料表 total_img_info，供get_img()函式，來下載圖片與影片
def getwb(target):
    ##設定IG目標帳戶的網址
    url = 'https://www.instagram.com/{}/?hl=zh-tw'.format(str(target))
    html = requests.get(url, headers=headers, cookies=cookies)
    response = BeautifulSoup(html.text, 'html.parser')
    a = response.select('script[type="text/javascript"]')  # 目標json在window._sharedData在當中，window._sharedData在a的第四個
    data_str = str(a[3].text)  # window._sharedData 的字串檔

    ###做json前先預處理data的字串
    data_str = '{' + data_str.split('= {')[-1].strip(';').strip()
    data_dict = json.loads(data_str)
    # page_cursor: 第一頁內容中指出的下一頁的參數
    page_cursor = data_dict['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
    # 將IG上的po文資訊存在a_dict
    dict_a = data_dict['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
    # id_target_num: 目標用戶的id
    id_target_num = data_dict['entry_data']['ProfilePage'][0]['graphql']['user']['id']

    # ========= 紀錄第一頁的相片資訊:  將在dict_a裏頭的img的型態/網址/short_code提出來 ===========
    tmp_img_info = []
    img_info = [0, 0, 0]
    count_sidercar = 0
    count_video = 0
    for item in dict_a:
        img_info[0] = item['node']['__typename']  # type of the img: GraphImage(一般圖片) or GraphSidecar(多張圖層) or GraphVideo(影片)
        img_info[1] = item['node']['shortcode']  # shortcode可以用來造訪發文的網頁，網址寫成: 'https://www.instagram.com/p/'+img_info[1]
        img_info[2] = item['node']['display_url']  # img_url
        tmp_img_info.append(img_info[:])
        if img_info[0] == 'GraphSidecar':
            count_sidercar += 1
        elif img_info[0] == 'GraphVideo':
            count_video += 1
    print('Page1: ')
    print(url)
    # ========= 開始進入第一頁後的每一頁，將結果存到 tmp_img_info中 =========
    count = 1
    while page_cursor is not None:
        count += 1
        var_num = {"id": id_target_num, "first": '12', "after": page_cursor}
        # 為variable的參數編碼
        var_num_code = parse.quote(json.dumps(var_num))
        # 製作下一頁的網址
        base = 'https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables='
        next_page_url = base + var_num_code
        print('Page{}: '.format(count))
        print(next_page_url)

        #造訪下一頁
        html_nextpage = requests.get(next_page_url, headers=headers, cookies=cookies)
        response_nextpage = BeautifulSoup(html_nextpage.text, 'html.parser')
        response_nextpage = json.loads(response_nextpage.text)
        # 更新下一頁的參數，若無下一頁，page_cursor會為None
        page_cursor = response_nextpage['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        dict_a = response_nextpage['data']['user']['edge_owner_to_timeline_media']['edges']

        # === 紀錄每一頁的發文資訊:  將在dict_a裏頭的img的型態/網址/short_code提出來
        img_info = [0, 0, 0]
        for item in dict_a:
            img_info[0] = item['node']['__typename']  # type of the img: GraphImage(一般圖片) or GraphSidecar(多張圖層) or GraphVideo(影片)
            img_info[1] = item['node']['shortcode']  # shortcode可以用來造訪發文的網頁，網址寫成: 'https://www.instagram.com/p/'+img_info[1]
            img_info[2] = item['node']['display_url']  # img_url
            tmp_img_info.append(img_info[:])
            if img_info[0] == 'GraphSidecar':
                count_sidercar += 1
            elif img_info[0] == 'GraphVideo':
                count_video += 1
        #抓完一頁資訊休息 1 秒
        time.sleep(1)

    # === 將跑完所有頁面的資料做統整性整理，重點: 將不同類型的發文作不同的處理: 呼叫getinfo_GraphSidecar()和getinfo_GraphVideo()函式
    total_img_info = {'GraphImage':[],'GraphSidecar':[],'GraphVideo':[]}
    print('處理圖層與影片資訊中，將耗時，請耐心...')
    #這只是粗估的時間，"最少"需要這樣的時間
    print('該帳戶有{}個圖層，{}個影片，預估最少需要{}分鐘來處理圖層與影片的資訊'.format(count_sidercar,count_video,(count_video*1+count_sidercar*5)//60))
    for item in tmp_img_info:
        #item[0]: type of the img => GraphImage or GraphSidecar(多張圖層) or GraphVideo(影片)
        #item[1]: 發文的網頁 'https://www.instagram.com/p/'+img_info[1]
        #item[2]: img_url
        # === 根據不同類型的圖檔做不同的動作
        if item[0] == 'GraphImage': # 圖檔為'GraphImage',將資訊存入
            total_img_info['GraphImage'].append(item[:])
        # 圖檔為'GraphSidecar(多張圖層)',使用函數getinfo_GraphSidecar(shortcode = item[1])造訪該圖層網頁，再提取資訊回傳回來
        # 圖層中若有影片，也會被getinfo_GraphSidecar()處理
        elif item[0] == 'GraphSidecar':
            data_Sidecar = getinfo_GraphSidecar(shortcode = item[1])
            for set in data_Sidecar:
                total_img_info[set[0]].append(set[:])
        #這邊處理的是'GraphVideo'，注意這邊不會處理到圖層中的影片，
        elif item[0] == 'GraphVideo': #圖檔為GraphVideo(影片)的case，使用getinfo_GraphVideo(shortcode = item[1])造訪該影片網頁，提取影片的播放網址，將網址回傳回來，
            data_video = getinfo_GraphVideo(shortcode = item[1])
            #data_video是回傳的播放網址(該網址才可用來下載影片)
            item[2] = data_video
            total_img_info['GraphVideo'].append(item[:])
    print('處理圖層與影片資訊完成!')
    return total_img_info

#==== get_img():下載圖片與影片的函式，根據total_img_info資料表來下載
def get_img(inputdata):

    # 下載圖片: 直接處理GraphImage的類型

    print('正在下載圖片...')
    print(inputdata)
    for i, info in enumerate(inputdata['GraphImage']):
        photo_url = info[2]
        #使用shortcode和號碼來編名
        request.urlretrieve(photo_url, './Img_No{}_{}.jpg'.format(i+1, info[1]))
        #休息
        time.sleep(1)
    print('完成下載，共有{}張圖片'.format(i+1))

    ### 下載影片的部分:
    # 一般情況下，我不希望下載太多的影片，因此會將這部分註解起來，暫不使用

    # 下載影片: 直接處理GraphVideo的類型
    '''
    print('正在下載影片...')
    for j, info in enumerate(inputdata['GraphVideo']):
        video_url = info[2]
        #使用shortcode和號碼來編名
        re = requests.get(video_url, stream=True)
        f = open('Video_No{}_{}.mp4'.format(j+1, info[1]), 'wb')
        shutil.copyfileobj(re.raw, f)
        f.close()
        #休息
        time.sleep(0.6)
    print('完成下載，共有{}個影片'.format(j + 1))
    '''


if __name__ == '__main__':
    target = 'u321122' #設定帳戶 ex: target = 'cawaiiun'
    create_file(target=target) #創建資料夾與設定工作目錄
    total_img_info = getwb(target=target) #開始爬蟲收集資訊
    print(total_img_info) #印出收集完成的資料表:total_img_info
    get_img(inputdata=total_img_info) #根據total_img_info來下載檔案
