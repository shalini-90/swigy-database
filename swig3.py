import os 
import requests
import pandas as pd
from bs4 import BeautifulSoup 
import mysql 
import mysql.connector 


mydb = mysql.connector.connect( 
    host='localhost',
    user='root',
    password='#zecDATA12345',
    database='zom1'
    
    ) 
print(mydb.connection_id)
mycursor = mydb.cursor()  
mycursor.execute('show tables;')
print(mycursor.fetchall())

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
        # try:
        #     img = menu.find('img', attrs={"class":"styles_itemImage__3CsDL"})['src'] 
        #     img_li.append(img)
        #     print('img:', img) 
        # except: 
        #     img_li.append(0)
        #     print('No Image Found!') 

            # sql = "INSERT INTO restaurant_table(res_name varchar (200),descriptions_li varchar (200),dish_li text (10000),price_li float(5)) VALUES (%s)"      
        sql = "INSERT INTO restaurant_table(res_name,descriptions_li ,dish_li , price_li) VALUES (%s,%s,%s,%s)"
        val = [(str(restaurant))]
        query = f"INSERT INTO restaurant_table(res_name,descriptions_li ,dish_li , price_li) VALUES ('{res_name}', '{desc}', '{dish_name}', {price});"
        print('\n\n\n\t\tQUERY:\n', f'\t{query}\n\n') 
        try:
            mycursor.execute(query) 
        except: 
            pass
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
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
    
    df = pd.DataFrame.from_dict(zoo, orient='index')
    df = df.transpose()
    print(df.shape) 
    restore = [tuple(x) for x in df.values]
    print(restore)

    df.to_csv(f"RESTAURANTS/{res_name}.csv") 

get_restaurants_links() 