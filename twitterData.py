import os
import tweepy as tw
import pymongo as pymo
import pandas as pd


#Completar datos de consumer_key, consumer_secret, access_token, access_token_secret

consumer_key= '' 
consumer_secret= ''
access_token= ''
access_token_secret= ''

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


# Definir los criterios de busqueda
search_words = input("Palabra clave:")
date_since = input("Desde fecha (aaaa-mm-dd):")
date_until = input("Hasta fecha (aaaa-mm-dd):")
tweet_count = input("Cantidad maxima de Tweets a obtener:")

# Guardar tweets
tweets = tw.Cursor(api.search,
              q=search_words + " -filter:retweets",
             #define language lang="en",
              since=date_since,
              until=date_until).items(int(tweet_count))


    

#Indicar link de conexion a mongo
client = pymo.MongoClient("")

mydb = client["mydatabase"]
mycol = mydb["tweetData"]

for tweet in tweets:
    mydict = { "keyword": search_words,"username": tweet.user.screen_name, "fechaCreacion": tweet.user.created_at, "likes": tweet.user.favourites_count,"tweets": tweet.user.statuses_count,"userlocation": tweet.user.location, "followers": tweet.user.followers_count,"verified":tweet.user.verified,"text": tweet.text, "tweetdate":tweet.created_at, "tweetlang":tweet.lang}
    x = mycol.insert_one(mydict)
    
    
    
mongo_docs = mycol.find()

    # Convertir de mongo docs a DataFrame
docs = pd.DataFrame(mongo_docs)

docs.pop("_id")

docs.to_csv("MongoData.csv", encoding='utf-8-sig')
