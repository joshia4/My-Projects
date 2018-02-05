#Importing required packages.
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import csv

#Fetching the web content and converting it to BeautifulSoup object.
response = requests.get("https://www.seed-db.com/accelerators")
txt = response.text
acc_soup = BeautifulSoup(txt, 'html.parser')
data = []

# Function to get the program IDs from seed-db.
def get_acc(soup):
    table=soup.find(id="accellist")
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols=row.find_all('td')
        counter=0

        for cols in row:
            try:
                cols.find('span')
            except NavigableString:
                pass
        col3=None
        col1=row.find('strong')
        links=row.find_all('a')
        links=[ele['href'] for ele in links]
        #print(links)
        if links:
            fu,col2=links[0].split("=")
            if len(links)==2:
                col3=links[1]
        
        data.append([col1.text.strip(),col2,col3])
    return data
get_acc(acc_soup)

#Converting the list returned by get_acc function to DataFrame.
print(type(data))
data = pd.DataFrame(data)
data


#function to fetch details from an accelorator

def get_details(id):
    temp= []
    response = requests.get("https://seed-db.com/accelerators/viewall?acceleratorid="+id)  
    txt = response.text
    soup = BeautifulSoup(txt, 'html.parser')
    table=soup.find(id="seedcos")
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    
    for row in rows:
        columns = row.find_all('td')
        temp.append(columns)
        
    finder = ['button','strong','a','span','span','span', 'span']
    for item in temp:
        for i in range(len(finder)+1):
            if i==(len(finder)):
                item.append(soup.find(itemprop = "name").get_text())
            elif i==1:
                a = item[i].find('a')
                link_text = a['href']
                bid = link_text.split("organization/")
                if(len(bid)==2):
                    item.append(bid[1])
                else:
                    item.append("None")
                item[i] = item[i].find(finder[i]).get_text()
            elif i==5 and item[i].find(finder[i]) is None:
                item[i] = item[i].get_text()    
            elif item[i].find(finder[i]) is None and i!=(len(finder)):
                item[i] = 'None'
            else:
                item[i] = item[i].find(finder[i]).get_text()
            
    return temp

#fetching data for all accelerators and writing it into a csv file
flag=0
for i in range(0,data.shape[0]):
    aid=str(data.loc[i,1]).strip()
    print("Parcing data for :", aid, "\n"  )
    value=get_details(aid)
    with open('accelorator_data.csv', 'a', newline='') as outfile:
        w = csv.writer(outfile)
        if flag==0:
            w.writerow(['State','Company Name', 'Website & Crunchbase Links', 'Cohort Date', 'Exit Value','Empty  Column', 'Funding','Crunchbase ID', 'Accelerator Name/Program'])
            flag=1
        for val in value:
            w.writerow(val)
