#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from openpyxl import Workbook
from urllib.request import urlopen
import json


st.set_page_config(layout='wide')

#st.sidebar.markdown('#Combating Food Insecurity')

multi_index = pd.MultiIndex.from_product

# In[6]:


datain = pd.read_csv('Df_Final.csv', index_col=0)
#print(datain)


# In[7]:

#fig = make_subplots(rows=3, cols=2)

#datain.head()


# In[10]:


#datain.shape


# In[16]:


datain['FIPS'] = datain['FIPS'].apply(lambda x: str(x))


# In[18]:


datain['FIPS'] = datain['FIPS'].str.zfill(5)
#datain.head()


# In[25]:



# Create columns
sect1_1, sect1_2 = st.beta_columns((2,3))

# Layout top section of app
with sect1_1:
    st.title("US Food Insecurity Data")

with sect1_2:
    st.write(
        """
        ##
        Team 30:  Examing Food Insecurity in the US.  Graphs are interactive.  Hover over graphs for data.  Click on items in the legend to toggle on/off.
        """
    )    

# In[29]:

col1, col2 = st.beta_columns(2)

# USA Only
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

fig = px.choropleth(datain, geojson=counties, locations='FIPS', color='Food Insecurity Rate',
                           color_continuous_scale="Jet",
                           range_color=(0,0.4),
                           #mapbox_style="carto-positron",
                           scope='usa',
                           #zoom=3, 
                           center = {"lat": 37.0902, "lon": -95.7129},
                           #opacity=0.9,
                           labels={'Food Insecurity Rate':'Food Insecurity Rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#fig.show()

with col1:
    st.write(
    """
    ##
    **US Food Insecurity Rates  **
    """)
    col1.plotly_chart(fig)


# In[30]:


datain['Regions']=""
datain['State']=""


# In[31]:


Regions_df=pd.read_excel('state-geocodes-v2015.xls',  dtype = str )


# In[32]:


Regions_df.drop([0,1,2,3,4], inplace=True)


# In[33]:


Regions_df.rename(columns={'Census Bureau Region and Division Codes and Federal Information Processing System (FIPS) Codes for States': 'Region',"Unnamed: 1":"Division", "Unnamed: 2":"State (FIPS)", "Unnamed: 3":"Name"}, inplace =True)
Regions_df.head()


# In[34]:


Regions_df.reset_index(inplace=True)
Regions_df.head()


# In[37]:


datain[["Regions", "State"]]=datain["County"].str.rsplit(",",  expand=True)


# In[38]:


datain['State']=datain['State'].apply(lambda x: str(x))


# In[40]:


# Filling the region column by using the states. 
Assigned_Regions=[]
for states in datain["State"]:
    if states in [' Connecticut',' Maine',' Massachusetts',' New Hampshire', ' Rhode Island', ' Vermont',' New Jersey', ' New York',' Pennsylvania']:
        Assigned_Regions.append("Northeast")
    elif states in [' Illinois', ' Indiana', ' Michigan',' Ohio', ' Wisconsin',' Iowa',' Kansas',' Minnesota',' Missouri',' Nebraska', ' North Dakota', ' South Dakota']:
        Assigned_Regions.append("Midwest")
    elif states in [' Delaware', ' District of Columbia',  ' Florida', ' Georgia', ' Maryland', ' North Carolina', ' South Carolina', ' Virginia', ' West Virginia', ' Alabama', ' Kentucky', ' Mississippi', ' Tennessee',' Arkansas', ' Louisiana',' Oklahoma', ' Texas']:
        Assigned_Regions.append("South")
    elif  states in [' Arizona', ' Colorado',' Idaho', ' Montana', ' Nevada', ' New Mexico', ' Utah', ' Wyoming', ' Alaska', ' California', ' Hawaii', ' Oregon', ' Washington']:
        Assigned_Regions.append("West")


# In[41]:


datain["Regions"]=Assigned_Regions


# In[43]:


# Filling the region column by using the states. 
# New England Division: Connecticut, Maine, Massachusetts, New Hampshire, Rhode Island, Vermont
# Middle Atlantic Division: New Jersey, New York, Pennsylvania
# East North Central Division: Illinois, Indiana, Michigan, Ohio, Wisconsin
# West North Central Division: Iowa, Kansas, Minnesota, Missouri, Nebraska, North Dakota, South Dakota
# South Atlantic Division: Delaware, District of Columbia,  Florida, Georgia, Maryland, North Carolina, South Carolina, Virginia, West Virginia
# East South Central Division: Alabama, Kentucky, Mississippi, Tennessee
# West South Central Division: Arkansas, Louisiana, Oklahoma, Texas
# Mountain Division: Arizona, Colorado, Idaho, Montana, Nevada, New Mexico, Utah, Wyoming
# Pacific Division" Alaska: California, Hawaii, Oregon, Washington

Assigned_SubRegions=[]
for states in datain["State"]:
    if states in [' Connecticut',' Maine',' Massachusetts',' New Hampshire', ' Rhode Island', ' Vermont']:           
        Assigned_SubRegions.append('New England Division')
    elif states in [' New Jersey', ' New York',' Pennsylvania']:
        Assigned_SubRegions.append('Middle Atlantic Division')
    elif states in [' Illinois', ' Indiana', ' Michigan',' Ohio', ' Wisconsin']:
        Assigned_SubRegions.append('East North Central Division')
    elif states in [' Iowa',' Kansas',' Minnesota',' Missouri',' Nebraska', ' North Dakota', ' South Dakota']:
        Assigned_SubRegions.append('West North Central Division')
    elif states in [' Delaware', ' District of Columbia',  ' Florida', ' Georgia', ' Maryland', ' North Carolina', ' South Carolina', ' Virginia', ' West Virginia']:
        Assigned_SubRegions.append("South Atlantic Division")
    elif states in [' Alabama', ' Kentucky', ' Mississippi', ' Tennessee']:
        Assigned_SubRegions.append("East South Central Division")
    elif states in [' Arkansas', ' Louisiana',' Oklahoma', ' Texas']:
        Assigned_SubRegions.append("West South Central Division")
    elif  states in [' Arizona', ' Colorado',' Idaho', ' Montana', ' Nevada', ' New Mexico', ' Utah', ' Wyoming']:
        Assigned_SubRegions.append("Mountain Division")
    elif  states in [' Alaska', ' California', ' Hawaii', ' Oregon', ' Washington']:
        Assigned_SubRegions.append("Pacific Division")


# In[44]:


datain["Subregions"]=Assigned_SubRegions


# In[46]:


fig = px.scatter(datain, x="Food Insecurity Rate", y="MedianFamilyIncome", color="Regions",
                    labels={
                            'Regions': 'Regions'
                    }
            )
#fig.show()

with col2:
    st.write(
    """
    ##
    **Food Insecurity Rate vs. Median Income by Region**
    """
    )
    col2.plotly_chart(fig)



# In[47]:

col3, col4 = st.beta_columns(2)




# In[48]:


All=datain.copy()  #groupby(["Regions"]).median().reset_index()
fig = px.box(All, x="Regions", y="Food Insecurity Rate", points="all", color= "Regions")
#fig.show()

with col3:
    st.write(
    """
    **Food Insecurity Rates by Region**
    """)
    col3.plotly_chart(fig)


# In[49]:


#Income Class 
Assigned_Class=[]
for Class in datain['MedianFamilyIncome']:
    if Class<40100:
        Assigned_Class.append("Low")
    elif (Class>= 40100 and Class<=120400):
        Assigned_Class.append("Middle")
    elif Class>120400: 
        Assigned_Class.append("High")
datain['Income_Group']=Assigned_Class


# In[50]:


All=datain#groupby(["Regions"]).median().reset_index()
fig = px.box(All, x="Regions", y="Food Insecurity Rate", points="all", color= "Income_Group")
#fig.show()

with col4:
    st.write(
        """
        ##
        **Food Insecurity Rate by Income Group by Region**
        """
    )
    col4.plotly_chart(fig)


# In[51]:

col5, col6 = st.beta_columns(2)

fig = px.box(All, x="Subregions", y="Food Insecurity Rate", points="all", color= "Subregions")
#fig.show()
with col5:
    st.write(
        """
        ##
        **Food Insecurity Rate by Subregion**
        """
    )
    col5.plotly_chart(fig)

fig = px.scatter(datain, x="Food Insecurity Rate", y="MedianFamilyIncome", color="Subregions",
        labels={
            'Subregions':'Subregions'
        }
)
#fig.show()

with col6:
    st.write(
        """
        **Food Insecurity Rate by Median Family Income by Subregion**
        """)
    col6.plotly_chart(fig)    


# In[52]:


fig = px.box(All, x="Subregions", y="Food Insecurity Rate", points="all", color= "Income_Group")
#fig.show()


# In[54]:


fig = px.histogram(datain, x="Food Insecurity Rate", color="Subregions")
#fig.show()

