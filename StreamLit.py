import tweepy as tw
import streamlit as st
import pandas as pd
from transformers import pipeline
import credentials

# Twitter API credentials
consumer_key = credentials.API_KEY
consumer_secret = credentials.API_SECRET_KEY
access_key = credentials.ACCESS_TOKEN
access_secret = credentials.ACCESS_TOKEN_SECRET

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tw.API(auth, wait_on_rate_limit=False)


# App streamlit
classifier = pipeline('sentiment-analysis')
st.title('Analyse de sentiments de tweets en temps réel ')


def run():
    with st.form(key='Enter name'):
        search_words = st.text_input('Saisir le sujet dont vous voulez connâitre le sentiment')
        number_of_tweets = st.number_input(
            'saisir le nombre de derniers tweets dont vous voulez connâitre le sentiment’, 0,10000,10')
        submit_button = st.form_submit_button(label='Submit')
        date_since = "2022-04-12"
        new_search = search_words + " -filter:retweets"

        if submit_button:
            tweets = tw.Cursor(api.search_tweets, q=new_search, lang='en', since_id=date_since,
                               result_type="recent").items(number_of_tweets)

            tweet_list = [i.text for i in tweets]
            p = [i for i in classifier(tweet_list)]
            q = [p[i]['label'] for i in range(len(p))]
            df = pd.DataFrame(list(zip(tweet_list, q)),
                              columns=['Latest' + str(number_of_tweets) + 'Tweets' + 'on' + search_words, 'sentiment'])
            tweets2 = tw.Cursor(api.search_tweets, q=new_search, lang='en', since_id=date_since,
                                result_type="recent").items(number_of_tweets)
            users_locs = [[i.user.screen_name, i.created_at, i.user.location, i.text] for i in tweets2]
            df2 = pd.DataFrame(data=users_locs, columns=['user', 'time', 'location', 'text'])



            st.write(df)
            st.write(df2)

            df.to_csv(f'C:/Users/younes.aziz/PycharmProjects/pythonProject_twitter/sentiment.csv')
            df2.to_csv(f'C:/Users/younes.aziz/PycharmProjects/pythonProject_twitter/data.csv')


if __name__ == '__main__':
    run()
