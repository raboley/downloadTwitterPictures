import tweepy
import os
from tweepy import OAuthHandler
import json
import argparse
import configparser

#TODO: Limit by number of tweets?
def parse_arguments():
  parser = argparse.ArgumentParser(description='Download pictures from Twitter.')
  group = parser.add_mutually_exclusive_group(required=True)
  parser.add_argument('--config', type=str, default='./config.cfg', help='Path to the configuration file')
  group.add_argument('--username', type=str, help='The twitter screen name from the account we want to retrieve all the pictures')
  group.add_argument('--hashtag', type=str, help='The twitter tag we want to retrieve all the pictures. ')
  parser.add_argument('--num', type=int, default=100, help='Maximum number of tweets to be returned.')
  parser.add_argument('--retweets', default=False, action='store_true', help='Include retweets')
  parser.add_argument('--replies', default=False, action='store_true', help='Include replies')
  parser.add_argument('--output', default='pictures/', type=str, help='folder where the pictures will be stored')
  parser.add_argument('--bucket', default='', type=str, help='aws s3 bucket where this should be uploaded')

  args = parser.parse_args()
  return args

def parse_config(config_file):
  config = configparser.ConfigParser()
  config.read(config_file)
  return config 
  
@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

def init_tweepy():
  # Status() is the data model for a tweet
  tweepy.models.Status.first_parse = tweepy.models.Status.parse
  tweepy.models.Status.parse = parse
  # User() is the data model for a user profil
  tweepy.models.User.first_parse = tweepy.models.User.parse
  tweepy.models.User.parse = parse

def authorize_twitter_api(config):
  auth = OAuthHandler(config['DEFAULT']['consumer_key'], config['DEFAULT']['consumer_secret'])
  auth.set_access_token(config['DEFAULT']['access_token'], config['DEFAULT']['access_secret'])
  return auth

# It returns [] if the tweet doesn't have any media
def tweet_media_urls(tweet_status):
  media = tweet_status._json.get('extended_entities', {}).get('media', [])
  if (len(media) == 0):
    return []
  else:
    return [item['media_url'] for item in media]

def create_folder(output_folder):
  if not os.path.exists(output_folder):
      os.makedirs(output_folder)

def download_images(status, num_tweets, output_folder, bucket):
  if bucket == '':
    download_images_local(status=status, num_tweets=num_tweets, output_folder=output_folder)
  else:
    download_images_s3(status, num_tweets, output_folder, bucket)

def download_images_local(status, num_tweets, output_folder):
  create_folder(output_folder)
  downloaded = 0

  for tweet_status in status:

    if(downloaded >= num_tweets):
      break

    for media_url in tweet_media_urls(tweet_status):
      # Only download if there is not a picture with the same name in the folder already
      file_name = os.path.split(media_url)[1]
      if not os.path.exists(os.path.join(output_folder, file_name)):
        print(media_url)
        wget.download(media_url +":orig", out=output_folder+'/'+file_name)
        downloaded += 1

def download_images_s3(status, num_tweets, output_folder, bucket):
  create_folder('temp')
  downloaded = 0

  for tweet_status in status:

    if(downloaded >= num_tweets):
      break

    for media_url in tweet_media_urls(tweet_status):
      # Only download if there is not a picture with the same name in the folder already
      file_name = os.path.split(media_url)[1]
      temp_full_path =  'temp/' + file_name
      final_path = output_folder + '/' + file_name
      if not push.file_exists_in_s3(bucket=bucket, file_path=final_path):
        print(media_url)
        wget.download(media_url +":orig", out=temp_full_path)
        push.uploadfile(bucket=bucket, upload_file_full_path=final_path, local_filepath=temp_full_path)
        downloaded += 1



def download_images_by_user(api, username, retweets, replies, num_tweets, output_folder, bucket):
  status = tweepy.Cursor(api.user_timeline, screen_name=username, include_rts=retweets, exclude_replies=replies, tweet_mode='extended').items()
  download_images(status, num_tweets, output_folder, bucket)

def download_images_by_tag(api, tag, retweets, replies, num_tweets, output_folder, bucket):
  status = tweepy.Cursor(api.search, '#'+tag, include_rts=retweets, exclude_replies=replies, tweet_mode='extended').items()
  download_images(status, num_tweets, output_folder, bucket)

def main():
  arguments = parse_arguments() 
  username = arguments.username
  hashtag = arguments.hashtag
  retweets = arguments.retweets
  replies = arguments.replies
  num_tweets = arguments.num
  output_folder = arguments.output
  config_path = arguments.config
  bucket = arguments.bucket

  config = parse_config(config_path)
  auth = authorise_twitter_api(config)
  api = tweepy.API(auth, wait_on_rate_limit=True)

  if hashtag:
    download_images_by_tag(api, hashtag, retweets, replies, num_tweets, output_folder, bucket)
  else:
    download_images_by_user(api, username, retweets, replies, num_tweets, output_folder, bucket)

if __name__=='__main__':
    main()
