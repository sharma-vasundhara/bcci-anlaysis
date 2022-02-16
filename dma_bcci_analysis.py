#!/usr/bin/env python
# coding: utf-8

# In[1]:


import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


connection = mysql.connector.connect(host = 'localhost', database = 'db_bcci', user = 'root', password = 'abcd1234' )


# In[3]:


cursor = connection.cursor()


# In[4]:


query_stakeholder = "select * from stakeholder"
query_player = "select * from player"
query_coachingstaff = "select * from coaching_staff"
query_managementstaff = "select * from management_staff"
query_clubowner = "select * from club_owner"
query_team_sponsor = "select * from team_sponsor"
query_sponsor = "select * from sponsor"
query_match = "select * from `match`"
query_team = "select * from team"
query_stadium = "select * from stadium"

df_stakeholder = pd.read_sql(query_stakeholder, connection)
df_player = pd.read_sql(query_player, connection)
df_cstaff = pd.read_sql(query_coachingstaff, connection)
df_mstaff = pd.read_sql(query_managementstaff, connection)
df_clubowner = pd.read_sql(query_clubowner, connection)
df_team_sponsor = pd.read_sql(query_team_sponsor, connection)
df_sponsor = pd.read_sql(query_sponsor, connection)
df_match = pd.read_sql(query_match, connection)
df_team = pd.read_sql(query_team, connection)
df_stadium = pd.read_sql(query_stadium, connection)

df_stakeholder.head()


# In[5]:


stakeholder_type = []
for prsnid in df_stakeholder['PRSNID']:
    if prsnid in list(df_player['PRSNID']):
        stakeholder_type.append('Player')
    elif prsnid in list(df_cstaff['PRSNID']):
        stakeholder_type.append('Coaching Staff')
    elif prsnid in list(df_mstaff['PRSNID']):
        stakeholder_type.append('Management Staff')
    elif prsnid in list(df_clubowner['PRSNID']):
        stakeholder_type.append('Club Owner')

df_stakeholder['TYPE'] = stakeholder_type
df_stakeholder.head()


# # Different types of stakeholders in BCCI

# In[6]:


df_type_of_stakeholders = df_stakeholder.groupby(['TYPE']).size()

df_type_of_stakeholders.plot(kind = 'pie', 
                             figsize = (7,7), 
                             autopct = '%1.3f%%', 
                             fontsize = 10, 
                             title = 'Type of Stakeholders',
                             legend = True,
                             label = "")
plt.show()


# # Sponsored Products

# In[7]:


df_team_sponsor_product = pd.merge(df_team_sponsor, df_sponsor, how = 'inner', on = 'SPONSORID')

df_team_sponsor_product.head(3)


# In[8]:


df_team_sponsor_groupby_product = df_team_sponsor_product.groupby(['PRODUCT'])['TEAMID'].count()
fig = df_team_sponsor_groupby_product.plot(kind='bar', color = 'purple', fontsize = 10, title='Advertised Products', figsize=(8, 8))
fig.grid(axis = 'y')


# # Team with maximum number of wins

# In[9]:


df_match_teams = pd.merge(df_match, df_team, how = 'inner', left_on = 'WINNER', right_on = 'TEAMID')
df_match_teams.head(3)


# In[10]:


countplt, fig = plt.subplots(figsize = (8,8))
fig = sns.countplot(df_match_teams['TEAM_NAME'], palette = "Set1")
fig.grid(axis = 'y')
fig.set(xlabel = 'Team Name', ylabel = 'Number of matches won', title = 'Number of matches won by IPL Teams')
fig.set_xticklabels(fig.get_xticklabels(), rotation=90)


# # Studying Mumbai Indians' win over the years

# In[11]:


df_match.head(3)


# In[12]:


df_mumbai_indians_matches = df_match[(df_match['TEAMID_1']=='T001') | (df_match['TEAMID_2']=='T001')]
df_mumbai_indians_matches.head()


# In[13]:


df_mumbai_indians_matches['DATE'] = pd.to_datetime(df_mumbai_indians_matches['DATE'], format='%Y-%m-%d')
df_mumbai_indians_matches.dtypes


# In[14]:


df_mumbai_indians_matches['DATE'] = df_mumbai_indians_matches['DATE'].dt.year
df_mumbai_indians_matches.head(2)


# In[22]:


countplt, fig = plt.subplots(figsize = (8,8))
fig = sns.countplot(df_mumbai_indians_matches['DATE'], palette = "rocket")
fig.grid(axis = 'y')
fig.set(xlabel = 'YEAR', ylabel = 'Number of matches won', title = 'Number of matches won by Mumbai Indians')

