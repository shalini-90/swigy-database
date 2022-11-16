import os 
import requests
import pandas as pd
from bs4 import BeautifulSoup 

cd=[] 

def createFolder(directory): 
    try: 
        if not os.path.exists(directory): 
            os.makedirs(directory) 
    except OSError: 
        print ('Error: Creating directory.' + directory) 

def get_restaurants_links() :
    pg_no=1 
    while True: 
        res1=requests.get(f'https://www.swiggy.com/city/indore?page={pg_no}') 
        if res1.status_code != 200 :
            break 

        content = BeautifulSoup(res1.content, 'html.parser')  
        links=content.find_all('a',attrs={"class":"_1j_Yo"})
        for link in links[:5]: 
            # cd.append(link['href']) 
            restaurant = link['href']
            get_restaurant_data(restaurant) 
        pg_no+=1 
    # print(cd) 

def get_restaurant_data(restaurant):
    descriptions_li=[]
    dish_li=[] 
    price_li=[] 
    img_li=[]  
    print(f'\n\t Scrapping Menu for :{restaurant}\n')
    res1=requests.get(f'https://www.swiggy.com{restaurant}') 
    content = BeautifulSoup(res1.content, 'html.parser')
    menu_list = content.find_all('div',attrs={"class":"_2wg_t"})
    print('len(div):', len(menu_list))
    res_name = content.find('h1', attrs={"class":"_3aqeL"}).text.replace("/",' ')

    for menu in menu_list:
        desc = menu.find('p', attrs={"class":"ScreenReaderOnly_screenReaderOnly___ww-V"}).text 
        descriptions_li.append(desc)
        print('\ndesc:', desc)
        dish_name = menu.find('h3', attrs={"class":"styles_itemNameText__3ZmZZ"}).text
        dish_li.append(dish_name)
        print('dish_name:', dish_name)
        price = menu.find('span', attrs={"class":"rupee"}).text 
        price_li.append(price)
        print('price:', price) 
        try:
            img = menu.find('img', attrs={"class":"styles_itemImage__3CsDL"})['src'] 
            img_li.append(img)
            print('img:', img) 
        except: 
            img_li.append(0)
            print('No Image Found!') 
    get_csv(descriptions_li, dish_li, price_li, img_li, res_name)

def get_csv(descriptions_li, dish_li, price_li, img_li, res_name):
    zoo ={   
    "DESC" :descriptions_li,  
    "DISH": dish_li, 
    "PRICE":price_li, 
    "IMG": img_li
    }  
    if not zoo : 
        return  
    # print('********', zoo)
    df = pd.DataFrame.from_dict(zoo, orient='index')
    df = df.transpose()

    df.to_csv(f"RESTAURANTS/{res_name}.csv") 

createFolder('./RESTAURANTS/')   
get_restaurants_links() 

# ( _2OmLw    1 to 8 no. div ) ( _1FZ7A lh9t3    for div 1)  ( _1FZ7A    for div 2 and all upto 8) # regex


# url="https://www.swiggy.com/city/indore?page=1"

# req = requests.get(url)

# content = BeautifulSoup(req.content,'html.parser') 
# nm = []

# #for i in content.find_all('div',{"class":"_3FR5S"}):
#     #outside name,timing,price,rating 
# for i in content.find_all('div',{"class":"_3FR5S"}): 
#     name=i.find('div',attrs={"class":"nA6kb"}).text 
#     print(name)
#     # _3Mn31  • 
#     #overall rating,timing and pricing list
#     rating=i.find_all('div',attrs={"class":"_3Mn31"})
#     x = [h.text for  h in rating]
#     print(x[0].split('•')[0]) 
#     '''
#     y= [h.text for h in rating] 
#     print(y[0].split('•')[1]) 

#     z= [h.text for h in rating] 
#     print(z[0].split('•')[2]) 
#     ''' 
# inn=[]
#     # inner href 
# box=content.find_all('a',attrs={"class":"_1j_Yo"})
#    # print(box)
# for d in box:#.find_all('a', attrs={'href':("^/restaurants/")}):
    
#    # print(d.get('href')) 
#     inn.append(d.get('href'))
# print(inn) 

# for i,link in enumerate(inn):
#     if i<2: continue
# res=requests.get(f'https://www.swiggy.com{link}')

