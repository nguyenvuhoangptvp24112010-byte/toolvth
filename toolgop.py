from datetime import datetime
import random
import hashlib
from collections import Counter
import statistics
import platform
from datetime import datetime
import base64
import urllib.parse
import requests
import string
import math
import json
import os
import time
from colorama import Fore, Style, init

room_names={
    1: 'Nhà kho',
    2: 'Phòng họp',
    3: "Phòng Giám đốc",
    4: 'Phòng trò chuyện',
    5: 'Phòng Giám sát',
    6: 'Văn phòng',
    7: 'Phòng Tài Vụ',
    8: 'Phòng Nhân sự'
}
init(autoreset=True)
def clear_screen():
    os.system('cls' if platform.system() == "Windows" else 'clear')
def prints(r, g, b, text="text", end="\n"):
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m", end=end)

def top10_vth(s,headers,Coin):
    params = {
        'asset': Coin,
    }
    try:
        response = s.get('https://api.escapemaster.net/escape_game/recent_10_issues', params=params, headers=headers).json()
        ki=[]
        phong=[]
        for i in response['data']:
            ki.append(i['issue_id'])
            phong.append(i['killed_room_id'])
        return ki,phong
    except Exception as e:
        prints(247, 30, 30,f'LỖI khi lấy dữ liệu {e}')
        time.sleep(5)
        top10_vth(s,headers,Coin)
def load_data_vth():
    if os.path.exists('data-xw-vth.txt'):
        prints(0, 255, 243,'Bạn có muốn sử dụng thông tin đã lưu không? (y/n): ',end='')
        x=input()
        if x=='y':
            with open('data-xw-vth.txt','r',encoding='utf-8') as f:
                return json.load(f)
        prints(247, 255, 97,"═" * 47)
    str="""
Hướng dẫn lấy link:
    0. Mở chrome
    1. Truy cập website xworld.io
    2. Đăng nhập vào tài khoản
    3. Tìm và nhấp vào Vua thoát hiểm
    4. Nhấn lâp jtucs truy cập
    5. Sao chép link website và dán vào đây
"""
    prints(218, 255, 125,str)
    prints(247, 255, 97,"═" * 47)
    prints(125, 255, 168,'📋Nhập liên kết của bạn:',end=' ')
    link=input()
    user_id=link.split('&')[0].split('?userId=')[1]
    user_secretkey=link.split('&')[1].split('secretKey=')[1]
    prints(218, 255, 125,f'    Your user id is {user_id}')
    prints(218, 255, 125,f'    Your user secret key is {user_secretkey}')
    json_data={
        'user-id':user_id,
        'user-secret-key':user_secretkey,
    }
    with open('data-xw-vth.txt','w+',encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    return json_data
def kiem_tra_kq_vth(s,headers,ki,bot_chon,Coin,tg):
    try:
        start_time=time.time()
        while True:
            if time.time()<=tg+60:
                prints(255,255,0,f'Đang chờ kết quả {time.time()-start_time:.0f}...',end='\r')
                time.sleep(1)
            data_top10=top10_vth(s,headers,Coin)
            prints(255,255,0,f'Đang chờ kết quả {time.time()-start_time:.0f}...',end='\r')
            if data_top10[0][0]==int(ki):
                prints(15, 87, 219,f'Kẻ giết người đã vào phòng số {data_top10[1][0]} : {room_names[data_top10[1][0]]}')
                if int(bot_chon)==int(data_top10[1][0]):
                    prints(255, 0, 38,'Bạn thua rồi. Chúc bạn may mắn lần sau nhé...')
                    time.sleep(10)
                    return False,time.time()
                else:
                    prints(0, 255, 102,' Xin chúc mừng, bạn đã thắng')
                    time.sleep(10)
                    return True,time.time()
            time.sleep(1)
    except Exception as e:
        prints(255,0,0,f'Lỗi khi kiểm tra kết quả: {e}')
        return kiem_tra_kq_vth(s,headers,ki,bot_chon,Coin,tg)
def chon_phong1(data_top10,data_top100):
    while True:
        result=random.randint(1,8)
        if result!=data_top10[1][0]:
            return result
def chon_phong(data10,data100,hisory,trap):
    x=1
    if len(hisory)>=1:
        if hisory[0]['kq']==False:
            x=trap
    bot_chon=chon_phong1(data10,data100)
    return bot_chon,x
def bet_vth(s,user_id,user_secretkey,room_id,Coin,bet_amount):
    try:
        headers = {
            'accept': '*/*',
            'accept-language': 'vi,en;q=0.9',
            'cache-control': 'no-cache',
            'country-code': 'vn',
            'origin': 'https://xworld.info',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://xworld.info/',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'user-id': user_id,
            'user-login': 'login_v2',
            'user-secret-key': user_secretkey,
            'xb-language': 'vi-VN',
        }
        json_data = {
            'asset_type': Coin,
            'user_id': user_id,
            'room_id': room_id,
            'bet_amount': float(bet_amount),
        }
        response = s.post('https://api.escapemaster.net/escape_game/bet', headers=headers, json=json_data).json()
        prints(255,255,0,response)
        if response['code']==0 and response['msg']=='ok':
            prints(0, 149, 255,f' Đã đặt {bet_amount} {Coin} vào phóng số {room_id}')
            return bet_amount
        else:
            prints(255,0,0,response['msg'])
            return bet_amount
    except Exception as e:
        prints(255, 0, 4,f' {e}')
        return bet_amount
def user_asset(s,headers):
    try:
        json_data = {
            'user_id': int(headers['user-id']),
            'source': 'home',
        }

        response = requests.post('https://wallet.3games.io/api/wallet/user_asset', headers=headers, json=json_data).json()
        asset={
            'USDT':response['data']['user_asset']['USDT'],
            'WORLD':response['data']['user_asset']['WORLD'],
            'BUILD':response['data']['user_asset']['BUILD']
        }
        return asset
    except Exception as e:
        prints(255,0,0,f'Error when getting balance: {e}')
        prints(255,0,0,f'Vui lòng lấy lại link và thử lại')
        exit(1)
def print_stats(s, stats, headers, Coin):
    asset = user_asset(s, headers)
    prints(5,255,0,f'{asset['USDT']:.2f}USDT - {asset['WORLD']:.2f}WORLD - {asset['BUILD']:.2f}BUILD')
    prints(66, 239, 245,F'Thắng: {stats['win']}/{stats['win']+stats['lose']}')
    prints(66, 239, 245,F'Lời: {asset[Coin]-stats['asset0']}')
    prints(66, 239, 245,F'Chuỗi thắng: {stats['streak']} (MAX: {stats['max_streak']})')
    total_games = stats['win'] + stats['lose']
    win_rate = (stats['win'] / total_games * 100) if total_games > 0 else 0
    earn = asset[Coin] - stats['asset0']
def top100_vth(s,headers,Coin):
    params = {
        'asset': Coin,
    }
    try:
        response = s.get('https://api.escapemaster.net/escape_game/recent_100_issues', params=params, headers=headers).json()
        return response['data']['room_id_2_killed_times']
    except Exception as e:
        prints(247, 30, 30,f'LỖI khi lấy dữ liệu {e}')
        time.sleep(5)
        return top100_vth(s,headers,Coin)

def vth():
   
    s=requests.Session()
    data=load_data_vth()
    headers = {
        'accept': '*/*',
        'accept-language': 'vi,en;q=0.9',
        'cache-control': 'no-cache',
        'country-code': 'vn',
        'origin': 'https://xworld.info',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://xworld.info/',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        'user-id': data['user-id'],
        'user-login': 'login_v2',
        'user-secret-key': data['user-secret-key'],
        'xb-language': 'vi-VN',
    }
    asset=user_asset(s,headers)
    prints(5,255,0,f'BALANCE: {asset['USDT']:.2f}USDT - {asset['WORLD']:.2f}WORLD - {asset['BUILD']:.2f}BUILD')
    prints(5,255,0,"""
        1. BUILD
        2. USDT
        3. WORLD
        """)
    prints(255,255,0,f'Chọn loại tiền bạn muốn chơi (1/2/3): ',end='')
    Coin=input()
    if Coin=='1':
        Coin='BUILD'
    elif Coin=='2':
        Coin='USDT'
    elif Coin=='3':
        Coin='WORLD'
    prints(255,255,0,f'Nhập số lương {Coin} để đặt (Gợi ý: {asset[Coin]/111:.2f}): ',end='')
    bet_amount0=float(input())
    prints(255,255,0,f'Ví dụ khi bạn đặt hệ số cược là 10 thì nếu ván này bạn đặt 100 build và đã thua thì ván sau mức cược sẽ tăng x10, sẽ đặt 1000 build')
    trap=float(input('Nhập hệ số cược sau khi thua: '))
    delay1=int(input('Sau bao nhiêu ván thì tạm nghỉ (Nhập 999 nếu không muốn tạm nghỉ): '))
    delay2=int(input(f'Sau {delay1} ván thì tạm nghỉ bao nhiêu ván (Nhập 0 nếu không muốn nghỉ): '))
    hisory=[]
    stats={
        'win':0,
        'lose':0,
        'asset0':asset[Coin],
        'streak':0,
        'max_streak':0,
    }
    tg=time.time()-60
    clear_screen()

    tong=0
    while True:
        tong+=1
        prints(247, 255, 97,"═" * 47)
        data10=top10_vth(s,headers,Coin)
        data100=top100_vth(s,headers,Coin)
        bot_chon=chon_phong(data10,data100,hisory,trap)
        ki=data10[0][0]+1
        print_stats(s,stats,headers,Coin)
        prints(5,255,0,f'Dự đoán cho kì {ki} : {bot_chon[0]} - {room_names[int(bot_chon[0])]}')
        cycle = delay1 + delay2
        pos = (tong - 1) % cycle
        if pos < delay1:
            stop=False
            bet_amount=bet_vth(s,data['user-id'],data['user-secret-key'],bot_chon[0],Coin,float(bet_amount0) if bot_chon[1]==1 else float(hisory[0]['bet_amount'])*bot_chon[1])
        else:
            stop=True
            prints(255,255,0,f'Ván này tạm nghỉ')
            bet_amount=bet_amount0
        result,tg=kiem_tra_kq_vth(s,headers,ki,bot_chon[0],Coin,tg)
        if result==True:
            stats['win']+=1
            stats['streak']+=1
            stats['max_streak']=max(stats['max_streak'],stats['streak'])
        elif result==False:
            stats['lose']+=1
            stats['streak']=0
        if stop==False:
            hisory.insert(0, {'bot_chon': bot_chon[0], 'kq': result,'bet_amount':bet_amount})
import hashlib
from collections import Counter
import statistics
import platform
from datetime import datetime
import base64
import urllib.parse
import requests
import random
import string
import math
import json
import os
import random
import requests
import time
from colorama import Fore, Style, init
import threading
init(autoreset=True)

# ==================== CẤU HÌNH MÀU SẮC ====================
class Colors:
    # Màu Gradient
    GRADIENT1 = (255, 215, 0)      # Vàng gold
    GRADIENT2 = (255, 140, 0)      # Cam
    GRADIENT3 = (255, 69, 0)       # Cam đỏ
    GRADIENT4 = (255, 20, 147)     # Hồng đậm
    GRADIENT5 = (138, 43, 226)     # Tím
    
    # Màu chính
    CYAN = (0, 255, 255)
    GREEN = (50, 255, 50)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)
    RED = (255, 50, 50)
    PURPLE = (170, 0, 255)
    PINK = (255, 105, 180)
    BLUE = (50, 150, 255)
    WHITE = (255, 255, 255)
    
    # Màu nền gradient cho banner
    BG_START = (0, 100, 255)       # Xanh dương
    BG_END = (255, 0, 255)          # Tím

NV = {
    1: 'Bậc thầy tấn công',
    2: 'Quyền sắt',
    3: 'Thợ lặn sâu',
    4: 'Cơn lốc sân cỏ',
    5: 'Hiệp sĩ phi nhanh',
    6: 'Vua home run'
}

def clear_screen():
    os.system('cls' if platform.system() == "Windows" else 'clear')

def prints(r, g, b, text="text", end="\n"):
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m", end=end)

def print_gradient(text, start_color, end_color, end="\n"):
    """In chữ với hiệu ứng gradient"""
    length = len(text)
    for i, char in enumerate(text):
        ratio = i / length
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        prints(r, g, b, char, end="")
    print(end=end)

def print_box(text, color=Colors.CYAN, width=60):
    """In khung bao quanh text"""
    prints(color[0], color[1], color[2], "╔" + "═" * (width-2) + "╗")
    
    # Chia text thành nhiều dòng nếu dài
    lines = []
    words = text.split()
    current_line = ""
    for word in words:
        if len(current_line + " " + word) <= width-4:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    for line in lines:
        padding = width - 4 - len(line)
        left_pad = padding // 2
        right_pad = padding - left_pad
        prints(color[0], color[1], color[2], "║ " + " " * left_pad + line + " " * right_pad + " ║")
    
    prints(color[0], color[1], color[2], "╚" + "═" * (width-2) + "╝")

def print_header(text, color=Colors.GRADIENT1):
    """In tiêu đề với đường kẻ đẹp"""
    prints(color[0], color[1], color[2], "━" * 40)
    prints(color[0], color[1], color[2], f"   {text}")
    prints(color[0], color[1], color[2], "━" * 40)

def print_success(text):
    prints(Colors.GREEN[0], Colors.GREEN[1], Colors.GREEN[2], f"{text}")

def print_error(text):
    prints(Colors.RED[0], Colors.RED[1], Colors.RED[2], f"{text}")

def print_warning(text):
    prints(Colors.ORANGE[0], Colors.ORANGE[1], Colors.ORANGE[2], f"{text}")

def print_info(text):
    prints(Colors.CYAN[0], Colors.CYAN[1], Colors.CYAN[2], f"{text}")

def print_betting(text):
    prints(Colors.PURPLE[0], Colors.PURPLE[1], Colors.PURPLE[2], f"{text}")

def print_stats(text):
    prints(Colors.GREEN[0], Colors.GREEN[1], Colors.GREEN[2], f"{text}")

def print_money(text, coin_type):
    """In số tiền với màu sắc theo loại coin"""
    if coin_type == "USDT":
        prints(50, 255, 50, f"{text}")
    elif coin_type == "BUILD":
        prints(255, 215, 0, f"{text}")
    else:
        prints(100, 200, 255, f"{text}")

def banner(game):
    clear_screen()
    banner_text = """
    ██╗  ██╗ ██████╗ ██████╗ ██████╗ ███████╗
    ██║  ██║██╔════╝██╔═══██╗██╔══██╗██╔════╝
    ███████║██║     ██║   ██║██║  ██║█████╗  
    ██╔══██║██║     ██║   ██║██║  ██║██╔══╝  
    ██║  ██║╚██████╗╚██████╔╝██████╔╝███████╗
    ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
    """
    # In banner với hiệu ứng gradient
    lines = banner_text.split('\n')
    for i, line in enumerate(lines):
        if line.strip():
            ratio = i / len(lines)
            r = int(Colors.GRADIENT1[0] + (Colors.GRADIENT5[0] - Colors.GRADIENT1[0]) * ratio)
            g = int(Colors.GRADIENT1[1] + (Colors.GRADIENT5[1] - Colors.GRADIENT1[1]) * ratio)
            b = int(Colors.GRADIENT1[2] + (Colors.GRADIENT5[2] - Colors.GRADIENT1[2]) * ratio)
            prints(r, g, b, line)
    
    print()
    print_gradient(f"   XWORLD - {game} v1.0", Colors.GRADIENT2, Colors.GRADIENT4)
    print()
    
    print_header("", Colors.YELLOW)

def load_data_cdtd():
    if os.path.exists('data-xw-cdtd.txt'):
        print_header("DU LIEU DA LUU", Colors.CYAN)
        print_info("Phat hien du lieu dang nhap cu")
        prints(Colors.YELLOW[0], Colors.YELLOW[1], Colors.YELLOW[2], "Ban co muon su dung thong tin da luu khong? (y/n): ", end='')
        x = input().lower()
        if x == 'y':
            with open('data-xw-cdtd.txt', 'r', encoding='utf-8') as f:
                data = json.load(f)
                print_success("Da tai du lieu thanh cong!")
                return data
        print_warning("Tiep tuc voi du lieu moi...")
    
    print_header("HUONG DAN LAY LINK", Colors.ORANGE)
    guide = """
    CAC BUOC THUC HIEN:
    
    1. Truy cap vao trang web xworld.io
    2. Dang nhap tai khoan cua ban
    3. Chon game "Chay dua toc do"
    4. Nhan "Lap tuc truy cap"
    5. Copy toan bo link tren thanh dia chi
    6. Dan vao o ben duoi
    """
    prints(218, 255, 125, guide)
    print_header("", Colors.ORANGE)
    
    prints(125, 255, 168, 'Nhap link cua ban: ', end='')
    link = input().strip()
    
    try:
        user_id = link.split('&')[0].split('?userId=')[1]
        user_secretkey = link.split('&')[1].split('secretKey=')[1]
        
        print_success(f"User ID: {user_id}")
        print_success(f"Secret Key: {user_secretkey[:10]}...")
        
        json_data = {
            'user-id': user_id,
            'user-secret-key': user_secretkey,
        }
        
        with open('data-xw-cdtd.txt', 'w+', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        
        print_success("Da luu thong tin thanh cong!")
        return json_data
    except Exception as e:
        print_error(f"Loi xu ly link: {e}")
        print_warning("Vui long kiem tra lai link va thu lai!")
        return load_data_cdtd()

def top_100_cdtd(s):
    headers = {
        'accept': '*/*',
        'accept-language': 'vi,en;q=0.9',
        'origin': 'https://sprintrun.win',
        'referer': 'https://sprintrun.win/',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36',
    }
    try:
        response = s.get('https://api.sprintrun.win/sprint/recent_100_issues', headers=headers).json()
        nv = [1, 2, 3, 4, 5, 6]
        kq = []
        for i in range(1, 7):
            kq.append(response['data']['athlete_2_win_times'][str(i)])
        return nv, kq
    except Exception as e:
        print_error(f'Loi khi lay top 100: {e}')
        return top_100_cdtd(s)

def top_10_cdtd(s, headers):
    params = ''
    try:
        response = s.get('https://api.sprintrun.win/sprint/recent_10_issues', params=params, headers=headers).json()
        ki = []
        kq = []
        for i in response['data']['recent_10']:
            ki.append(i['issue_id'])
            kq.append(i['result'][0])
        return ki, kq
    except Exception as e:
        print_error(f'Loi khi lay top 10: {e}')
        return top_10_cdtd(s, headers)

def print_data(data_top10_cdtd, data_top100_cdtd):
    print_header("DU LIEU THONG KE", Colors.CYAN)
    
    # Hiển thị 10 ván gần nhất
    print_info("10 VAN GAN NHAT:")
    for i in range(len(data_top10_cdtd[0])):
        result_color = Colors.GREEN if data_top10_cdtd[1][i] in [1, 2, 3] else Colors.ORANGE
        prints(result_color[0], result_color[1], result_color[2], 
               f"   Ky #{data_top10_cdtd[0][i]}: {NV[int(data_top10_cdtd[1][i])]}")
    
    print_header("", Colors.YELLOW)
    
    # Hiển thị thống kê 100 ván
    print_info("THONG KE 100 VAN GAN NHAT:")
    total_wins = sum(data_top100_cdtd[1])
    for i in range(6):
        wins = data_top100_cdtd[1][int(i)]
        percent = (wins / total_wins) * 100 if total_wins > 0 else 0
        bar_length = int(percent / 2)  # 50% = 25 ký tự
        bar = "█" * bar_length + "░" * (25 - bar_length)
        
        # Màu sắc theo thứ hạng
        if i < 2:
            color = Colors.RED
        elif i < 4:
            color = Colors.YELLOW
        else:
            color = Colors.GREEN
            
        prints(color[0], color[1], color[2], 
               f"   {NV[int(i+1)]:<25}: {wins:3d} lan ({percent:4.1f}%)")
        prints(color[0], color[1], color[2], f"      [{bar}]")
    
    print_header("", Colors.YELLOW)

def selected_NV(data_top10_cdtd, data_top100_cdtd, htr, heso, bet_amount0):
    bet_amount = bet_amount0
    if len(htr) >= 1:
        if htr[len(htr)-1]['kq'] == False:
            bet_amount = heso * htr[len(htr)-1]['bet_amount']
    try:
        win_count_10 = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for result in data_top10_cdtd[1]:
            nv = int(result)
            win_count_10[nv] += 1
        sorted_nv = sorted(win_count_10.items(), key=lambda x: x[1])
        top3_least_wins = [nv for nv, wins in sorted_nv[:3]]
        return top3_least_wins, bet_amount
    except Exception as e:
        print_error(f'Loi khi chon: {e}')
        return [random.randint(1, 6)], bet_amount

def kiem_tra_kq_cdtd(s, headers, list_kq, ki):
    start = time.time()
    print_betting(f'Dang doi ket qua cua ky #{ki}')
    while True:
        data_top10_cdtd = top_10_cdtd(s, headers)
        if int(data_top10_cdtd[0][0]) == int(ki):
            actual_result = int(data_top10_cdtd[1][0])
            prints(Colors.GREEN[0], Colors.GREEN[1], Colors.GREEN[2], 
                   f'Ket qua ky #{ki}: {NV[actual_result]}')
            if actual_result in list_kq:
                print_success('CHUC MUNG! Ban da thang!')
                return True
            else:
                print_error('Rat tiec! Ban da thua!')
                return False
        elapsed = time.time() - start
        prints(Colors.CYAN[0], Colors.CYAN[1], Colors.CYAN[2], 
               f'Dang doi ket qua... {elapsed:.0f}s', end='\r')

def user_asset(s, headers):
    try:
        json_data = {
            'user_id': int(headers['user-id']),
            'source': 'home',
        }
        response = s.post('https://wallet.3games.io/api/wallet/user_asset', headers=headers, json=json_data).json()
        asset = {
            'USDT': response['data']['user_asset']['USDT'],
            'WORLD': response['data']['user_asset']['WORLD'],
            'BUILD': response['data']['user_asset']['BUILD']
        }
        return asset
    except Exception as e:
        print_error(f'Loi khi lay so du: {e}')
        return user_asset(s, headers)

def print_stats_cdtd(stats, s, headers, Coin):
    try:
        asset = user_asset(s, headers)
        print_header("THONG KE HIEN TAI", Colors.GREEN)
        
        total_games = stats["win"] + stats["lose"]
        win_rate = (stats["win"] / total_games * 100) if total_games > 0 else 0
        
        # Vẽ progress bar cho win rate
        bar_length = int(win_rate / 4)  # 100% = 25 ký tự
        bar = "█" * bar_length + "░" * (25 - bar_length)
        
        print_stats(f"So tran: {stats['win']} thang / {stats['lose']} thua")
        prints(Colors.YELLOW[0], Colors.YELLOW[1], Colors.YELLOW[2], 
               f"   Ty le thang: {win_rate:.1f}% [{bar}]")
        print_stats(f"Chuoi thang: {stats['streak']} (Max: {stats['max_streak']})")
        
        profit = asset[Coin] - stats['asset_0']
        if profit >= 0:
            print_money(f"Loi nhuan: +{profit:.2f} {Coin}", Coin)
        else:
            prints(Colors.RED[0], Colors.RED[1], Colors.RED[2], 
                   f"Loi nhuan: {profit:.2f} {Coin}")
        
        print_header("", Colors.GREEN)
    except Exception as e:
        print_error(f'Loi khi in thong ke: {e}')

def print_wallet(s, asset):
    print_header("THONG TIN VI", Colors.CYAN)
    
    # Vẽ progress bar cho số dư
    max_asset = max(asset.values()) if max(asset.values()) > 0 else 1
    
    for coin, amount in asset.items():
        if coin == "USDT":
            color = Colors.GREEN
        elif coin == "BUILD":
            color = Colors.YELLOW
        else:
            color = Colors.BLUE
        
        bar_length = int((amount / max_asset) * 25) if max_asset > 0 else 0
        bar = "█" * bar_length + "░" * (25 - bar_length)
        
        prints(color[0], color[1], color[2], 
               f"   {coin}: {amount:8.2f}  [{bar}]")
    
    print_header("", Colors.CYAN)

def bet_cdtd(s, headers, ki, list_kq, Coin, bet_amount):
    total_bet = 0
    print_betting(f"DAT CUOC KY #{ki}")
    
    for kq in list_kq:
        print_info(f"Dang dat {bet_amount} {Coin} cho {NV[kq]}")
        try:
            json_data = {
                'issue_id': int(ki),
                'bet_group': 'winner',
                'asset_type': Coin,
                'athlete_id': kq,
                'bet_amount': bet_amount,
            }
            response = s.post('https://api.sprintrun.win/sprint/bet', headers=headers, json=json_data).json()
            if response['code'] == 0 and response['msg'] == 'ok':
                print_success(f"Da dat {bet_amount} {Coin} vao {NV[kq]}")
                total_bet += bet_amount
            else:
                print_error(f'Loi dat cuoc {NV[kq]}: {response}')
        except Exception as e:
            print_error(f'Loi dat {Coin} cho {NV[kq]}: {e}')
    
    print_money(f"Tong cuoc: {total_bet} {Coin} cho {len(list_kq)} nhan vat", Coin)

def run_betting_thread(thread_name, nv_list, s, headers, coin, base_amount, heso):
    stats = {'win': 0, 'lose': 0, 'streak': 0, 'max_streak': 0, 'asset_0': 0}
    current_bet_amount = base_amount
    last_played_issue = -1
    
    # Lấy số dư ban đầu
    try:
        asset = user_asset(s, headers)
        stats['asset_0'] = asset[coin]
    except:
        pass
    
    # Hiển thị thông tin luồng
    nv_names = []
    for nv_id in nv_list:
        nv_names.append(NV[nv_id])
    nv_text = ", ".join(nv_names)
    
    print(f"\n[LUONG 1 BAT DAU - NHAN VAT: {len(nv_list)} NV]")
    for nv_id in nv_list:
        print(f"- {NV[nv_id]}")
    
    print(f"\n[LUONG 2 BAT DAU - NHAN VAT: {len(nv_list)} NV]")
    for nv_id in nv_list:
        print(f"- {NV[nv_id]}")
    
    print_header("", Colors.YELLOW)

    while True:
        try:
            # Lấy dữ liệu kỳ hiện tại
            data_top10 = top_10_cdtd(s, headers)
            latest_ki = int(data_top10[0][0])
            last_result = int(data_top10[1][0])

            # Kiểm tra kết quả của ván vừa đánh
            if last_played_issue == latest_ki:
                if last_result in nv_list:
                    print_success(f"[{thread_name}] THANG ky #{latest_ki}!")
                    stats['win'] += 1
                    stats['streak'] += 1
                    if stats['streak'] > stats['max_streak']:
                        stats['max_streak'] = stats['streak']
                    current_bet_amount = base_amount
                else:
                    print_error(f"[{thread_name}] THUA ky #{latest_ki}!")
                    stats['lose'] += 1
                    stats['streak'] = 0
                    current_bet_amount *= heso
                    print_warning(f"Cuoc moi: {current_bet_amount:.2f} {coin} (x{heso})")
                
                last_played_issue = -1

            # Đặt cược cho kỳ tiếp theo
            next_ki = latest_ki + 1
            if last_played_issue != next_ki:
                # Hiển thị thông tin đặt cược cho từng luồng
                if thread_name == "LUONG 1":
                    nv_names = []
                    for nv_id in nv_list:
                        nv_names.append(NV[nv_id])
                    nv_text = ", ".join(nv_names)
                    print(f"\nLUONG 1 DAT CUOC 3 NV: {nv_text}")
                else:
                    nv_names = []
                    for nv_id in nv_list:
                        nv_names.append(NV[nv_id])
                    nv_text = ", ".join(nv_names)
                    print(f"\nLUONG 2 DAT CUOC 3 NV: {nv_text}")
                
                bet_cdtd(s, headers, next_ki, nv_list, coin, current_bet_amount)
                last_played_issue = next_ki
                
                # Hiển thị thống kê nhanh
                total = stats['win'] + stats['lose']
                if total > 0:
                    win_rate = (stats['win'] / total) * 100
                    prints(Colors.CYAN[0], Colors.CYAN[1], Colors.CYAN[2], 
                           f"[{thread_name}] Win rate: {win_rate:.1f}% ({stats['win']}/{total})")

        except Exception as e:
            print_error(f"Loi tai {thread_name}: {e}")
        
        time.sleep(10)

def cdtd6nv():
    s = requests.Session()
    banner("CHAY DUA TOC DO - Ai la quan quan - 6 NHAN VAT")
    
    # Load dữ liệu
    data = load_data_cdtd()
    
    headers = {
        'accept': '*/*',
        'accept-language': 'vi,en;q=0.9',
        'cache-control': 'no-cache',
        'country-code': 'vn',
        'origin': 'https://xworld.info',
        'referer': 'https://xworld.info/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        'user-id': data['user-id'],
        'user-login': 'login_v2',
        'user-secret-key': data['user-secret-key'],
        'xb-language': 'vi-VN',
    }

    # Hiển thị số dư
    asset = user_asset(s, headers)
    print_wallet(s, asset)

    # Chọn loại tiền với UI đẹp
    print_header("CHON LOAI TIEN", Colors.YELLOW)
    prints(Colors.GREEN[0], Colors.GREEN[1], Colors.GREEN[2], "   1. USDT")
    prints(Colors.YELLOW[0], Colors.YELLOW[1], Colors.YELLOW[2], "   2. BUILD")
    prints(Colors.BLUE[0], Colors.BLUE[1], Colors.BLUE[2], "   3. WORLD")
    
    while True:
        prints(125, 255, 168, 'Nhap lua chon (1/2/3): ', end='')
        x = input().strip()
        if x in ['1', '2', '3']:
            Coin = 'USDT' if x == '1' else 'BUILD' if x == '2' else 'WORLD'
            break
        else:
            print_error('Sai dinh dang, vui long nhap lai!')

    # Nhập thông số cược
    print_header("CAU HINH CUOC", Colors.ORANGE)
    
    while True:
        try:
            bet_amount0 = float(input(f'Muc cuoc GOC cho moi NV ({Coin}): '))
            if bet_amount0 > 0:
                break
            print_error("Muc cuoc phai lon hon 0!")
        except ValueError:
            print_error("Vui long nhap so!")
    
    while True:
        try:
            heso = float(input('He so nhan khi thua (vi du: 2): '))
            if heso > 1:
                break
            print_error("He so phai lon hon 1!")
        except ValueError:
            print_error("Vui long nhap so!")

    clear_screen()
    banner('BOT DANG CHAY 2 LUONG')

    # === CHIA NHÂN VẬT: LUỒNG 1 RANDOM 3, LUỒNG 2 LẤY PHẦN CÒN LẠI ===
    all_nv = [1, 2, 3, 4, 5, 6]
    random.shuffle(all_nv)  # Xáo trộn danh sách
    
    # Luồng 1: lấy 3 nhân vật đầu tiên sau khi random
    thread1_nv = sorted(all_nv[:3])
    
    # Luồng 2: lấy 3 nhân vật còn lại
    thread2_nv = sorted(all_nv[3:])
    
    # Hiển thị thông tin cấu hình
    print_box("THONG TIN CAU HINH", Colors.CYAN)
    print_info(f"Loai tien: {Coin}")
    print_info(f"Cuoc goc: {bet_amount0} {Coin}")
    print_info(f"He so nhan: {heso}x")
    print()
    
    # Hiển thị phân chia luồng
    print_header("PHAN CHIA LUONG (RANDOM)", Colors.PURPLE)
    
    nv_names_1 = []
    for i in thread1_nv:
        nv_names_1.append(NV[i])
    nv_text_1 = ", ".join(nv_names_1)
    prints(Colors.PINK[0], Colors.PINK[1], Colors.PINK[2], f"   LUONG 1 (RANDOM): {nv_text_1}")
    
    nv_names_2 = []
    for i in thread2_nv:
        nv_names_2.append(NV[i])
    nv_text_2 = ", ".join(nv_names_2)
    prints(Colors.BLUE[0], Colors.BLUE[1], Colors.BLUE[2], f"   LUONG 2 (CON LAI): {nv_text_2}")
    
    print_header("", Colors.YELLOW)
    print_info("Bot dang chay... Nhan Ctrl+C de dung")
    print()

    # Khởi tạo 2 luồng
    t1 = threading.Thread(target=run_betting_thread, 
                          args=("LUONG 1", thread1_nv, s, headers, Coin, bet_amount0, heso))
    t2 = threading.Thread(target=run_betting_thread, 
                          args=("LUONG 2", thread2_nv, s, headers, Coin, bet_amount0, heso))

    t1.daemon = True
    t2.daemon = True
    
    t1.start()
    t2.start()

    # Giữ chương trình và hiển thị số dư định kỳ
    try:
        last_balance_check = time.time()
        while True:
            time.sleep(1)
            current_time = time.time()
            
            # Kiểm tra số dư mỗi 60 giây
            if current_time - last_balance_check >= 60:
                try:
                    current_asset = user_asset(s, headers)
                    if current_asset:
                        clear_screen()
                        print_header("CAP NHAT SO DU", Colors.GREEN)
                        print_wallet(s, current_asset)
                        
                        # Tính lợi nhuận
                        initial_asset = asset[Coin] if Coin in asset else 0
                        profit = current_asset[Coin] - initial_asset
                        if profit >= 0:
                            print_money(f"Loi nhuan: +{profit:.2f} {Coin}", Coin)
                        else:
                            prints(Colors.RED[0], Colors.RED[1], Colors.RED[2], 
                                   f"Loi nhuan: {profit:.2f} {Coin}")
                        
                        print_info("Bot van dang chay...")
                        last_balance_check = current_time
                except Exception as e:
                    print_error(f"Loi cap nhat so du: {e}")
                    
    except KeyboardInterrupt:
        print_header("DUNG BOT", Colors.RED)
        print_warning("Dang dung tat ca cac luong...")
        print_success("Da dung bot thanh cong!")
        print_info("Cam on ban da su dung tool!")
import sys
import platform
import os
import time
import re
import json
import asyncio
import aiohttp
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.align import Align
from rich import box
from rich.layout import Layout
from rich.live import Live

console = Console()
redeemed_or_exhausted_codes = set()
last_log_time = {}
user_claimed_history = {}
limit_reached_users = set()
system_logs = []

CODES_FILE = 'codes.txt'
CLAIM_STATS_FILE = 'claim_stats.json'
DAILY_LIMIT_PER_USER = 2
FILE_WATCH_INTERVAL = 5  # giây, khoảng thời gian quét lại codes.txt ở chế độ Full Auto
MAX_ATTACK_ROUNDS = 8  # số đợt bắn lại tối đa cho các TK bị lỗi tạm thời (get lock fail...) trên CÙNG 1 code trước khi chuyển code khác

HEADERS_INFO = {
    'accept': '*/*',
    'accept-language': 'vi,en;q=0.9',
    'content-type': 'application/json',
    'country-code': 'vn',
    'origin': 'https://xworld-app.com',
    'priority': 'u=1, i',
    'referer': 'https://xworld-app.com/',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'xb-language': 'vi-VN',
}

def clear_screen():
    os.system('cls' if platform.system() == "Windows" else 'clear')

def render_banner():
    text = Text("CANH CODE XWORLD AUTO FILTER", style="bold cyan", justify="center")
    panel = Panel(
        text,
        title="[bold yellow]✨ CANH CODE XWORLD AUTO FILTER ✨[/bold yellow]",
        subtitle="[bold green]ADMIN: HOANG NGUYEN | Zalo: 0965303727[/bold green]",
        border_style="bold magenta",
        box=box.DOUBLE_EDGE,
        padding=(1, 2)
    )
    console.print(panel)

# ─── ASYNC API CALLS ──────────────────────────────────────────────────────────

async def async_get_code_info(session, code):
    json_data = {'code': code, 'os_ver': 'android', 'platform': 'h5', 'appname': 'app'}
    try:
        async with session.post(
            'https://web3task.3games.io/v1/task/redcode/detail',
            headers=HEADERS_INFO,
            json=json_data,
            timeout=aiohttp.ClientTimeout(total=4)
        ) as resp:
            response = await resp.json(content_type=None)
        if response.get('code') == 0 and response.get('message') == 'ok':
            data = response.get('data', {})
            admin_data = data.get('data', {}).get('admin', {})
            return {
                'status': True,
                'total': data.get('user_cnt', 0),
                'used': data.get('progress', 0),
                'remaining': data.get('user_cnt', 0) - data.get('progress', 0),
                'currency': data.get('currency', 'UNK'),
                'value': admin_data.get('ad_show_value', 0),
                'name': admin_data.get('nick_name', 'Admin')
            }
        else:
            return {'status': False, 'message': response.get('message', 'Lỗi không xác định')}
    except Exception as e:
        return {'status': False, 'message': str(e)}

async def fetch_all_codes_info(codes):
    """Lấy thông tin toàn bộ danh sách code để kiểm tra ban đầu."""
    async with aiohttp.ClientSession() as session:
        tasks = [async_get_code_info(session, code) for code in codes]
        results = await asyncio.gather(*tasks)
        valid_data = []
        for code, res in zip(codes, results):
            if res.get('status'):
                res['code'] = code
                valid_data.append(res)
            else:
                console.print(f"[bold red]❌ Code '{code}' lỗi/không tồn tại: {res.get('message')}[/bold red]")
        return valid_data

async def async_nhap_code(session, userId, secretKey, code, max_retries=6, retry_delay=0.3):
    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'origin': 'https://xworld.info',
        'referer': 'https://xworld.info/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'user-id': userId,
        'user-secret-key': secretKey,
        'xb-language': 'vi-VN',
    }
    json_data = {'code': code, 'os_ver': 'android', 'platform': 'h5', 'appname': 'app'}

    # Các lỗi mang tính "tạm thời" từ server (lock bị giữ, quá tải...) -> nên thử lại
    TRANSIENT_ERROR_KEYWORDS = ["get lock fail", "lock fail", "timeout", "too many request", "server busy", "system busy"]

    last_error = "Unknown"
    for attempt in range(max_retries + 1):
        try:
            async with session.post(
                'https://web3task.3games.io/v1/task/redcode/exchange',
                headers=headers,
                json=json_data,
                timeout=aiohttp.ClientTimeout(total=4)
            ) as resp:
                response = await resp.json(content_type=None)
            if response.get('code') == 0 and response.get('message') == 'ok':
                val = response['data'].get('value', 0)
                curr = response['data'].get('currency', '')
                return True, f"SUCCESS|{userId}|{val}|{curr}"
            else:
                msg = response.get('message', 'Unknown')
                if "đạt đến giới hạn" in msg.lower() or "limit" in msg.lower():
                    return False, "LIMIT_REACHED"
                if "reward has been received" in msg.lower():
                    return False, "CLAIMED"
                if "not exist" in msg.lower() or "finish" in msg.lower():
                    return False, "EXHAUSTED"

                # Lỗi tạm thời (get lock fail, quá tải...) -> thử lại vài lần trước khi bỏ cuộc
                if any(kw in msg.lower() for kw in TRANSIENT_ERROR_KEYWORDS) and attempt < max_retries:
                    last_error = msg
                    await asyncio.sleep(retry_delay)
                    continue

                return False, msg
        except Exception as e:
            last_error = str(e)
            if attempt < max_retries:
                await asyncio.sleep(retry_delay)
                continue
            return False, last_error

    return False, f"{last_error} (đã thử lại {max_retries} lần)"

# ─── UI & INPUT ───────────────────────────────────────────────────────────────

def extract_codes_from_lines(lines):
    """Lọc sạch Icon & Link từ danh sách các dòng văn bản để lấy ra mã code.
    Xử lý theo từng dòng để không bị mất code khi 1 file/đoạn dán có lẫn cả link và code trần."""
    ignored_words = {"ngap", "tran", "code", "xworld", "global", "tat", "ca", "nguoi", "dung"}
    found_codes = []

    for line in lines:
        if not line.strip():
            continue

        # 1. Ưu tiên tìm code nếu dòng này là link dạng code=xxxx
        link_match = re.search(r'code=([a-zA-Z0-9]+)', line)
        if link_match:
            found_codes.append(link_match.group(1))
            continue

        # 2. Nếu không phải link, lọc icon/ký tự lạ ra lấy mã code trần
        clean_line = re.sub(r'[^a-zA-Z0-9]', '', line)

        if clean_line and clean_line.lower() not in ignored_words:
            # Code thường có độ dài từ 4 đến 15 ký tự
            if 4 <= len(clean_line) <= 15:
                found_codes.append(clean_line)

    # Lọc trùng lặp nhưng giữ nguyên thứ tự
    unique_codes = list(dict.fromkeys(found_codes))
    return unique_codes

def get_pasted_codes():
    """Nhận dữ liệu dán nhiều dòng từ người dùng, lọc sạch Icon & Link để lấy Code."""
    console.print(Panel(
        "[bold cyan]Dán văn bản, danh sách link hoặc danh sách code có Icon vào bên dưới.[/bold cyan]\n"
        "[bold yellow]👉 Sau khi dán xong, ấn Enter 2 lần để hệ thống tiến hành lọc code![/bold yellow]",
        title="[bold green]NHẬP DỮ LIỆU GIFTCODE[/bold green]", box=box.ROUNDED
    ))
    
    lines = []
    empty_lines_count = 0
    
    while True:
        try:
            line = input()
            if line.strip() == "":
                empty_lines_count += 1
                if empty_lines_count >= 1 and lines:
                    break
            else:
                empty_lines_count = 0
                lines.append(line)
        except (EOFError, KeyboardInterrupt):
            break

    return extract_codes_from_lines(lines)

def load_codes_from_file(path=CODES_FILE):
    """Đọc danh sách code/link đã chuẩn bị sẵn trong file (mỗi dòng 1 code hoặc 1 link)."""
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write("")
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = [ln.rstrip("\n") for ln in f.readlines()]
    return extract_codes_from_lines(lines)

def remove_code_from_codes_file(path, code):
    """Xóa dòng chứa code đã hết lượt ra khỏi file codes.txt để tránh canh lại code đã chết."""
    if not os.path.exists(path):
        return
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        kept_lines = []
        removed = False
        for line in lines:
            line_codes = extract_codes_from_lines([line.rstrip("\n")])
            if code in line_codes:
                removed = True
                continue
            kept_lines.append(line)

        if removed:
            with open(path, 'w', encoding='utf-8') as f:
                f.writelines(kept_lines)
    except Exception as e:
        add_system_log(f"Không thể xóa code '{code}' khỏi file '{path}': {e}", "bold red")


def display_account_table(user_ids):
    table = Table(title="[bold green]DANH SÁCH TÀI KHOẢN HIỆN CÓ[/bold green]", box=box.ROUNDED, header_style="bold cyan")
    table.add_column("STT", justify="center", width=5)
    table.add_column("User ID", justify="left", style="yellow")
    table.add_column("Trạng thái", justify="center", style="green")
    for idx, uid in enumerate(user_ids):
        table.add_row(str(idx + 1), uid, "Sẵn sàng")
    console.print(Align.center(table))

def display_code_info_table(valid_codes_data):
    table = Table(title="[bold magenta]DANH SÁCH CODE ĐÃ LỌC (SẮP XẾP SỐ LƯỢNG ÍT NHẤT LÊN ĐẦU)[/bold magenta]", box=box.HEAVY_HEAD, header_style="bold yellow")
    table.add_column("STT", justify="center", style="bold white", width=5)
    table.add_column("Mã Code", justify="center", style="cyan", width=15)
    table.add_column("Giá trị", justify="center", style="green")
    table.add_column("Đã dùng / Tổng", justify="center", style="white")
    table.add_column("Còn lại", justify="center", style="bold red")
    
    for idx, data in enumerate(valid_codes_data):
        table.add_row(str(idx + 1), data['code'], f"{data['value']} {data['currency']}", f"{data['used']} / {data['total']}", str(data['remaining']))
    
    console.print(Align.center(table))

def add_system_log(message, style="white"):
    time_str = time.strftime("%H:%M:%S")
    system_logs.append((f"[{time_str}] {message}", style))
    if len(system_logs) > 15:
        system_logs.pop(0)

def render_accounts_activity_table(user_ids, claim_stats):
    """Bảng nhật ký hoạt động: STT | User ID | Lượt đã nhập hôm nay (n/2) | Tổng đã nhận."""
    counts = claim_stats.get("counts", {})
    totals = claim_stats.get("totals", {})

    table = Table(box=box.SIMPLE, expand=True, header_style="bold cyan")
    table.add_column("STT", justify="center", width=4)
    table.add_column("User ID", justify="left", overflow="fold")
    table.add_column("Lượt hôm nay", justify="center")
    table.add_column("Tổng đã nhận", justify="right")

    for idx, uid in enumerate(user_ids):
        n = counts.get(uid, 0)
        total = totals.get(uid, 0)
        if uid in limit_reached_users or n >= DAILY_LIMIT_PER_USER:
            count_display = f"[bold red]{n}/{DAILY_LIMIT_PER_USER} (Full)[/bold red]"
        elif n > 0:
            count_display = f"[bold yellow]{n}/{DAILY_LIMIT_PER_USER}[/bold yellow]"
        else:
            count_display = f"[dim]{n}/{DAILY_LIMIT_PER_USER}[/dim]"
        table.add_row(str(idx + 1), uid, count_display, f"[bold green]{total:g}[/bold green]")

    return table

def render_dashboard(valid_codes_data, threshold, user_ids=None, claim_stats=None, mode_label="1 CODE"):
    user_ids = user_ids or []
    claim_stats = claim_stats or {"counts": {}, "totals": {}}

    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="tables", size=6),
        Layout(name="body")
    )
    layout["body"].split_row(
        Layout(name="accounts", ratio=1),
        Layout(name="logs", ratio=1)
    )
    header_text = Text(
        f"⚡ ĐANG AUTO CANH {mode_label} - NGƯỠNG TẤN CÔNG: {threshold} LƯỢT ⚡",
        style="bold white on red", justify="center"
    )
    layout["header"].update(Panel(header_text, box=box.ROUNDED))

    table = Table(box=box.SIMPLE, expand=True, header_style="bold cyan")
    table.add_column("MÃ CODE", justify="center")
    table.add_column("PHẦN THƯỞNG", justify="center")
    table.add_column("LƯỢT CÒN LẠI", justify="center")
    table.add_column("TRẠNG THÁI", justify="center")

    for data in valid_codes_data:
        rem = data['remaining']
        status = "[bold green]Đang theo dõi...[/bold green]" if rem > threshold else "[bold red]ĐANG TẤN CÔNG![/bold red]"
        if rem > threshold + 10:
            rem_display = f"[bold green]{rem}[/bold green]"
        elif rem > threshold:
            rem_display = f"[bold yellow]{rem}[/bold yellow]"
        else:
            rem_display = f"[bold red blink]{rem}[/bold red blink]"
        table.add_row(data['code'], f"{data['value']} {data['currency']}", rem_display, status)

    layout["tables"].update(Panel(table, title="[bold yellow]BẢNG THEO DÕI THỜI GIAN THỰC[/bold yellow]", box=box.ROUNDED))

    accounts_table = render_accounts_activity_table(user_ids, claim_stats)
    layout["accounts"].update(Panel(accounts_table, title="[bold magenta]NHẬT KÝ HOẠT ĐỘNG TÀI KHOẢN[/bold magenta]", box=box.ROUNDED, border_style="magenta"))

    log_text = Text()
    for msg, style in system_logs:
        log_text.append(f"{msg}\n", style=style)
    layout["logs"].update(Panel(log_text, title="[bold blue]NHẬT KÝ HỆ THỐNG[/bold blue]", box=box.ROUNDED, border_style="blue"))
    return layout

# ─── THỐNG KÊ LƯỢT NHẬP TRONG NGÀY (mỗi user 2 lượt/ngày) ─────────────────────

def load_claim_stats():
    today = time.strftime("%Y-%m-%d")
    stats = {"date": today, "counts": {}, "totals": {}}
    if os.path.exists(CLAIM_STATS_FILE):
        try:
            with open(CLAIM_STATS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            stats["totals"] = data.get("totals", {})
            # Chỉ giữ lại "counts" (số lượt hôm nay) nếu vẫn đúng ngày, sang ngày mới thì reset về 0
            if data.get("date") == today:
                stats["counts"] = data.get("counts", {})
        except Exception:
            pass
    return stats

def save_claim_stats(stats):
    try:
        with open(CLAIM_STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def bump_claim_count(stats, uid, kind, val=0.0):
    """Cập nhật số lượt đã nhập hôm nay + tổng đã nhận của 1 user, rồi lưu file."""
    counts = stats.setdefault("counts", {})
    totals = stats.setdefault("totals", {})
    current = counts.get(uid, 0)

    if kind == "SUCCESS":
        counts[uid] = min(current + 1, DAILY_LIMIT_PER_USER)
        totals[uid] = totals.get(uid, 0) + val
    elif kind == "CLAIMED":
        counts[uid] = min(current + 1, DAILY_LIMIT_PER_USER)
    elif kind == "LIMIT_REACHED":
        counts[uid] = DAILY_LIMIT_PER_USER

    save_claim_stats(stats)

# ─── DATA LOADING ─────────────────────────────────────────────────────────────

DATA_FILE = 'data_xw_confirm_code.txt'

def _doc_file_tk():
    ids, keys = [], []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if '|' in line:
                    parts = line.strip().split('|')
                    if len(parts) >= 2:
                        ids.append(parts[0])
                        keys.append(parts[1])
    return ids, keys

def _luu_file_tk(ids, keys):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        for i in range(len(ids)):
            f.write(f'{ids[i]}|{keys[i]}\n')

def _them_tai_khoan(ids, keys):
    try:
        num = int(Prompt.ask("[bold yellow]Nhập số lượng tài khoản cần thêm[/bold yellow]"))
    except:
        console.print("[red]Số lượng không hợp lệ![/red]")
        return
    for i in range(num):
        link = Prompt.ask(f"[bold white]Nhập link Vua thoát hiểm của tài khoản mới thứ {i+1}[/bold white]").strip()
        try:
            uid = link.split('?userId=')[1].split('&')[0]
            key = link.split('secretKey=')[1].split('&')[0]
            if uid in ids:
                console.print(f"[yellow]⚠ Tài khoản {uid} đã tồn tại, bỏ qua.[/yellow]")
                continue
            ids.append(uid)
            keys.append(key)
            console.print(f"[green]✔ Đã thêm tài khoản: {uid}[/green]")
        except:
            console.print("[bold red]❌ Link không hợp lệ, đã bỏ qua.[/bold red]")

def _xoa_tai_khoan_cu(ids, keys):
    if not ids:
        console.print("[yellow]Không có tài khoản nào để xóa.[/yellow]")
        return
    display_account_table(ids)
    sel = Prompt.ask("[bold yellow]Nhập STT tài khoản muốn xóa (nhiều STT cách nhau bởi dấu phẩy)[/bold yellow]")
    try:
        chi_so = sorted({int(x.strip()) - 1 for x in sel.split(',') if x.strip()}, reverse=True)
        for idx in chi_so:
            if 0 <= idx < len(ids):
                removed = ids.pop(idx)
                keys.pop(idx)
                console.print(f"[green]✔ Đã xóa tài khoản: {removed}[/green]")
            else:
                console.print(f"[red]STT {idx + 1} không hợp lệ.[/red]")
    except:
        console.print("[red]Nhập không hợp lệ![/red]")

def _thiet_lap_tai_khoan_moi(ids, keys):
    console.print(Panel("[bold cyan]THIẾT LẬP TÀI KHOẢN MỚI[/bold cyan]", box=box.ROUNDED))
    try:
        num = int(Prompt.ask("[bold yellow]Nhập số lượng tài khoản cần chạy[/bold yellow]"))
    except:
        console.print("[bold red]❌ Số lượng không hợp lệ.[/bold red]")
        return
    for i in range(num):
        link = Prompt.ask(f"[bold white]Nhập link Vua thoát hiểm của tài khoản {i+1}[/bold white]").strip()
        try:
            uid = link.split('?userId=')[1].split('&')[0]
            key = link.split('secretKey=')[1].split('&')[0]
            ids.append(uid)
            keys.append(key)
            console.print(f"[green]✔ Đã thêm tài khoản: {uid}[/green]")
        except:
            console.print("[bold red]❌ Link không hợp lệ, đã bỏ qua.[/bold red]")

def load_data_comfirm_codexw():
    user_ids = []
    user_secretkeys = []
    try:
        saved_ids, saved_keys = _doc_file_tk()

        if saved_ids:
            console.print(Panel(
                f"[yellow]Phát hiện {len(saved_ids)} tài khoản đã lưu trong file dữ liệu ({DATA_FILE}).[/yellow]",
                title="[bold blue]THÔNG TIN HỆ THỐNG[/bold blue]", box=box.ROUNDED
            ))
            user_ids, user_secretkeys = saved_ids, saved_keys

            while True:
                console.print(Panel(
                    "[bold cyan]1.[/bold cyan] Dùng tài khoản đã lưu\n"
                    "[bold cyan]2.[/bold cyan] Thêm tài khoản mới\n"
                    "[bold cyan]3.[/bold cyan] Xóa tài khoản cũ\n"
                    "[bold cyan]4.[/bold cyan] Xóa tất cả tài khoản",
                    title="[bold cyan]LỰA CHỌN TÀI KHOẢN[/bold cyan]", box=box.ROUNDED
                ))
                choice = Prompt.ask("[bold yellow]Chọn thao tác[/bold yellow]", choices=["1", "2", "3", "4"], default="1")

                if choice == "1":
                    if not user_ids:
                        console.print("[bold red]❌ Danh sách tài khoản trống, vui lòng thêm tài khoản mới.[/bold red]")
                        continue
                    console.print(f"[bold green]✅ Sử dụng {len(user_ids)} tài khoản đã lưu.[/bold green]\n")
                    display_account_table(user_ids)
                    break

                elif choice == "2":
                    _them_tai_khoan(user_ids, user_secretkeys)
                    _luu_file_tk(user_ids, user_secretkeys)
                    if user_ids:
                        display_account_table(user_ids)

                elif choice == "3":
                    _xoa_tai_khoan_cu(user_ids, user_secretkeys)
                    _luu_file_tk(user_ids, user_secretkeys)
                    if user_ids:
                        display_account_table(user_ids)

                elif choice == "4":
                    confirm = Prompt.ask(
                        "[bold red]Bạn chắc chắn muốn xóa TẤT CẢ tài khoản? (y/n)[/bold red]",
                        choices=["y", "n"], default="n"
                    )
                    if confirm.lower() == 'y':
                        user_ids.clear()
                        user_secretkeys.clear()
                        if os.path.exists(DATA_FILE):
                            os.remove(DATA_FILE)
                        console.print("[bold green]✅ Đã xóa toàn bộ dữ liệu tài khoản.[/bold green]")

        if not user_ids:
            _thiet_lap_tai_khoan_moi(user_ids, user_secretkeys)

        if user_ids:
            _luu_file_tk(user_ids, user_secretkeys)
            console.print("\n[bold green]✅ Đã lưu toàn bộ dữ liệu tài khoản vào file cấu hình.[/bold green]")
            display_account_table(user_ids)

        return user_ids, user_secretkeys
    except Exception as e:
        console.print(f"[bold red]❌ Lỗi hệ thống khi nhập liệu: {e}[/bold red]")
        sys.exit()

def print_summary(user_ids, claim_stats, reward_stats):
    counts = claim_stats.get("counts", {})
    totals = claim_stats.get("totals", {})

    table = Table(title="[bold green]📊 NHẬT KÝ HOẠT ĐỘNG TÀI KHOẢN[/bold green]", box=box.HEAVY_HEAD, header_style="bold cyan")
    table.add_column("STT", justify="center", width=5)
    table.add_column("User ID", style="yellow", no_wrap=True)
    table.add_column(f"Lượt đã nhập hôm nay (/{DAILY_LIMIT_PER_USER})", justify="center")
    table.add_column("Tổng đã nhận", justify="right", style="bold green")
    table.add_column("Chi tiết code đã nhập phiên này", style="white")

    for idx, uid in enumerate(user_ids):
        n = counts.get(uid, 0)
        total = totals.get(uid, 0)
        n_display = f"{n}/{DAILY_LIMIT_PER_USER}" + (" (Full)" if n >= DAILY_LIMIT_PER_USER else "")
        details = ""
        if uid in reward_stats:
            details = ", ".join([f"{d['code']} ({d['value']} {d['currency']})" for d in reward_stats[uid]['details']])
        table.add_row(str(idx + 1), uid, n_display, f"{total:g}", details)

    console.print(Panel(table, title="[bold blue]BÁO CÁO KẾT QUẢ[/bold blue]", box=box.DOUBLE_EDGE))

# ─── MAIN ASYNC LOOP ──────────────────────────────────────────────────────────

async def _reload_codes_from_file(session, codes_file, known_codes, valid_codes_order, valid_codes_data_map):
    """Đọc lại codes.txt, kiểm tra các code mới chưa từng thấy và thêm vào hàng đợi canh nếu còn hợp lệ."""
    try:
        file_codes = load_codes_from_file(codes_file)
    except Exception as e:
        add_system_log(f"Không đọc được file '{codes_file}': {e}", "bold red")
        return

    new_codes = [c for c in file_codes if c not in known_codes]
    if not new_codes:
        return

    for code in new_codes:
        known_codes.add(code)
        info = await async_get_code_info(session, code)
        if info.get('status') and info.get('remaining', 0) > 0:
            info['code'] = code
            valid_codes_data_map[code] = info
            valid_codes_order.append(code)
            last_log_time[code] = 0
            add_system_log(f"🆕 Phát hiện code mới từ file: '{code}' (Còn {info['remaining']} lượt). Thêm vào hàng đợi canh.", "bold green")
        elif info.get('status') and info.get('remaining', 0) <= 0:
            add_system_log(f"Code '{code}' từ file đã hết lượt sẵn. Xóa khỏi '{codes_file}'.", "yellow")
            remove_code_from_codes_file(codes_file, code)
        else:
            add_system_log(f"Code mới '{code}' từ file không hợp lệ/lỗi, bỏ qua (không xóa khỏi file).", "yellow")

async def run_monitor(user_ids, user_secretkeys, valid_codes_data_initial, threshold, reward_stats, claim_stats,
                       auto_mode=False, codes_file=CODES_FILE):
    # valid_codes_order: hàng đợi các code còn hợp lệ (chưa hết lượt) đang chờ canh
    valid_codes_order = [d['code'] for d in valid_codes_data_initial]
    valid_codes_data_map = {d['code']: d for d in valid_codes_data_initial}
    known_codes = set(valid_codes_order)
    mode_label = "FULL AUTO (LẦN LƯỢT TỪNG CODE ÍT LƯỢT NHẤT)" if auto_mode else "1 CODE DUY NHẤT"
    current_code = None  # Code đang được canh độc quyền; chỉ đổi sang code khác khi code này đã xong hẳn

    connector = aiohttp.TCPConnector(limit=0, ttl_dns_cache=300)
    async with aiohttp.ClientSession(connector=connector) as session:

        initial_dashboard = list(valid_codes_data_map.values())
        with Live(render_dashboard(initial_dashboard, threshold, user_ids, claim_stats, mode_label), refresh_per_second=10, screen=True) as live:
            last_file_watch = 0.0

            while True:
                # Ở chế độ Full Auto: định kỳ đọc lại codes.txt để nhận thêm code mới, không bao giờ tự dừng vì hết code
                if auto_mode and time.time() - last_file_watch > FILE_WATCH_INTERVAL:
                    await _reload_codes_from_file(session, codes_file, known_codes, valid_codes_order, valid_codes_data_map)
                    last_file_watch = time.time()

                if len(limit_reached_users) >= len(user_ids):
                    add_system_log("TẤT CẢ TÀI KHOẢN ĐÃ ĐẠT GIỚI HẠN NGÀY. HỆ THỐNG TỰ ĐỘNG DỪNG.", "bold red on white")
                    live.update(render_dashboard(list(valid_codes_data_map.values()), threshold, user_ids, claim_stats, mode_label))
                    await asyncio.sleep(3)
                    break

                if not valid_codes_order:
                    current_code = None
                    if auto_mode:
                        # Không dừng: tiếp tục chờ và quét file để lấy code mới
                        add_system_log(f"Chưa có code nào để canh. Đang chờ code mới từ '{codes_file}'...", "yellow")
                        live.update(render_dashboard([], threshold, user_ids, claim_stats, mode_label))
                        await asyncio.sleep(FILE_WATCH_INTERVAL)
                        continue
                    else:
                        add_system_log("Code đã cạn kiệt hoặc kết thúc. Dừng hệ thống.", "bold red")
                        live.update(render_dashboard([], threshold, user_ids, claim_stats, mode_label))
                        await asyncio.sleep(3)
                        break

                # Chỉ canh DUY NHẤT 1 code tại 1 thời điểm: nếu chưa có code nào đang canh (hoặc code
                # trước đó đã xong), chọn code có LƯỢT CÒN LẠI ÍT NHẤT trong hàng đợi. Nếu đang canh dở
                # 1 code thì giữ nguyên, không nhảy sang code khác cho đến khi code này xong hẳn.
                if current_code is None or current_code not in valid_codes_data_map:
                    current_code = min(valid_codes_order, key=lambda c: valid_codes_data_map[c]['remaining'])
                    add_system_log(f"🎯 Chọn canh code còn ÍT LƯỢT NHẤT: '{current_code}' (còn {valid_codes_data_map[current_code]['remaining']} lượt). Các code khác tạm gác lại.", "bold cyan")

                info = await async_get_code_info(session, current_code)

                if not info.get('status'):
                    add_system_log(f"Lỗi kiểm tra code '{current_code}': {info.get('message')}", "red")
                    await asyncio.sleep(0.3)
                    continue

                info['code'] = current_code
                valid_codes_data_map[current_code] = info
                current_dashboard_data = list(valid_codes_data_map.values())
                remaining = info['remaining']
                curr_time = time.time()

                eligible_users_indices = [
                    idx for idx, uid in enumerate(user_ids)
                    if uid not in limit_reached_users and current_code not in user_claimed_history[uid]
                ]

                if not eligible_users_indices:
                    active_users_count = len(user_ids) - len(limit_reached_users)
                    if active_users_count > 0:
                        add_system_log(f"Tất cả tài khoản đã nhận code '{current_code}'. Hoàn tất! Chuyển sang xét code khác.", "bold green")
                        valid_codes_order.remove(current_code)
                        valid_codes_data_map.pop(current_code, None)
                        current_code = None
                    await asyncio.sleep(0.5)
                    continue

                # Log định kỳ
                if curr_time - last_log_time.get(current_code, 0) > 0.5:
                    if remaining > threshold + 10:
                        add_system_log(f"Quét: {current_code} an toàn. Còn {remaining}/{info['total']} lượt.", "green")
                    else:
                        add_system_log(f"Quét: {current_code} BÁO ĐỘNG! Còn {remaining}/{info['total']} lượt.", "red")
                    last_log_time[current_code] = curr_time

                # Kích hoạt bắn code khi lượt <= threshold
                if remaining <= threshold and remaining > 0:
                    add_system_log(f"⚡ CODE '{current_code}' CÒN {remaining} LƯỢT! BẮN ĐỒNG LOẠT {len(eligible_users_indices)} TÀI KHOẢN!", "bold white on red")
                    live.update(render_dashboard(current_dashboard_data, threshold, user_ids, claim_stats, mode_label))

                    pending_indices = list(eligible_users_indices)
                    attack_round = 0
                    code_exhausted = False

                    # Bám đuổi (không chuyển sang code khác) cho đến khi:
                    # - toàn bộ TK đủ điều kiện đã được giải quyết (thành công/đã nhận/limit), hoặc
                    # - code chính thức hết lượt, hoặc
                    # - đã thử quá số đợt tối đa (tránh kẹt vô hạn nếu server lỗi liên tục)
                    while pending_indices and attack_round < MAX_ATTACK_ROUNDS:
                        attack_round += 1
                        if attack_round > 1:
                            add_system_log(f"🔁 Đợt {attack_round}: bắn lại {len(pending_indices)} TK còn lỗi/chưa xong cho code '{current_code}'...", "bold magenta")

                        tasks = [
                            asyncio.create_task(async_nhap_code(session, user_ids[idx], user_secretkeys[idx], current_code))
                            for idx in pending_indices
                        ]
                        results = await asyncio.gather(*tasks, return_exceptions=True)

                        still_pending = []
                        for idx, result in zip(pending_indices, results):
                            uid = user_ids[idx]
                            if isinstance(result, Exception):
                                add_system_log(f"[{uid}] Lỗi: {result} -> sẽ thử lại", "bold red")
                                still_pending.append(idx)
                                continue
                            success, msg = result
                            if success:
                                parts = msg.split('|')
                                if parts[0] == "SUCCESS":
                                    val = float(parts[2])
                                    curr = parts[3]
                                    if uid not in reward_stats:
                                        reward_stats[uid] = {'total': 0, 'details': []}
                                    reward_stats[uid]['total'] += val
                                    reward_stats[uid]['details'].append({'code': current_code, 'value': val, 'currency': curr})
                                    bump_claim_count(claim_stats, uid, "SUCCESS", val)

                                add_system_log(f"[{uid}] ✅ Cướp thành công! +{val} {curr}", "bold cyan")
                                user_claimed_history[uid].add(current_code)
                            else:
                                if msg == "CLAIMED":
                                    add_system_log(f"[{uid}] Đã nhận trước đó.", "dim white")
                                    user_claimed_history[uid].add(current_code)
                                    bump_claim_count(claim_stats, uid, "CLAIMED")
                                elif msg == "LIMIT_REACHED":
                                    add_system_log(f"[{uid}] Chạm giới hạn ngày! Khóa TK.", "bold red")
                                    limit_reached_users.add(uid)
                                    bump_claim_count(claim_stats, uid, "LIMIT_REACHED")
                                elif msg == "EXHAUSTED":
                                    add_system_log(f"[{uid}] Code hết lượt.", "bold red")
                                    code_exhausted = True
                                else:
                                    # Lỗi khác (vd get lock fail dù đã retry nội bộ) -> vẫn còn cơ hội, thử lại đợt sau
                                    add_system_log(f"[{uid}] Lỗi: {msg} -> sẽ thử lại", "bold red")
                                    still_pending.append(idx)

                        pending_indices = still_pending
                        live.update(render_dashboard(list(valid_codes_data_map.values()), threshold, user_ids, claim_stats, mode_label))

                        if code_exhausted or not pending_indices:
                            break

                        # Kiểm tra lại lượt còn lại trước khi bắn đợt tiếp theo
                        recheck = await async_get_code_info(session, current_code)
                        if recheck.get('status'):
                            recheck['code'] = current_code
                            valid_codes_data_map[current_code] = recheck
                            if recheck['remaining'] <= 0:
                                code_exhausted = True
                                break

                        await asyncio.sleep(0.25)

                    if pending_indices and attack_round >= MAX_ATTACK_ROUNDS:
                        add_system_log(f"⚠️ Đã bắn {MAX_ATTACK_ROUNDS} đợt cho code '{current_code}' nhưng vẫn còn {len(pending_indices)} TK lỗi. Chuyển sang quét code khác, sẽ quay lại sau.", "bold yellow")

                    final_check = await async_get_code_info(session, current_code)
                    if final_check['status'] and final_check['remaining'] <= 0:
                        add_system_log(f"Code '{current_code}' chính thức cạn lượt. Dừng canh code này.", "bold red")
                        if current_code in valid_codes_order:
                            valid_codes_order.remove(current_code)
                        valid_codes_data_map.pop(current_code, None)
                        if auto_mode:
                            remove_code_from_codes_file(codes_file, current_code)
                            add_system_log(f"🗑️ Đã xóa code '{current_code}' khỏi file '{codes_file}'.", "dim white")
                        current_code = None
                    else:
                        add_system_log(f"Code '{current_code}' còn {final_check.get('remaining', 0)} lượt. Tiếp tục giám sát.", "bold yellow")

                elif remaining <= 0:
                    add_system_log(f"Code '{current_code}' đã hết lượt (0). Dừng canh code này.", "bold red")
                    if current_code in valid_codes_order:
                        valid_codes_order.remove(current_code)
                    valid_codes_data_map.pop(current_code, None)
                    if auto_mode:
                        remove_code_from_codes_file(codes_file, current_code)
                        add_system_log(f"🗑️ Đã xóa code '{current_code}' khỏi file '{codes_file}'.", "dim white")
                    current_code = None

                live.update(render_dashboard(list(valid_codes_data_map.values()), threshold, user_ids, claim_stats, mode_label))
                await asyncio.sleep(0.05 if auto_mode else 0.01)

def canhcode():
    clear_screen()
    render_banner()

    user_ids, user_secretkeys = load_data_comfirm_codexw()
    if not user_ids:
        console.print("[bold red]❌ Không có tài khoản nào. Thoát.[/bold red]")
        return

    for uid in user_ids:
        user_claimed_history.setdefault(uid, set())

    claim_stats = load_claim_stats()

    console.print(Panel(
        "[bold cyan]1.[/bold cyan] Dán code/link thủ công (chọn 1 code duy nhất để canh)\n"
        f"[bold cyan]2.[/bold cyan] FULL AUTO - Đọc code từ file [yellow]{CODES_FILE}[/yellow] "
        "(canh nhiều code cùng lúc, tự động chạy liên tục, tự nhận thêm code mới thêm vào file)",
        title="[bold cyan]CHỌN CHẾ ĐỘ CHẠY[/bold cyan]", box=box.ROUNDED
    ))
    mode_choice = Prompt.ask("[bold yellow]Chọn chế độ[/bold yellow]", choices=["1", "2"], default="2")
    auto_mode = (mode_choice == "2")

    if auto_mode:
        if not os.path.exists(CODES_FILE):
            open(CODES_FILE, 'w', encoding='utf-8').close()
        extracted_codes = load_codes_from_file(CODES_FILE)
        if not extracted_codes:
            console.print(Panel(
                f"[yellow]File '{CODES_FILE}' hiện đang trống.[/yellow]\n"
                f"[white]Hãy mở file '{CODES_FILE}' và dán mỗi code (hoặc link chứa code=xxxx) trên 1 dòng, rồi lưu lại.[/white]",
                title="[bold red]CHƯA CÓ CODE[/bold red]", box=box.ROUNDED
            ))
            Prompt.ask("[bold yellow]Nhấn Enter sau khi đã lưu file để tiếp tục[/bold yellow]", default="")
            extracted_codes = load_codes_from_file(CODES_FILE)
    else:
        # Trích xuất danh sách code từ văn bản/link dán vào
        extracted_codes = get_pasted_codes()

    if not extracted_codes:
        console.print("[bold red]❌ Không tìm thấy mã code nào trong dữ liệu nhập. Thoát.[/bold red]")
        return

    console.print(f"\n[bold green]✔ Trích xuất thành công {len(extracted_codes)} mã code![/bold green]")
    console.print("[bold magenta]⏳ Đang phân tích thông tin code trên máy chủ...[/bold magenta]")

    valid_codes_data = asyncio.run(fetch_all_codes_info(extracted_codes))

    if not valid_codes_data:
        console.print("[bold red]❌ Tất cả các code vừa lọc đều không hợp lệ hoặc đã hết hạn. Thoát.[/bold red]")
        return

    # Sắp xếp code có lượt còn lại ít nhất lên đầu
    valid_codes_data.sort(key=lambda x: x['remaining'])

    console.print("\n")
    display_code_info_table(valid_codes_data)

    if auto_mode:
        # FULL AUTO: canh TẤT CẢ code hợp lệ (còn lượt) cùng lúc, không cần chọn STT
        valid_codes_data_initial = [d for d in valid_codes_data if d['remaining'] > 0]
        for d in valid_codes_data_initial:
            last_log_time[d['code']] = 0

        # Dọn luôn những code đã hết lượt sẵn ra khỏi file, tránh quét lại code chết mỗi lần chạy
        dead_codes = [d['code'] for d in valid_codes_data if d['remaining'] <= 0]
        for code in dead_codes:
            remove_code_from_codes_file(CODES_FILE, code)
        if dead_codes:
            console.print(f"[dim]🗑️ Đã dọn {len(dead_codes)} code hết lượt khỏi '{CODES_FILE}'.[/dim]")

        console.print(f"\n[bold green]✅ FULL AUTO: sẽ canh tất cả {len(valid_codes_data_initial)} code còn lượt, "
                       f"tự động đọc thêm code mới từ '{CODES_FILE}' mỗi {FILE_WATCH_INTERVAL}s.[/bold green]\n")
    else:
        # Cho phép người dùng chọn ĐÚNG 1 code để canh
        while True:
            try:
                stt_choice = int(Prompt.ask(f"[bold yellow]Nhập STT code bạn muốn chọn để canh (1 - {len(valid_codes_data)})[/bold yellow]"))
                if 1 <= stt_choice <= len(valid_codes_data):
                    selected_code_data = valid_codes_data[stt_choice - 1]
                    break
                else:
                    console.print(f"[red]STT không hợp lệ! Vui lòng chọn từ 1 đến {len(valid_codes_data)}.[/red]")
            except:
                console.print("[red]Vui lòng nhập số nguyên hợp lệ![/red]")

        console.print(f"\n[bold green]✅ Đã chọn canh duy nhất code: [bold cyan]{selected_code_data['code']}[/bold cyan] (Còn lại: {selected_code_data['remaining']} lượt)[/bold green]\n")

        valid_codes_data_initial = [selected_code_data]
        last_log_time[selected_code_data['code']] = 0

    console.print(Panel("[white]Ví dụ: Code có 300 lượt, muốn cướp khi còn 10 lượt → nhập 10.[/white]", box=box.MINIMAL))
    try:
        threshold = int(Prompt.ask("[bold yellow]Nhập ngưỡng lượt còn lại để kích hoạt cướp[/bold yellow]", default="5"))
    except:
        threshold = 5

    clear_screen()
    if auto_mode:
        add_system_log("Hệ thống FULL AUTO bắt đầu - canh nhiều code, chạy liên tục không dừng.", "bold cyan")
    else:
        add_system_log("Hệ thống bắt đầu quét API cực nhanh cho 1 code duy nhất.", "bold cyan")
    add_system_log(f"Tổng tài khoản: {len(user_ids)}", "cyan")

    reward_stats = {}

    try:
        asyncio.run(run_monitor(user_ids, user_secretkeys, valid_codes_data_initial, threshold, reward_stats,
                                 claim_stats, auto_mode=auto_mode, codes_file=CODES_FILE))
    except KeyboardInterrupt:
        clear_screen()
        console.print(Panel("[bold red]HỆ THỐNG ĐÃ ĐƯỢC DỪNG BỞI NGƯỜI DÙNG.[/bold red]", box=box.DOUBLE))
    finally:
        print_summary(user_ids, claim_stats, reward_stats)

def banner_chinh():
    clear_screen()
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     ██╗  ██╗██╗    ██╗ ██████╗ ██████╗ ██╗     ██████╗       ║
    ║     ╚██╗██╔╝██║    ██║██╔═══██╗██╔══██╗██║     ██╔══██╗      ║
    ║      ╚███╔╝ ██║ █╗ ██║██║   ██║██████╔╝██║     ██║  ██║      ║
    ║      ██╔██╗ ██║███╗██║██║   ██║██╔══██╗██║     ██║  ██║      ║
    ║     ██╔╝ ██╗╚███╔███╔╝╚██████╔╝██║  ██║███████╗██████╔╝      ║
    ║     ╚═╝  ╚═╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝       ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    prints(255, 215, 0, banner)
    prints(0, 255, 255, "\n" + "═" * 60)
    prints(255, 255, 0, "   ADMIN: HOANG NGUYEN | Zalo: 0965303727")
    prints(0, 255, 255, "═" * 60 + "\n")

def menu_chinh():
    prints(255, 255, 255, "\n" + "═" * 60)
    prints(255, 215, 0, "              🎯 CHỌN CÔNG CỤ BẠN MUỐN SỬ DỤNG")
    prints(255, 255, 255, "═" * 60)
    
    prints(50, 255, 50, "\n   ┌─────────────────────────────────────────────────────┐")
    prints(50, 255, 50, "   │  [1]  🏃 VUA THOÁT HIỂM - TỰ ĐỘNG ĐẶT CƯỢC          │")
    prints(50, 255, 50, "   │      ─────────────────────────────────────────      │")
    prints(50, 255, 50, "   │      Chơi game Vua thoát hiểm, tự động đặt          │")
    prints(50, 255, 50, "   │      cược theo chiến thuật Martingale               │")
    prints(50, 255, 50, "   └─────────────────────────────────────────────────────┘")
    
    prints(255, 215, 0, "\n   ┌─────────────────────────────────────────────────────┐")
    prints(255, 215, 0, "   │  [2]  🏎️ CHẠY ĐUA TỐC ĐỘ - 6 NHÂN VẬT                │")
    prints(255, 215, 0, "   │      ─────────────────────────────────────────      │")
    prints(255, 215, 0, "   │      Dự đoán người chiến thắng trong game           │")
    prints(255, 215, 0, "   │      Chạy đua tốc độ với 2 luồng song song          │")
    prints(255, 215, 0, "   └─────────────────────────────────────────────────────┘")
    
    prints(170, 0, 255, "\n   ┌─────────────────────────────────────────────────────┐")
    prints(170, 0, 255, "   │  [3]  🎁 CANH CODE - NHẬN QUÀ TỰ ĐỘNG               │")
    prints(170, 0, 255, "   │      ─────────────────────────────────────────      │")
    prints(170, 0, 255, "   │      Tự động canh và nhận giftcode từ               │")
    prints(170, 0, 255, "   │      XWorld, hỗ trợ nhiều tài khoản                 │")
    prints(170, 0, 255, "   └─────────────────────────────────────────────────────┘")
    
    prints(255, 100, 100, "\n   ┌─────────────────────────────────────────────────────┐")
    prints(255, 100, 100, "   │  [0]  🚪 THOÁT                                      │")
    prints(255, 100, 100, "   └─────────────────────────────────────────────────────┘")
    
    prints(255, 255, 255, "\n" + "═" * 60)

def main():
    # Khởi tạo colorama
    init(autoreset=True)
    
    while True:
        banner_chinh()
        menu_chinh()
        
        prints(255, 255, 0, "\n   📌 Nhập lựa chọn của bạn (0-3): ", end="")
        choice = input().strip()
        
        if choice == "1":
            prints(0, 255, 102, "\n   🔄 ĐANG KHỞI ĐỘNG VUA THOÁT HIỂM...")
            prints(255, 255, 0, "   ═" * 40)
            time.sleep(1)
            try:
                vth()
            except ImportError:
                prints(255, 0, 0, "   ❌ Không tìm thấy module Vua thoát hiểm!")
                prints(255, 255, 0, "   Nhấn Enter để tiếp tục...")
                input()
                
        elif choice == "2":
            prints(0, 255, 102, "\n   🔄 ĐANG KHỞI ĐỘNG CHẠY ĐUA TỐC ĐỘ...")
            prints(255, 255, 0, "   ═" * 40)
            time.sleep(1)
            try:
                cdtd6nv()
            except ImportError:
                prints(255, 0, 0, "   ❌ Không tìm thấy module Chạy đua tốc độ!")
                prints(255, 255, 0, "   Nhấn Enter để tiếp tục...")
                input()
                
        elif choice == "3":
            prints(0, 255, 102, "\n   🔄 ĐANG KHỞI ĐỘNG CANH CODE...")
            prints(255, 255, 0, "   ═" * 40)
            time.sleep(1)
            try:
                canhcode()
            except ImportError:
                prints(255, 0, 0, "   ❌ Không tìm thấy module Canh code!")
                prints(255, 255, 0, "   Nhấn Enter để tiếp tục...")
                input()
                
        elif choice == "0":
            prints(255, 100, 100, "\n   👋 CẢM ƠN BẠN ĐÃ SỬ DỤNG TOOL!")
            prints(255, 215, 0, "   ═" * 40)
            prints(255, 255, 0, "   🔗 Liên hệ: Zalo 0965303727")
            prints(255, 100, 100, "   ═" * 40)
            break
            
        else:
            prints(255, 0, 0, "\n   ❌ LỰA CHỌN KHÔNG HỢP LỆ!")
            prints(255, 255, 0, "   Vui lòng chọn 1, 2, 3 hoặc 0 để thoát.")
            prints(255, 255, 0, "   Nhấn Enter để tiếp tục...")
            input()

if __name__ == "__main__":
    import time
    main()
