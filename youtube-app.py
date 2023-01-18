import requests
import pandas as pd
import streamlit as st
import time
import re
import json
from bs4 import BeautifulSoup

#scraping channel id from url input

URL = st.text_input("Enter channel's URL", 'https://www.youtube.com/@rad827')
soup = BeautifulSoup(requests.get(URL, cookies={'CONSENT': 'YES+1'}).text, "html.parser")

data = re.search(r"var ytInitialData = ({.*});", str(soup.prettify())).group(1)
json_data = json.loads(data)

CHANNEL_ID = json_data['header']['c4TabbedHeaderRenderer']['channelId']

#keys

API_KEY = 'AIzaSyDLgV5vjxJ5Qo9JCr1hfJoUCd4rSyUpwnc'#'AIzaSyCdY6oRpKZkrQNcW28u0wCCM-HL24aVrpQ'


def get_video_details(video_id):
    
   #second API call

    url_video_stats = "https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&part=statistics&key="+API_KEY
    response_video_stats =  requests.get(url_video_stats).json()

    view_count = response_video_stats['items'][0]['statistics']['viewCount']
    like_count = response_video_stats['items'][0]['statistics']['likeCount']
    comment_count = response_video_stats['items'][0]['statistics']['commentCount']

    return view_count, like_count, comment_count 


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

#build our dataframe
df = pd.DataFrame(columns=("video_id","video_title","upload_date","view_count","like_count","comment_count"))
df = get_videos(df)

st.dataframe(df)

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