#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import time
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

###########################################################################################################################
main_driver = webdriver.Chrome('C:\chromedriver.exe')

#boards = ['design','freebird','film','tech','art','leisure','citizen','local','sport','game','publish','traveling']
boards = ['freebird','film']
for board in boards:
    title_list=[]
    content_list=[]
    count=0
    for page in range(1,100):
        main_driver.get('https://www.flyingv.cc/categories/' +board+ '/all?status=success'+'&page='+str(page))
        time.sleep(2)
        error=0
        for x in range(12):
            try:
                tmp_title = main_driver.find_element_by_xpath('//*[@id="projects"]/div/div['+str(x+1)+']/div/div[3]/p[1]')
                #tmp_title = main_driver.find_element_by_xpath('//*[@id="projects"]/div/div['+str(x+1)+']/div/div[2]/p[1]')
                tmp_content = main_driver.find_element_by_xpath('//*[@id="projects"]/div/div['+str(x+1)+']/div/div[3]/p[3]')
                title_list.append(tmp_title.get_attribute('innerHTML'))
                content_list.append(tmp_content.get_attribute('innerHTML'))
                print(title_list[count])
                print(content_list[count])
                print('\n')
                count+=1
            except Exception as e:
                print(str(e))
                error+=1
        if error>10:
            break
    with open(board+'.csv', 'w', encoding = 'utf_8_sig', newline='') as result:
        awriter = csv.writer(result)
        awriter.writerow(['title'])
        for article in range(len(title_list)):
            list_a = []
            list_a.append(title_list[article])
            awriter.writerow(list_a)


# In[4]:


import csv
import jieba
import jieba.posseg as pseg

jieba.set_dictionary('dict.txt.txt')
for board in boards:
    with open(board + ".csv", "r", encoding="utf_8_sig" ) as csvFile:
        rows=csv.DictReader(csvFile, delimiter="\t")
        dictionary_title={'eng' : 0}
        dictionary_prob={'eng' : 0}
        document_num=0
        for row in rows:
            words=pseg.cut(row['title'])
            count=0
            length=0
            dictionary_temp={'eng' : 0}
            for word in words:
                if(word.flag!='x'):
                    length+=1
                ###統計該標題的各詞性出現次數###
                if(word.flag=='eng'):
                    dictionary_temp['eng']+=1
                elif(word.flag[0] not in dictionary_temp):
                    dictionary_temp[word.flag[0]] = 1
                else:
                    dictionary_temp[word.flag[0]] += 1
                ###統計開頭的字之詞性###
                if count==0 and word.flag!='x':
                    #print(word.word +" "+ word.flag)
                    count+=1
                    if(word.flag=='eng'):
                        dictionary_title['eng']+=1
                        #print('eng', " ", row['title'])
                    else:
                        if(word.flag[0] not in dictionary_title):
                            dictionary_title[word.flag[0]]=1
                            #print(word.flag, " ", row['title'])
                        else:
                            dictionary_title[word.flag[0]]+=1
                            #print(word.flag, " ", row['title'])
            ###更新dicitonary_prob的機率###
            for category in dictionary_temp:
                if(category!='x' and length!=0):
                    dictionary_temp[category]/=length
                    if(category not in dictionary_prob):
                        dictionary_prob[category]=dictionary_temp[category]
                    else:
                        dictionary_prob[category]+=dictionary_temp[category]
            if(length!=0):
                document_num+=1

    dictionary_title['others'] = 0  
    dictionary_prob['others'] = 0 
    temp_list = []
    temp = 0
    for category in dictionary_title:
        dictionary_title[category] = round(dictionary_title[category]/document_num, 2)
        if(dictionary_title[category] < 0.03 and category!='others'):
            dictionary_title['others']+=dictionary_title[category]
            temp_list.append(category)
            temp = dictionary_title['others']
    dictionary_title['others'] = round(temp, 2)
    for delete_item in temp_list:
        del dictionary_title[delete_item]

    temp_list = []
    for category in dictionary_prob:
        dictionary_prob[category] = round(dictionary_prob[category]/document_num, 2)
        if(dictionary_prob[category] < 0.03 and category!='others'):
            dictionary_prob['others']+=dictionary_prob[category]
            #print(dictionary_prob[category], " ", dictionary_prob['others'])
            temp_list.append(category)
            temp = dictionary_prob['others']
    dictionary_prob['others'] = round(temp, 2)
    for delete_item in temp_list:
        del dictionary_prob[delete_item]

    print("--------"+ board +"--------")
    ###標題開頭各詞性出現的機率###
    print("標題開頭各詞性出現的機率 : ", dictionary_title)
    ###標題內各詞性出現的機率###
    print("標題內各詞性出現的機率 : " ,dictionary_prob)
    print('\n')


# In[ ]:




