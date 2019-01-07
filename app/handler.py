import download_twitter_photos.py

def handler(event,context):
    """Sends random tweet from list of potential tweets"""
    send_tweet(random.choice(potential_tweets))