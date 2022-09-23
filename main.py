# -*- coding: utf-8 -*-
import requests 
from bs4 import BeautifulSoup
import time

model_id=219095 #需要自行填上 勇造ID 
area_id=60076   #需要自行填上 場外ID 
post_id=0000000 #需要自行填上 文章ID 

url="https://forum.gamer.com.tw/C.php?page="
area="&bsn="+str(area_id)
post="&snA="+str(post_id)


defaultFloor=1
cookie="" #需要自行填上
header={'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        ,'content-type':"application/x-www-form-urlencoded"
        ,'x-ua-compatible':'IE=edge'
        ,'cookie':cookie        
        }
id_array=[]
all_floor=0

res = requests.get(url+str(defaultFloor)+area+post,headers=header)
res.encoding="utf-8"
soup = BeautifulSoup(res.text, "lxml")

div=soup.find_all("a", class_="userid")
floor=soup.find_all('p',class_="BH-pagebtnA")
floor=floor[0].find_all('a')
all_floor=floor[len(floor)-1].next

for i in range(1,int(all_floor)+1):    
    
    defaultFloor=str(i)
    newUrl=url+defaultFloor+area+post   
    print(newUrl)    
    res = requests.get(newUrl,headers=header)
    res.encoding="utf-8"
    soup = BeautifulSoup(res.text, "lxml")
    div=soup.find_all("a", class_="userid")
    
    for i in div:
        if not i.next in id_array:
            id_array.append(i.next)    
    time.sleep(1)
print(id_array)
t = time.time()
csrf = requests.get("https://avatar1.gamer.com.tw/ajax/getCSRFToken.php?="+str(t),headers=header)


for i in id_array:
    userData ={"mode":2,"uid":i,"token":csrf.text}

    switchUser = requests.post("https://avatar1.gamer.com.tw/ajax/ch_user.php", data = userData,headers=header)

    if switchUser.text=="":
        print("搜尋到勇者:"+i)    
        time.sleep(0.5)
        url="https://avatar1.gamer.com.tw/ajax/incar.php?buynow=2&sn="+str(model_id)+"&token="+csrf.text
        getInCart = requests.get(url,headers=header)
        if getInCart.status_code==200 and getInCart.text=="已加入購物車": 
            print("成功加入購物車")
            print(getInCart.text)
            cart = requests.get("https://avatar1.gamer.com.tw/shopcar.php",headers=header)     
            time.sleep(0.5)
            if cart.status_code==200:
                print("購物車呼叫")
                soup = BeautifulSoup(cart.text, "lxml")
                token=soup.find("input",{"name":"token"})["value"]
                model_data=soup.find("input",{"name":"checkobj_"+str(model_id)})["value"]                              
                objName="checkobj_"+str(model_id)
                objData={"token":token,"checkobj[]":model_id,objName:model_data}
                cartSelect = requests.post("https://avatar1.gamer.com.tw/paybygold1.php", data = objData,headers=header)           
                time.sleep(0.5)
                if cartSelect.status_code==200:
                    print("商品選擇成功")
                    soup = BeautifulSoup(cartSelect.text, "lxml")
                    token=soup.find("input",{"name":"token"})["value"]                  
                    finalData={"token":token}                
                    cartBuy = requests.post("https://avatar1.gamer.com.tw/paybygold2.php", data = finalData,headers=header)
                    time.sleep(0.5)
                    if cartBuy.status_code==200:                    
                        #soup = BeautifulSoup(cartBuy.text, "lxml")
                        print("送禮成功")
                        #success=soup.find("p")
                        #print(success)
                    else:
                        print("送禮失敗")
                        print(cartBuy.text)
                        
                else:
                    print("商品選擇失敗")
                    
                    
                    
            
        else:
            print("勇者:"+i+"購物車加入失敗")
            print(getInCart.text)
     
    else:
        print("勇者id錯誤:"+i)
        


    









    

