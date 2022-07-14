# -*- coding: utf-8 -*-

from operator import neg
import os
import pandas as pd
import googleapiclient.discovery
from google.cloud import language
import os, sys
import plotext as plt

VIDEO_ID = sys.argv[1]


def main(video_id):
    # data scraping 
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
#     DEVELOPER_KEY = "AIzaSyDUegTGf9xjYEPubMqLodgxcmI3uuvNM3o"
    DEVELOPER_KEY = "AIzaSyDs6CAMKo4YaEfT0G9X1l2ZsS42cLndPYA"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet,id",
        order="relevance",
        videoId=video_id
    )
    response = request.execute()

    return response

def analyze_text_sentiment(text):
    
    # sentiment analysis
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gspyapi-310804-55422293f563.json'
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document=document)
    sentiment = response.document_sentiment
    return sentiment.score
        
        
if __name__ == "__main__":
    # print('welcome')
    data = main(VIDEO_ID)
    pos_cnt, neg_cnt, neu_cnt = 0, 0, 0
    # print(data['items'][i])
    try:
        for i in range(len(data['items'])):
            text = data['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal']
            score = analyze_text_sentiment(text)
            print('----')
            print('text:', text)
            if score >= 0.45:
                print('sentiment is positive')
                pos_cnt += 1
            elif -0.45 <= score <= 0.45:
                print('sentiment is neutral')
                neu_cnt += 1
            else:
                print('sentiment is negative')
                neg_cnt += 1
            print('-----'*10)


        sentiments = ["Positive", "Neutral", "Negative"]
        count = [pos_cnt, neu_cnt, neg_cnt]

        plt.bar(sentiments, count) # or shorter orientation = 'h'
        plt.title("Sentiment of Youtube comments")
        plt.show()
        # print(f'total positive comments : {pos_cnt}')
        # print(f'total neutral comments : {neu_cnt}')
        # print(f'total negative comments : {neg_cnt}')
    except IndexError:
        print(i)
        sys.exit(0)



