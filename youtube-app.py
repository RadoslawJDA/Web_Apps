import requests
import pandas as pd
import streamlit as st
import time
import re
import json
import numpy
from bs4 import BeautifulSoup

st.set_page_config(page_title="YouTube Data Dashboard", page_icon="chart_with_upwards_trend")


#scraping channel id from url input
def get_channel_id():
  URL = st.sidebar.text_input("Enter channel's URL", 'https://www.youtube.com/@rad827')
  soup = BeautifulSoup(requests.get(URL, cookies={'CONSENT': 'YES+1'}).text, "html.parser")

  data = re.search(r"var ytInitialData = ({.*});", str(soup.prettify())).group(1)
  json_data = json.loads(data)

  CHANNEL_ID = json_data['header']['c4TabbedHeaderRenderer']['channelId']
  return CHANNEL_ID
CHANNEL_ID = get_channel_id()

#API keys
API_KEY = 'AIzaSyCdY6oRpKZkrQNcW28u0wCCM-HL24aVrpQ'#'AIzaSyDLgV5vjxJ5Qo9JCr1hfJoUCd4rSyUpwnc'#

#video details
def get_video_details(video_id):
    
   #second API call

    url_video_stats = "https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&part=statistics&key="+API_KEY
    response_video_stats =  requests.get(url_video_stats).json()

    view_count = response_video_stats['items'][0]['statistics']['viewCount']
    like_count = response_video_stats['items'][0]['statistics']['likeCount']
    comment_count = response_video_stats['items'][0]['statistics']['commentCount']

    return view_count, like_count, comment_count 

#video
def get_videos(df):

  #api call
  pageToken = ""
  url = "https://www.googleapis.com/youtube/v3/search?key="+API_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=date&maxResults=10000"+pageToken
  response =  requests.get(url).json()

  for video in response['items']:
    if video['id']['kind']== "youtube#video":
      video_id = video['id']['videoId']
      video_title = video['snippet']['title']
      upload_date = video['snippet']['publishedAt']
      upload_date = str(upload_date).split("T")[0]

      view_count, like_count, comment_count = get_video_details(video_id)

      #save data in pandas df
      df = df.append({'video_id': video_id,"video_title": video_title,
                      "upload_date": upload_date,"view_count": view_count,
                      "like_count": like_count,"comment_count": comment_count},ignore_index=True) 
      
  more_pages = True
  while more_pages:
    next_page_token = response.get('nextPageToken')
    if next_page_token is None:
      more_pages = False
    else:
      #api call
      url = "https://www.googleapis.com/youtube/v3/search?key="+API_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=date&maxResults=10000&pageToken="+next_page_token

      response =  requests.get(url).json()


      for video in response['items']:
        if video['id']['kind']== "youtube#video":
          video_id = video['id']['videoId']
          video_title = video['snippet']['title']
          upload_date = video['snippet']['publishedAt']
          upload_date = str(upload_date).split("T")[0]

          view_count, like_count, comment_count = get_video_details(video_id)

          #save data in pandas df
          df = df.append({'video_id': video_id,"video_title": video_title,
                          "upload_date": upload_date,"view_count": view_count,
                          "like_count": like_count,"comment_count": comment_count},ignore_index=True)

  return df


pageToken = ""
url = "https://www.googleapis.com/youtube/v3/search?key="+API_KEY+"&channelId="+CHANNEL_ID+"&part=snippet,id&order=date&maxResults=10000"+pageToken
response =  requests.get(url).json()

#dataframe
df = pd.DataFrame(columns=("video_id","video_title","upload_date","view_count","like_count","comment_count"))
df = get_videos(df)

# showing dataset
st.dataframe(df)

# Download Dataset button 
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')
csv = convert_df(df)

st.download_button(
   "Download Dataset",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)

# # Display the data in a chart or table
# if st.checkbox("Show data"):
#         st.write("Number of Subscriber ", data['items'][0]['statistics']['subscriberCount'])
#         st.write("Number of Views", data['items'][0]['statistics']['viewCount'])
#         st.write("Number of Videos", data['items'][0]['statistics']['videoCount'])

# # title
# with header_mid:
#     st.title('YouTube Data Dashboard')
    
# # sidebar
# with st.sidebar:
#     Campaign_filter = st.multiselect(label= 'Select The Campaign',
#                                 options=df['campaign'].unique(),
#                                 default=df['campaign'].unique())

#     Age_filter = st.multiselect(label='Select Age Group',
#                             options=df['age'].unique(),
#                             default=df['age'].unique())

#     Gender_filter = st.multiselect(label='Select Gender Group',
#                             options=df['gender'].unique(),
#                             default=df['gender'].unique())



