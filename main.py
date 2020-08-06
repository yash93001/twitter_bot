from helper import *

def main_function():
    keyword,user, task_choice, count = disp_index()
    api = authenticate_api()
    if task_choice == 1:
        specific_user_no_of_tweets(api, keyword, user, count)

    elif task_choice == 2:
        unique_user_tweet_likes(api,keyword,count)
    else:
        random_user_tweet_likes(api,keyword,count)


if __name__ == "__main__":
    status = 1
    display_greet()
    while(status):
        main_function()
        status = disp_quit()










