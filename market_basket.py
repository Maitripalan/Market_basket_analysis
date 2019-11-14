from numpy import *
import csv

def loadDataSet():
    groceries = []
    cleaned_groceries = []
    with open('data1.csv', 'r', encoding='mac_roman', newline='') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            groceries.append(row)
    del(groceries[0])
    for item in groceries:
        #print(item)
        item = list(filter(None, item))
        del(item[0])
        cleaned_groceries.append(item)
    #print(cleaned_groceries)
    return cleaned_groceries
    
def oneItemset(dataset):
    oneItem = []
    for trans in dataset:
        for item in trans:
            if not [item] in oneItem:
                oneItem.append([item])
    oneItem.sort()
    #print("oneItemSet",oneItem)
    return list(map(frozenset,oneItem))#use frozen set so we can use it as a key in a dict

def scanD(dataset, one_item_set, minSupport):
    ssCnt = {}
    for trans in dataset:
        for can in one_item_set:
            if can.issubset(trans):
                if not can in ssCnt: 
                    ssCnt[can]=1
                else: 
                    ssCnt[can] += 1
    #print("ssCnt",ssCnt)
    supp_list = []
    supportData = {}
    for key in ssCnt:
        #print(len(dataset))
        support = (ssCnt[key]*100)/(len(dataset))
        #print("key/value",key, ssCnt[key] ,"support",round(support,2),'%')
        if support >= minSupport:
            supp_list.insert(0,key)
        supportData[key] = support
    #print(supportData,'--------key-------')
    #print(len(supportData)) list of all the unique items with its support value
    #print(len(supp_list))    list of all items above support 
    return supp_list,supportData

def setGen(Lk, k): 
    retList = []
    lenLk = len(Lk)
    #print(lenLk,'jjjjjjjjjjjjjjjj')
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            l1 = list(Lk[i])[:k-2]; l2 = list(Lk[j])[:k-2]
            l1.sort(); l2.sort()
            if l1==l2: 
                retList.append(Lk[i] | Lk[j]) #set union
    #print('qqqqqqqqqqqqqqqqqq',retList)
    return retList


min_support = int(input('Enter the required support threshold in percentage : '))
confidence = int(input('Enter the required confidence threshold in percentage : '))

data = loadDataSet()
OneItem = oneItemset(data)

D = list(map(set,data))
#print(D)
L1,suppData = scanD(D,OneItem,min_support)
#print(type(L1))

L = [L1]
#print(L)


k = 2
#print(len(L[k-2]))
#print(L[k-2])
while (len(L[k-2]) > 0):
    Ck = setGen(L[k-2], k)
    #print('ckkk',Ck)
    Lk, supK = scanD(D, Ck, min_support)
    suppData.update(supK)
    L.append(Lk)
    print(L,'--- printing L ')

    k += 1
    print('lkkk',Lk)

#print("Dataset :: -- ",L )
#print("-----",suppData)
#return L, supportData
#print(suppData)
#print(supportData)
