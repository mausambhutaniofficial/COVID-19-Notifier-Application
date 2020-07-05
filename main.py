from tkinter import *
from PIL import Image, ImageTk
import requests
from bs4 import BeautifulSoup
import plyer
from tkinter import messagebox, filedialog
import pandas as pd

def scrape():   
    def notifier(title, msg):     
        plyer.notification.notify(
            title=title,
            message=msg,
            app_icon="images/icon.ico",
            timeout=20
        )
    url="https://www.worldometers.info/coronavirus/"
    r=requests.get(url)
    #print(r.text)
    soup=BeautifulSoup(r.content, 'html.parser')
    #print(soup.prettify())
    table_body=soup.find('tbody')
    #print(table_body)
    table_tr=table_body.find_all('tr')
    #print(table_tr)
    # for i in table_tr:
    #     id=i.find_all('td')
    #     print(id[1].text)         Actual country wise data
    #     #print(id[0].text,id[1].text,id[2].text)

    notify_country=countrydata.get()
    if notify_country=="":
        notify_country='india'


    #MAKING LISTS OF THE DATA WE GOT:-
    rank,countries, total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases= [], [], [], [], [], [], [], []
    serious, totalcases_permillion, totaldeaths_permillion, totaltests, totaltests_permillion= [], [], [], [], []
    headers=['rank','countries', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_recovered', 
    'active_cases','serious', 'totalcases_permillion', 'totaldeaths_permillion', 'totaltests', 
    'totaltests_permillion']

    for i in table_tr:
        id=i.find_all('td')
        if id[1].text.strip().lower() == notify_country:
            rank1=id[0].text.strip()
            totalcases1=int(id[2].text.strip().replace(",",""))
            totaldeaths1=id[4].text.strip()
            newcases1=id[3].text.strip()
            newdeaths1=id[5].text.strip()
            notifier(f"Coronavirus Updates in {notify_country.upper()}", f" Rank : {rank1}\n Total Confirmed Cases : {totalcases1}\n Total Deaths : {totaldeaths1}\n New Cases Today : {newcases1}\n New Deaths : {newdeaths1} ")
        rank.append(id[0].text.strip())
        countries.append(id[1].text.strip())
        total_cases.append(int(id[2].text.strip().replace(",","")))
        new_cases.append(id[3].text.strip())
        total_deaths.append(id[4].text.strip())
        new_deaths.append(id[5].text.strip())
        total_recovered.append(id[6].text.strip())
        active_cases.append(id[7].text.strip())
        serious.append(id[8].text.strip())
        totalcases_permillion.append(id[9].text.strip())
        totaldeaths_permillion.append(id[10].text.strip())
        totaltests.append(id[11].text.strip())
        totaltests_permillion.append(id[12].text.strip())

    df=pd.DataFrame(list(zip(rank,countries, total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases,serious, totalcases_permillion, totaldeaths_permillion, totaltests, totaltests_permillion)),columns=headers)
    sort=df.sort_values('total_cases', ascending=FALSE  )         
    for k in format_list:
        if k=='html':
            path2=f"{path}/alldata.html"
            sort.to_html(r'{}'.format(path2))

        if k=='csv':
            path2=f"{path}/alldata.csv"
            sort.to_csv(r'{}'.format(path2))

        if k=='json':
            path2=f"{path}/alldata.json"
            sort.to_json(r'{}'.format(path2))
            
    if len(format_list)!=0:
        messagebox.showinfo("Success", "Corona Details have been saved to your desired path", parent=root)
def download_data():     #browse files to select where to download on Submit button
    global path
    if (len(format_list)!=0):
        path=filedialog.askdirectory()
    else:
        pass
    scrape()
    format_list.clear()
    html.configure(state='normal')
    csv.configure(state='normal')
    json.configure(state='normal')

def inhtml():
    format_list.append('html')
    html.configure(state='disabled')


def incsv():
    format_list.append('csv')
    csv.configure(state='disabled')


def injson():
    format_list.append('json')
    json.configure(state='disabled')












root = Tk()
root.title("COVID-19 NOTIFIER APPLICATION")
root.geometry("728x450+340+100")
root.resizable(False,False)
root.config(bg="#fcb3b3")
root.wm_iconbitmap("images/icon.ico")

title=Label(root, text="World Coronavirus Live Notifier ", font=("trebuchet ms", 35, "italic bold"),bg="#fc8b8b")
title.place(x=0, y=0, height=90)

format_list=[]
path=""
#images
one=ImageTk.PhotoImage(Image.open("images/one.png"))
one_l=Label(root,image=one, bg="#fcb3b3")
one_l.place(x=50,y=90)

two=ImageTk.PhotoImage(Image.open("images/two.png"))
two_l=Label(root,image=two, bg="#fcb3b3")
two_l.place(x=220,y=90)

three=ImageTk.PhotoImage(Image.open("images/three.png"))
three_l=Label(root,image=three, bg="#fcb3b3")
three_l.place(x=390,y=90)

four=ImageTk.PhotoImage(Image.open("images/four.png"))
four_l=Label(root,image=four, bg="#fcb3b3")
four_l.place(x=560,y=90)


#Labels and entry boxes
notify=Label(root, text="Notify Country     :", font=("trebuchet ms", 17),bg="#fcb3b3") 
notify.place(x=20, y=220)

countrydata=StringVar()
entry=Entry(root, font=("trebuchet ms", 17),bg="#fc8b8b", bd=2, relief=GROOVE, textvariable=countrydata)
entry.place(x=230, y=220, width=280)


download=Label(root, text="Download Data in :", font=("trebuchet ms", 17),bg="#fcb3b3") 
download.place(x=20, y=270)

#Buttons
html=Button(root, text="HTML",command=inhtml, font=("trebuchet ms", 17),bg="#fc8b8b",relief=GROOVE,activebackground="#fc8b8b",cursor="hand2")
html.place(x=230, y=270, width=80, height=40)

csv=Button(root, text="CSV",command=incsv, font=("trebuchet ms", 17),bg="#fc8b8b",relief=GROOVE,activebackground="#fc8b8b",cursor="hand2")
csv.place(x=330, y=270, width=80, height=40)

json=Button(root, text="JSON",command=injson, font=("trebuchet ms", 17),bg="#fc8b8b",relief=GROOVE,activebackground="#fc8b8b",cursor="hand2")
json.place(x=430, y=270, width=80, height=40)


submit=Button(root, text="Submit",command=download_data, font=("trebuchet ms", 17),bg="#fc8b8b",relief=GROOVE,activebackground="#fc8b8b",cursor="hand2")
submit.place(x=170, y=370, width=280, height=40)

root.mainloop()