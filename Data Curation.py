
# coding: utf-8

# <h1> DATA CURATION PROJECT 
# <h2> Created by : Malhar Patwari <br><br>
# 

# <h3> import libraries

# In[3]:

#importing libraries

import pandas as pd
import csv
from collections import Counter
import requests
import geocoder
#import zipcode
from uszipcode import ZipcodeSearchEngine   #Install this library using !pip install uszipcode
from ast import literal_eval


# <h2> Input Data :

# In[65]:

# Getting data from CSV
data = pd.read_excel("Data.xlsx",dtype={'Zip':'str','Latitude':'str','Longitude':'str','Location':'str'}) #Note: read zip,lat,log in string
data.head()
#data['Zip'][data['Zip']=="nan"]
#print(data[data["Zip"].isnull()])
df = pd.DataFrame(data)
df['Zip'][df['Zip'] == 'nan'] = None
df['Latitude'][df['Latitude'] == 'nan'] = None
df['Longitude'][df['Longitude'] == 'nan'] = None
df['Location'][df['Location'] == 'nan'] = None
#df['Zip']=df['Zip'].astype(int)
#df['Zip'] = list(map(int,df['Zip']))
df[3785:3790]


# <h2> User Defined Functions for Google API and Edit distance

# In[19]:

#function to calculate edit distance between two strings
def edit(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    if s[-1] == t[-1]:
        cost = 0
    else:
        cost = 1
       
    res = min([edit(s[:-1], t)+1,
               edit(s, t[:-1])+1, 
               edit(s[:-1], t[:-1]) + cost])
    return res

def get_city_by_api(z):
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+z+"&sensor=true&key=AIzaSyC8UyUnx2LZn1jiSNIC4DPXfP3gtI2RUMY")
    r = r.json()
    if(r['status']=="OK"):
        a = r['results'][0]['address_components']
        for i in a:        
            if(i['types'][0]=="locality"):
                name= i['long_name']
                print("API USED")
                break
        name =name.lower()
        return name
    else:
        return "ERROR"

def get_state_by_api(z):
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+z+"&sensor=true&key=AIzaSyC8UyUnx2LZn1jiSNIC4DPXfP3gtI2RUMY")
    r = r.json()
    if(r['status']=="OK"):
        a = r['results'][0]['address_components']
        for i in a:        
            if(i['types'][0]=="administrative_area_level_1"):
                name= i['short_name']
                print("API USED")
                break
        name =name.upper()
        return name
    else:
        return "ERROR"

def get_city_by_api_loc(lat,log):
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng="+lat+","+log+"&sensor=true&key=AIzaSyC8UyUnx2LZn1jiSNIC4DPXfP3gtI2RUMY")
    r = r.json()
    if(r['status']=="OK"):
        a = r['results'][0]['address_components']
        for i in a:        
            if(i['types'][0]=="locality"):
                name= i['long_name']
                print("API USED")
                break
        name =name.lower()
        return name
    else:
        return "ERROR"

def get_state_by_api_loc(lat,log):
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng="+lat+","+log+"&sensor=true&key=AIzaSyC8UyUnx2LZn1jiSNIC4DPXfP3gtI2RUMY")
    r = r.json()
    if(r['status']=="OK"):
        a = r['results'][0]['address_components']
        for i in a:        
            if(i['types'][0]=="administrative_area_level_1"):
                name= i['short_name']
                print("API USED")
                break
        name =name.upper()
        return name
    else:
        return "ERROR"
    
def get_zip_by_api_loc(lat,log):
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng="+lat+","+log+"&sensor=true&key=AIzaSyC8UyUnx2LZn1jiSNIC4DPXfP3gtI2RUMY")
    r = r.json()
    if(r['status']=="OK"):
        a = r['results'][0]['address_components']
        for i in a:        
            if(i['types'][0]=="postal_code"):
                name= i['long_name']
                print("API USED")
                break        
        return name
    else:
        return "ERROR"    
    
def get_zip_by_api(add):
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+add+"&sensor=true&key=AIzaSyC8UyUnx2LZn1jiSNIC4DPXfP3gtI2RUMY")
    r = r.json()
    if(r['status']=="OK"):
        a = r['results'][0]['address_components']
        for i in a:        
            if(i['types'][0]=="postal_code"):
                name= i['long_name']
                print("API USED")
                break        
        return name
    else:
        return "ERROR"
    
def get_latitude_by_api(add):
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+add+"&sensor=true&key=AIzaSyC8UyUnx2LZn1jiSNIC4DPXfP3gtI2RUMY")
    r = r.json()
    if(r['status']=="OK"):
        a = r['results'][0]['geometry']['location']['lat']
        a = str(a)
        print(a)
        return a
    else:
        return "ERROR"
    
def get_longitude_by_api(add):
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+add+"&sensor=true&key=AIzaSyC8UyUnx2LZn1jiSNIC4DPXfP3gtI2RUMY")
    r = r.json()
    if(r['status']=="OK"):
        a = r['results'][0]['geometry']['location']['lng']
        a = str(a)
        print(a)
        return a
    else:
        return "ERROR"

def get_add_by_api_loc(lat,log):
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng="+lat+","+log+"&sensor=true&key=AIzaSyC8UyUnx2LZn1jiSNIC4DPXfP3gtI2RUMY")
    r = r.json()
    if(r['status']=="OK"):
        a = r['results'][0]['address_components']
        for i in a:            
            if(i['types'][0] == "street_number"):
                street_num = i['long_name']
            if(i['types'][0] == "route"):
                route = i['long_name']
            if(i['types'][0] == "neighborhood"):
                neighborhood = i['long_name']    
        name= street_num + " " + route + " " + neighborhood       
        return name        
        
    else:
        return "ERROR"   


# <h2>Replacing Null values on "Inspection Id" attribute

# In[23]:

# Null error detection for Inspectionid: 

print("all null value indices:")
null_index_inspec = df[df['Inspection ID'].isnull()].index
print(null_index_inspec)

#if duplicated values then replace ids with 0
df['Inspection ID'][df['Inspection ID'].duplicated()] = 0

#replacing nulls with 0
for i in null_index_inspec:
    df['Inspection ID'][i] = 0
        
        
print("all null values must be replaced")       


# <h2> Replacing Null values on "License#" attribute

# In[25]:

# Null error detection for License#: 
print("All null value indices")
null_index_license = df[df['License #'].isnull()].index
print(null_index_license)

#Replacing nulls with 0
for i in null_index_license:
    df['License #'][i] = 0


# <h2> Replacing Null values on Inspection Date and Inspection Type

# In[9]:

# Null error detection for Inspection date and Inspection Type: 
null_index_indate = df[df['Inspection Date'].isnull()].index
print(null_index_indate)

null_index_intype = df[df['Inspection Type'].isnull()].index
print(null_index_intype)

#Replacing nulls in Inspection date and type with "NA"
for i in null_index_indate:
    df['Inspection Date'][i] = "NA"
for i in null_index_intype:
    df['Inspection Type'][i] = "NA"    


# <h2> Replacing Null values on Results attribute

# In[27]:

# Null error detection for Results: 
null_index_result = df[df['Results'].isnull()].index
print(null_index_result)

#Replacing nulls in results with "No Entry"
for i in null_index_result:
    df['Results'][i] = "No Entry"


# <h2> Replacing Null Values on Violations attribute

# In[12]:

# Null error detection for Violations: 
null_index_violations = df[df['Violations'].isnull()].index
print(null_index_violations)

#Replacing nulls in results with "NA"
for i in null_index_violations:
    df['Violations'][i] = "NA"


print(df['Violations'][null_index_violations])


# <h2> Replacing Nulls on "Risk" Attribute

# In[30]:

# detecting nulls in Risk field
null_index_risk = df[df['Risk'].isnull()].index
print(null_index_risk)

#removal of nulls with "NA" for risk
for i in null_index_risk:
    df['Risk'][i] = "NA"

df['Risk'][null_index_risk]


# <h2> Replacing Nulls on "Facility Type" attribute 

# In[34]:

#error 2 detection for Facility types
null_index_facility = df[df['Facility Type'].isnull()].index
print(null_index_facility)
#df[45:50]

#Solve Nulls for Facility Type
for i in null_index_facility:    
    if(df['DBA Name'][i]!=None):                        
        Dname = df['DBA Name'][i]
        #print(Dname)
        li = df[df['DBA Name'] == Dname].index
        #print(li)
        if(len(li)==1):  # this is if the dba name is unique
            df['Facility Type'][i] = "NA"
        else:            #this is if DBA name is not unique i.e. it is a new name
            all_names = df['Facility Type'][li]
            all_names_set = set(all_names)
            print(all_names_set)
            if((len(all_names_set) == 1)and(next(iter(all_names_set))!=None)):    #if all has same facility type
                df['Facility Type'][i] = all_names_set.pop()
            else:                           #if different facility types
                c = Counter(all_names)
          #      print(c)
                if(c.most_common()[0][1] >int(len(li)/2)):   # 50% enough frequency to assign facility type
                    df['Facility Type'][i] = c.most_common()[0][0]
                else:                        #not enough frequency so assign its own dba name 
                    df['Facility Type'][i] = "NA"
    else:
        df['Facility Type'][i]="NA"

df['Facility Type'][df['Facility Type'].isnull()] = "NA" #this will replace all remaining nulls with "NA"

print("ALL NULL Values are REPLACED")
#all null solved for Facility in df.
df['Facility Type'][null_index_facility]


# <h2> Replacing Null Values on Attribute DBA Name

# In[36]:

# Null error detection for DBA Name: 


null_index_dba = df[df['DBA Name'].isnull()].index
print(null_index_dba)


#Solve Nulls for DBA Names 
for i in null_index_dba:
    if(df['AKA Name']!= None):
        Aname = df['AKA Name'][i]
        #print(Aname)
        li = df[df['AKA Name'] == Aname].index
        print(li)
        if(len(li)==1):  # this is if the AKA name is unique
            df['DBA Name'][i] = df['AKA Name'][i]
        else:            #this is if AKA name is not unique
            all_names = df['DBA Name'][li]
            all_names_set = set(all_names)
            print(all_names_set)
            if((len(all_names_set) == 1)and(next(iter(all_names_set))!=None)):    #if all has same aka name            
                df['DBA Name'][i] = all_names_set.pop()
            else:                           #if different dba names
                c = Counter(all_names)
                print(c)
                if(c.most_common()[0][1] >int(len(li)/2)):   # 50% enough frequency to assign aka name
                    df['DBA Name'][i] = c.most_common()[0][0]
                else:                        #not enough frequency so assign its own aka name 
                    df['DBA Name'][i] = df['AKA Name'][i]
    else:
        df['DBA Name'][i] = "NA"

df['DBA Name'][df['DBA Name'].isnull()] = df['AKA Name'][df['DBA Name'].isnull()] #This will replace all null with its DBA name
#df[1214:1216]
print("All nulls have been replaced")
#all null solved for DBA Names in df.
df[df['DBA Name'].isnull()]


# <h2> Replacing all Null values on AKA Name

# In[37]:

#TASK1 Null error detection for AKA Name: 

null_index = df[df['AKA Name'].isnull()].index
print(null_index)
    

#Solve Nulls for AKA Names 
for i in null_index:
    if(df['DBA Name'][i]!=None):
        if(df['DBA Name'][i]=="NA"):
            df['AKA Name'][i] = "NA"
        else:
            Dname = df['DBA Name'][i]
            #print(Dname)
            li = df[df['DBA Name'] == Dname].index
            #print(li)
            if(len(li)==1):  # this is if the dba name is unique
                df['AKA Name'][i] = df['DBA Name'][i]
            else:            #this is if DBA name is not unique
                all_names = df['AKA Name'][li]
                all_names_set = set(all_names)
                #print(all_names_set)
                if((len(all_names_set) == 1)and(next(iter(all_names_set))!=None)):    #if all has same dba name            
                    df['AKA Name'][i] = all_names_set.pop()
                else:                           #if different dba names
                    c = Counter(all_names)
                    #print(c)
                    if(c.most_common()[0][1] >int(len(li)/2)):   # 50% enough frequency to assign dba name
                        df['AKA Name'][i] = c.most_common()[0][0]
                    else:                        #not enough frequency so assign its own dba name 
                        df['AKA Name'][i] = df['DBA Name'][i]
    else:
        df['AKA Name'][i] = "NA"

df['AKA Name'][df['AKA Name'].isnull()] = df['DBA Name'][df['AKA Name'].isnull()] #This will replace all null with its DBA name
df[1214:1216]
print("All Nullsa have been replaced")
#all null solved for AKA Names in df.
df["AKA Name"][null_index]


# <h2>Replacing all Nulls on Address Attribute

# In[38]:

# detection for Address
null_index_add = df[df['Address'].isnull()].index
print(null_index_add)


for i in null_index_add:
    if((df['Latitude'][i]!=None)and(df['Longitude'][i]!=None)):            #This if is to identify on basis of lat andlog
        lat = df['Latitude'][i]
        log = df['Longitude'][i]       
        a = get_add_by_api_loc(lat,log) #uses google api to get City
        if(a=="ERROR"):
            print("ERROR OCCURED FROM GOOGLEAPI")
            df['Address'][i] = "NA"
        else:
            df['Address'][i] = a
            print(df['Address'][i])
            print("Used Google API")
    else:                                                                 #if not location, put NA instead
        df['Address'][i] = "NA"
        
print("ALL Address attribute values have been replaced")        
#show null addresses 
df['Address'][null_index_add]


# <h2> Replacing all Nulls on City Attribute

# In[69]:

# detection for City
null_index_City = df[df['City'].isnull()].index
print(null_index_City)

#Error4 removing nulls from city
search = ZipcodeSearchEngine()

for i in null_index_City:
    
    if(df['Zip'][i]!= None):   #This if is to identify on basis of zipcode
        zzip = df['Zip'][i] 
        #print(zzip)        
        #print(i)
        li = list(df[df['Zip'] == zzip].index)
        #print(li)
        li.remove(i)
        #print(li)   
        
        if(li == None):  # this is if the zip is unique
            if(((search.by_zipcode(zzip)).City)!= None):
                df['City'][i] = ((search.by_zipcode(zzip)).City).lower() #this will assign city using library
                #print(df['City'][i])
                print("Successsful")
            else:
                a = get_city_by_api(zzip) #uses google api to get City
                if(a=="ERROR"):
                    print("ERROR OCCURED FROM GOOGLEAPI")
                    df['City'][i] = "NA"
                else:
                    df['City'][i] = a
                  #  print(df['City'][i])
                    print("Used Google API")
                    
        else:                                           #this is if zip is not unique
            all_names = df['City'][li]
            all_names_set = set(all_names)
         #   print(all_names_set)
            if((len(all_names_set) == 1)and(next(iter(all_names_set))!=None)):    #if all has same City
                df['City'][i] = all_names_set.pop()
            else:                           #if different City
                if(((search.by_zipcode(zzip)).City)!= None):
                    df['City'][i] = ((search.by_zipcode(zzip)).City).lower() #this will assign city using library                
                else:
                    a = get_city_by_api(zzip) #uses google api to get City
                    if(a=="ERROR"):
                        print("ERROR OCCURED FROM GOOGLEAPI")
                        df['City'][i] = "NA"
                    else:
                        df['City'][i] = a
                        
    elif((df['Latitude'][i]!=None)and(df['Longitude'][i]!=None)):            #This if is to identify on basis of lat andlog
        lat = df['Latitude'][i]
        log = df['Longitude'][i]       
        a = get_city_by_api_loc(lat,log) #uses google api to get City
        if(a=="ERROR"):
            print("ERROR OCCURED FROM GOOGLEAPI")
            df['City'][i] = "NA"
        else:
            df['City'][i] = a
            print(df['City'][i])
            print("Used Google API")  
            
    elif(df['Address'][i]!=None):            #This if is to identify on basis of Address
        add = df['Address'][i] 
        print(add)
        li = list(df[df['Address'] == add].index)
        li.remove(i)
        print(li)
        if(li == None):  # this is if the Address is unique
            a = get_city_by_api(add) #uses google api to get City
            if(a=="ERROR"):
                print("ERROR OCCURED FROM GOOGLEAPI")
                df['City'][i] = "NA"
            else:
                df['City'][i] = a
                print(df['City'][i])
                print("Used Google API")
                
        else:                                           #this is if Address is not unique
            all_names = df['City'][li]
            all_names_set = set(all_names)
            print(all_names_set)
            if((len(all_names_set) == 1)and(next(iter(all_names_set))!=None)):    #if all has same City
                df['City'][i] = all_names_set.pop()
            else:                           #if different City
                a = get_city_by_api(add) #uses google api to get City
                if(a=="ERROR"):
                    print("ERROR OCCURED FROM GOOGLEAPI")
                    df['City'][i] = "NA"
                else:
                    df['City'][i] = a
                    
    else:
        print("No data is there on the basis of which city can be found")
        print("So putting NA as a City")
        df['City'][i] = "NA"



#see all remaining nulls in city
#df[2001:2015]
df[df['City'].isnull()]


# <h2> Used edit distance to replacing Typos in City Attribute

# In[71]:

#Convert characters into lower case
df['City']=[str(x).lower() for x in df['City']]

# first clean data using edit distance to clean any typos in City.

for i in df['City'].index:    
    if(df['City'][i] != "chicago"):
        if(edit(df['City'][i],"chicago")<3):            
            df['City'][i]="chicago"
        else:            
            continue
    else:
        continue
df['City'].unique()


df[df['City'].isnull()]


# <h2>Replacing all Nulls on State Attribute

# In[42]:

#error5 detection for State
null_index_State = df[df['State'].isnull()].index
print(null_index_State)

#Error5 removing nulls from State
search = ZipcodeSearchEngine()

for i in null_index_State:
    
    if(df['Zip'][i]!= None):   #This if is to identify on basis of zipcode
        zzip = df['Zip'][i] 
        #print(zzip)        
        #print(i)
        li = list(df[df['Zip'] == zzip].index)
        #print(li)
        li.remove(i)
        #print(li)   
        if(li == None):  # this is if the zip is unique
            if(((search.by_zipcode(zzip)).State)!= None):     #if library has answer
                df['State'][i] = ((search.by_zipcode(zzip)).State).upper()    #this will assign State using library
                #print(df['State'][i])
                print("Successsful")
            else:                                             #if library has no answer
                a = get_state_by_api(zzip) #uses google api to get State
                if(a=="ERROR"):
                    print("ERROR OCCURED FROM GOOGLEAPI")
                    df['State'][i] = "NA"
                else:
                    df['State'][i] = a
                 #   print(df['State'][i])
                    print("Used Google API")
        else:                                           #this is if zip is not unique
            all_names = df['State'][li]
            all_names_set = set(all_names)
          #  print(all_names_set)
            if((len(all_names_set) == 1)and(next(iter(all_names_set))!=None)):    #if all has same City
                df['State'][i] = all_names_set.pop()
            else:                           #if different City
                if(((search.by_zipcode(zzip)).State)!= None):
                    df['State'][i] = ((search.by_zipcode(zzip)).State).upper()    #this will assign city using library                
                else:
                    a = get_state_by_api(zzip) #uses google api to get City
                    if(a=="ERROR"):
                        print("ERROR OCCURED FROM GOOGLEAPI")
                        df['State'][i] = "NA"
                    else:
                        df['State'][i] = a
                        
    elif(df['City'][i]!=None):            #This if is to identify on basis of City
        city = df['City'][i] 
       # print(city)
        li = list(df[df['City'] == city].index)
        li.remove(i)
       # print(li)
        if(li == None):  # this is if the City is unique
            a = get_state_by_api(city) #uses google api to get State
            if(a=="ERROR"):
                print("ERROR OCCURED FROM GOOGLEAPI")
                df['State'][i] = "NA"
            else:
                df['State'][i] = a
                print(df['State'][i])
                print("Used Google API")
        else:                                           #this is if City is not unique
            all_names = df['State'][li]
            all_names_set = set(all_names)
        #    print(all_names_set)
            if((len(all_names_set) == 1)and(next(iter(all_names_set))!=None)):    #if all has same State
                df['State'][i] = all_names_set.pop()
            else:                           #if different State
                a = get_state_by_api(city) #uses google api to get State
                if(a=="ERROR"):
                    print("ERROR OCCURED FROM GOOGLEAPI")
                    df['State'][i] = "NA"
                else:
                    df['State'][i] = a                     
                    
    elif((df['Latitude'][i]!=None)and(df['Longitude'][i]!=None)):            #This if is to identify on basis of lat andlog
        lat = df['Latitude'][i]
        log = df['Longitude'][i]       
        a = get_state_by_api_loc(lat,log) #uses google api to get State
        if(a=="ERROR"):
            print("ERROR OCCURED FROM GOOGLEAPI")
            df['State'][i] = "NA"
        else:
            df['State'][i] = a
            print(df['State'][i])
            print("Used Google API")  
            
    elif(df['Address'][i]!=None):            #This if is to identify on basis of Address
        add = df['Address'][i] 
      #  print(add)
        li = list(df[df['Address'] == add].index)
        li.remove(i)
       # print(li)
        if(li == None):  # this is if the Address is unique
            a = get_state_by_api(add) #uses google api to get State
            if(a=="ERROR"):
                print("ERROR OCCURED FROM GOOGLEAPI")
                df['State'][i] = "NA"
            else:
                df['State'][i] = a
       #         print(df['State'][i])
                print("Used Google API")
        else:                                           #this is if Address is not unique
            all_names = df['State'][li]
            all_names_set = set(all_names)
        #    print(all_names_set)
            if((len(all_names_set) == 1)and(next(iter(all_names_set))!=None)):    #if all has same State
                df['State'][i] = all_names_set.pop()
            else:                           #if different State
                a = get_state_by_api(add) #uses google api to get State
                if(a=="ERROR"):
                    print("ERROR OCCURED FROM GOOGLEAPI")
                    df['State'][i] = "NA"
                else:
                    df['State'][i] = a
                    
    else:
        print("No data is there on the basis of which State can be found")
        print("So putting NA as a State")
        df['State'][i] = "NA"

print("all Nulls are replaced for State Attribute")
#all null solved for State in df.
df[df['State'].isnull()]
#df[2003:2008]


# <h2>Replacing all Nulls on Zip Attribute

# In[44]:

# detection for zip
null_index_Zip = df[df['Zip'].isnull()].index
print(null_index_Zip)

# removing nulls from Zip

for i in null_index_Zip:
    
    if((df['Latitude'][i]!=None)and(df['Longitude'][i]!=None)):   #This if is to identify on basis of Lat and log
        lat = df['Latitude'][i]
        log = df['Longitude'][i]        
        li = list(df[(df['Latitude'] == lat)&(df['Longitude']==log)].index)
       # print(li)
        li.remove(i)
        #print(li)   
        if(li == None):  # this is if the Lat long is new
            a = get_zip_by_api_loc(lat,log) #uses google api to get State
            if(a=="ERROR"):
                print("ERROR OCCURED FROM GOOGLEAPI")
                df['Zip'][i] = "NA"
            else:
                df['Zip'][i] = a
        #        print(df['Zip'][i])
                print("Used Google API")              
        else:                                           #this is if lat & long is not unique
            all_names = df['Zip'][li]
            all_names_set = set(all_names)
         #   print(all_names_set)
            if((len(all_names_set) == 1)and(next(iter(all_names_set))!=None)):    #if all has same Zip
                df['Zip'][i] = all_names_set.pop()
            else:                           #if different Zip
                a = get_zip_by_api_loc(lat,log) #uses google api to get Zip
                if(a=="ERROR"):
                    print("ERROR OCCURED FROM GOOGLEAPI")
                    df['Zip'][i] = "NA"
                else:
                    df['Zip'][i] = a
           #         print(df['Zip'][i])
                    print("Used Google API")             
                    
                    
    elif(df['Address'][i]!=None):            #This if is to identify on basis of Address
        add = df['Address'][i]
     #   print(add)
        li = list(df[df['Address'] == add].index)
        li.remove(i)
      #  print(li)
        if(li == None):  # this is if the Address is unique
            a = get_zip_by_api(add) #uses google api to get Zip
            if(a=="ERROR"):
                print("ERROR OCCURED FROM GOOGLEAPI")
                df['Zip'][i] = "NA"
            else:
                df['Zip'][i] = a
       #         print(df['Zip'][i])
                print("Used Google API")
        else:                                           #this is if Address is not unique
            all_names = df['Zip'][li]
            all_names_set = set(all_names)
        #    print(all_names_set)
            if((len(all_names_set) == 1)and(next(iter(all_names_set))!=None)):    #if all has same Zip
                df['Zip'][i] = all_names_set.pop()
            else:                           #if different Zip
                a = get_zip_by_api(add) #uses google api to get Zip
                if(a=="ERROR"):
                    print("ERROR OCCURED FROM GOOGLEAPI")
                    df['Zip'][i] = "NA"
                else:
                    df['Zip'][i] = a
                    
    else:
        print("No data is there on the basis of which Zip can be found")
        print("So putting NA as a Zip")
        df['Zip'][i] = "NA"

print("All Nulls have been replaced")
#all null solved for Zip in df.
df[df['State'].isnull()]
#df[4072:4075]


# <h2>Replacing all Nulls on Longitude

# In[46]:

#error8 null detection for Longitude
null_index_Longitude = df[df['Longitude'].isnull()].index
print(null_index_Longitude)

#Error8 resolving null from Longitude
for i in null_index_Longitude:    
    
    if(df['Location'][i]!=None):            #This is based on location attrribute
        l = literal_eval(df['Location'][i])
        df['Longitude'][i] = l[1]
    
    elif(df['Address'][i]!=None):            #This if is to identify on basis of Address
        add = df['Address'][i]
       # print(add)
        li = list(df[df['Address'] == add].index)
        li.remove(i)
        #print(li)
        if(li == None):  # this is if the Address is unique
            a = get_longitude_by_api(add) #uses google api to get Zip
         #   print(a)
            if(a=="ERROR"):
                print("ERROR OCCURED FROM GOOGLEAPI")
                df['Longitude'][i] = "NA"
            else:
                df['Longitude'][i] = a
          #      print(df['Longitude'][i])
                print("Used Google API")
        else:                                           #this is if Address is not unique
            all_names = df['Longitude'][li]
            all_names_set = set(all_names)
           # print(all_names_set)
            if((len(all_names_set) == 1)and(next(iter(all_names_set))!=None)):    #if all has same Longitude
                df['Longitude'][i] = all_names_set.pop()
            else:                                                           #if different lognitude
                a = get_longitude_by_api(add) #uses google api to get lognitude
                if(a=="ERROR"):
                    print("ERROR OCCURED FROM GOOGLEAPI")
                    df['Longitude'][i] = "NA"
                else:
                    df['Longitude'][i] = a
                    
    else:
        print("No data is there on the basis of which Longitude can be found")
        print("So putting NA as a Longitude")
        df['Longitude'][i] = "NA"
        
        
        
print("ALL Nulls have been replaced")
#nulls are replaced from Longitude
df[df['Longitude'].isnull()]
df['Longitude'][null_index_Longitude]


# <h2>Replacing all Nulls on Latitude

# In[48]:

# null detection for Latitude
null_index_Latitude = df[df['Latitude'].isnull()].index
print(null_index_Latitude)

#Error7 resolving null from latitude
for i in null_index_Latitude:
#    print(df['Location'][i])
 #   print(df['Address'][i])
    
    if(df['Location'][i]!=None):            #This is based on location attrribute
        l = literal_eval(df['Location'][i])
        df['Latitude'][i] = l[0]
    
    elif(df['Address'][i]!=None):            #This if is to identify on basis of Address
        add = df['Address'][i]
   #     print(add)
        li = list(df[df['Address'] == add].index)
        li.remove(i)
    #    print(li)
        if(li == None):  # this is if the Address is unique
            a = get_latitude_by_api(add) #uses google api to get latitude
     #       print(a)
            if(a=="ERROR"):
                print("ERROR OCCURED FROM GOOGLEAPI")
                df['Latiude'][i] = "NA"
            else:
                df['Latitude'][i] = a
      #          print(df['Latitude'][i])
                print("Used Google API")
        else:                                           #this is if Address is not unique
            all_names = df['Latitude'][li]
            all_names_set = set(all_names)
       #     print(all_names_set)
            if((len(all_names_set) == 1)and(next(iter(all_names_set))!=None)):    #if all has same latitude
                df['Latitude'][i] = all_names_set.pop()
            else:                                                           #if different Latitude
                a = get_latitude_by_api(add) #uses google api to get latitude
                if(a=="ERROR"):
                    print("ERROR OCCURED FROM GOOGLEAPI")
                    df['Latitude'][i] = "NA"
                else:
                    df['Latitude'][i] = a
                    
    else:
        print("No data is there on the basis of which Latitude can be found")
        print("So putting NA as a Latitude")
        df['Latitude'][i] = "NA"
        
        
print("All Nulls have been replaced")
#nulls are replaced from Latitude
df[df['Latitude'].isnull()]
df['Latitude'][null_index_Latitude]


# <h2>Replacing all Nulls on Location Attribute

# In[49]:

#error9 null detection for Location
null_index_Location = df[df['Location'].isnull()].index
print(null_index_Location)

for i in null_index_Location:    
    location=""
    if((df['Latitude'][i]!=None)and(df['Longitude'][i]!=None)):   #This if is to identify on basis of Lat and log
        location = "("+df['Latitude'][i]+","+df['Longitude'][i]+")"
        df['Location'][i]= location
    
    elif(df['Address'][i]!=None):            #This if is to identify on basis of Address
        add = df['Address'][i]
        #print(add)
        li = list(df[df['Address'] == add].index)
        li.remove(i)
        #print(li)
        if(li == None):  # this is if the Address is unique
            a = get_latitude_by_api(add) #uses google api to get latitude
            b = get_longitude_by_api(add) #uses google api to get longitude
         #   print(a)
         #   print(b)
            if((a=="ERROR")or(b == "ERROR")):
                print("ERROR OCCURED FROM GOOGLEAPI")
                df['Location'][i] = "NA"
            else:
                df['Location'][i] = "("+a+","+b+")"
          #      print(df['Location'][i])
                print("Used Google API")
        else:                                           #this is if Address is not unique
            all_names = df['Location'][li]
            all_names_set = set(all_names)
         #   print(all_names_set)
            if((len(all_names_set) == 1)and(next(iter(all_names_set))!=None)):    #if all has same location
                df['Location'][i] = all_names_set.pop()
            else:                                                           #if different location
                a = get_latitude_by_api(add) #uses google api to get latitude
                b = get_longitude_by_api(add) #uses google api to get longitude                
                if((a=="ERROR")or(b == "ERROR")):
                    print("ERROR OCCURED FROM GOOGLEAPI")
                    df['Location'][i] = "NA"
                else:
                    df['Location'][i] = "("+a+","+b+")"
          #          print(df['Location'][i])
                    print("Used Google API")
                    
    else:
        print("No data is there on the basis of which Location can be found")
        print("So putting NA as a Location")
        df['Location'][i] = "NA"
    

print("All nulls have been replaced")
#nulls are replaced from Location
#df[df['Location'].isnull()]
df['Location'][null_index_Location]


# <h1> Write DATA ON Output File

# In[50]:

# Write output in output_DIW file
writer = pd.ExcelWriter('output_DIW.xlsx')
df.to_excel(writer,'Sheet1',index=False)
writer.save()

