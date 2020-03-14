#   References:
#
#   https://github.com/tweepy/tweepy/blob/master/examples/streaming.py
#       - tweepy, streaming, OAUth, listener
#   https://www.tutorialspoint.com/python/string_lower.htm
#       - convert to lowercase in preprocessing 'for' loop
#   https://www.youtube.com/watch?v=qelrVA3zeMc
#       - while loop, counter for streaming tweets 'num_tweets'
#   https://stackoverflow.com/questions/20863486/tweepy-streaming-stop-collecting-tweets-at-x-amount
#       - stop streaming tweets at 'num_tweets'
#   https://stackoverflow.com/questions/19001402/how-to-count-the-total-number-of-lines-in-a-text-file-using-python
#       - counting lines in file, for counting tweets ('num_tweets')
#   https://www.blog.pythonlibrary.org/2010/09/04/python-101-how-to-open-a-file-or-program/
#       - open a file (for opening workbook)
#   https://stackoverflow.com/questions/983354/how-do-i-make-python-to-wait-for-a-pressed-key
#       - press Enter to continue
#   https://en.wikibooks.org/wiki/A_Beginner%27s_Python_Tutorial/Importing_Modules
#       - importing modules
#   https://www.tutorialspoint.com/python/string_lower.htm
#       - lowercase text
#   https://pypi.python.org/pypi/tweet-preprocessor/0.4.0
#       - tweet preprocessor
#   http://xlsxwriter.readthedocs.io/example_chart_pie.html
#       - write results to graph
#   https://docs.python.org/3/tutorial/controlflow.html
#       - else, if, elif


# twitter API auth keys and tokens
import my_keys
# tweepy, stream listener
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
# tweet preprocessor
import preprocessor as pp
# my scripts for tokenization/stopwords
from pp_scripts import *
# naive bayes classifier
from nltk.classify import NaiveBayesClassifier
import pickle
# writing results to graph
import xlsxwriter
# my scripts for slow print function
from sys_scripts import delay_print
# system modules
import operator
import json
import time
import sys
import os

####################

#   asks user for input, this program has two functions:
#       1. search Twitter for user-specified keywords and analyse tweets
#       2. user can enter a sentence and the sentence will be analysed

####################

delay_print("First, specify what data you would like to analyse... Twitter data, or a sentence of your own?\n")
user_source = input('Type "t" for Twitter, or "s" for a sentence: ')

# user types "t", assign to usr_tw variable
usr_tw = 't'
# user types "s", assign to usr_snt variable
usr_snt = 's'

####################

#   naive bayes classifier opened
#       classifier is used in 'if' and also 'elif'
#       so has to be opened outside of 'if' statement

####################

classifier_f = open("naivebayes.pickle", "rb")
myClassifier = pickle.load(classifier_f)
classifier_f.close()


################################################################################

#   IF / ELIF / ELSE
#   'if' statement used below if user chooses Twitter
#       1. user is asked to input keywords and number of tweets to search
#       2. the tweepy streamer class is created
#       3. tweet data is saved to json file
#       4. for loop is entered
#       5. preprocessing and sentiment analysis takes place line by line
#       6. results are appended to lists to be counted later
#       7. for loop is exited
#       8. number of results are printed
#       9. workbook is opened for results
#       10. chart is created in workbook with results
#       11. workbook is closed
#       12. workbook is presented to user

# 'else' and 'elif' statements come later

################################################################################

if user_source == usr_tw:

    # Ask user to input the keyword(s) they want to stream on Twitter, and how many tweets
    keyword = input("Enter the keyword(s) you'd like to search on Twitter:\t")
    num_tweets = int(input("Enter the number of tweets you'd like to retrieve:\t"))

    ####################

    #   my stream listener class is defined below
    #       total number of tweets is counted as tweets are saved
    #       'if' used for saving tweets until criteria is met
    #       tweets will continue to be saved until the total num specified has been reached
    #       'else' finishes the process

    ####################

    def __init__(self, api=None):  # allows us to count total tweets in file
        super(MyListener, self).__init__()
        self.total = 0  # starts total at zero

    class MyListener(StreamListener):

        def on_data(self, data):
            f = open('database.json', 'a')  # opens empty JSON file
            f.write(data)  # writes each tweet to JSON file
            with open('database.json') as f:  # opens to view contents while writing
                total = int(sum(1 for _ in f) / 2)  # sum seemed to be counting double the amount of tweets, so I added '/ 2'
                if total < num_tweets:  # if total tweets is less than number specified, continue
                    return True
                else:  # when total tweets reaches number specified, stop
                    print("\nComplete.")
                    print("Total number of tweets:", total)  # confirms number of tweets
                    return False
            f.close()  # closes the file
            return True

        ####################

        #   error handling
        #       prints the error if there's a problem
        #       e.g. fails to authorise: 401 error

        ####################

        def on_error(self, status):
            print(status)

    ####################

    #   twitter API streaming and authentication
    #       filters 'keyword(s)' as specified by user
    #       searches English only tweets
    #       auth keys and tokens imported from my_keys.py

    ####################

    if __name__ == '__main__':

        l = MyListener()
        auth = OAuthHandler(my_keys.consumer_key, my_keys.consumer_secret)  # consumer key and consumer secret impored from my_keys.py
        auth.set_access_token(my_keys.access_token, my_keys.access_secret)  # access token and access secret impored from my_keys.py
        stream = Stream(auth, l)  # uses MyListener class
        delay_print("Please wait...")  # user friendly info
        print('\n')  # prints line break for tidiness
        stream.filter(track=[keyword], languages=['en'])  # filters English tweets for 'keyword(s)' specified by user

    delay_print('Performing sentiment analysis. Please wait... \n')  # user friendly info

    ####################

    #   some variables are defined below:
    #       tags are given same value returned by naive bayes classifier in classifier.py lines 42 + 57
    #       tags are used for 'if', 'else' statements below
    #       empty lists are created for pos and neg results
    #       lists will be used to count total number of results

    ####################

    pos_tag = 'Positive'
    neg_tag = 'Negative'

    positive_tweets = []
    negative_tweets = []

    ####################

    #   'database.json is opened, and then 'for' loop is entered
    #   I had to nest a try and except loop inside due to json.loads(line) decode errors
    #       1. loads json file line by line
    #       2. extracts tweet from line and preprocesses
    #       3. converts to lowercase for consistency
    #       4. tokenizes and removes stopwords
    #       5. 'True' appended to each token for naive bayes
    #       6. naive bayes classifier runs and analyses each tweet
    #       7. 'if' result is positive, append to pos results list
    #       8. 'else' result is negative, so append to neg results list
    #       9. length of lists are calculated
    #       10. results are defined as variables: 'num_pos_results', 'num_neg_results'
    #       11. totals are diplayed to user

    ####################

    with open('database.json', 'r') as f:

        # had to nest a try and except loop inside for loop due to json.loads(line) decode errors
        for line in f:
            try:  # initiates line by line loop
                each_line = json.loads(line)
                pp_tweet = pp.clean(each_line['text'])  # preprocesses the tweet from each line - removes hashtags, @-mentions, URLs etc.
                lower = pp_tweet.lower()  # converts to lowercase for consistency
                tokens = [term for term in myTokenizer(lower) if term not in stop_words]  # calls myTokenizer function and tokenizes i imported from pp_scripts.py
                features = myFeatures(tokens)  # appends 'True' to tokens
                sentiment = myClassifier.classify(features)  # classifier is called and analyses the tokens
                if sentiment == pos_tag:  # if result is 'pos'
                    positive_sentiment = sentiment  # result becomes 'positive_sentiment'
                    positive_tweets.append(positive_sentiment)  # append result to 'positive_tweets' list
                else:  # if result is not 'pos', then result is 'neg'
                    negative_sentiment = sentiment  # result becomes 'negative_sentiment'
                    negative_tweets.append(negative_sentiment)  # append result to 'negative_tweets' list
            except:  # continues even if there's an error
                continue  # 'pass' is suitable here too

    num_pos_results = len(positive_tweets)  # number of pos tweets defined as 'num_pos_results'
    num_neg_results = len(negative_tweets)  # number of neg tweets defined as 'num_neg_results'

    print('Number of positive tweets:', num_pos_results)  # prints number of pos tweets
    print('Number of negative tweets:', num_neg_results)  # prints number of neg tweets

    ####################

    #   results are saved to graph and presented to user
    #       1. workbook is opened for results
    #       2. 'num_pos_results', 'num_neg_results' referred to in chart data
    #       2. chart is created in workbook
    #       3. workbook is closed
    #       4. workbook is opened and presented to user

    ####################

    # create workbook in same directory
    workbook = xlsxwriter.Workbook('sentiment_results.xlsx')
    # create spreadsheet in the workbook
    worksheet = workbook.add_worksheet()
    # bold font style
    bold = workbook.add_format({'bold': 1})

    # column headings
    headings = ['Polarity', 'Quantity']
    data = [
        ['Positive', 'Negative'],  # pull results and use in chart
        [num_pos_results, num_neg_results],
    ]

    worksheet.write_row('A1', headings, bold)  # write column headings beginning in cell A1
    worksheet.write_column('A2', data[0])  # write num of pos tweets in cell A2
    worksheet.write_column('B2', data[1])  # write num of neg tweets in cell B2

    # create a new chart object
    chart1 = workbook.add_chart({'type': 'bar'})

    # configure the series - required for styling the chart
    chart1.add_series({
        'name':       'Sentiment Analysis',
        'categories': ['Sheet1', 1, 0, 3, 0],
        'values':     ['Sheet1', 1, 1, 3, 1],
        'points': [
            {'fill': {'color': 'green'}},  # colours pos results green
            {'fill': {'color': 'red'}},  # colours neg results red
        ]
    })

    # add the chart title
    chart1.set_title({'name': 'Sentiment Analysis'})

    # insert the chart into the worksheet with offset
    worksheet.insert_chart('C2', chart1, {'x_offset': 65, 'y_offset': 10})

    # close workbook
    workbook.close()

    delay_print("Sentiment analysis complete. \n")  # user friendly info

    # asks user to press Enter and then opens the workbook automatically
    print("Ready to display results, ", end=''), input("press Enter to continue...")
    os.startfile('.\sentiment_results.xlsx')

################################################################################

#   IF / ELIF / ELSE
#   return to inital user_source choice
#   'elif' statement used below if user chooses sentence
#       1. user is asked to input sentence
#       2. sentence is preprocessed
#       3. sentence is tokenized and stopwords are removed
#       4. 'True' appended to each token for naive bayes
#       5. naive bayes classifier runs and analyses the tokens
#

# 'else' statement comes later

################################################################################

elif user_source == usr_snt:  # if user chooses to analyse a sentence
    usr_input = input("Enter the sentence you'd like to analyse: ")  # enter the sentence
    delay_print("Thank you. Now we perform the sentiment analysis!\n")  # user friendly info
    # delay_print("Now we have to process the sentence and remove the junk...\n")
    pp_input = pp.clean(usr_input)  # preprocesses the sentence if necessary - removes hashtags, URLs etc
    lower = pp_input.lower()  # converts to lowercase if necessary
    tokens = [term for term in myTokenizer(lower) if term not in stop_words]  # calls myTokenizer function from pp_scripts.py
    # print(tokens)
    features = (myFeatures(tokens))  # appends 'True' to tokens
    sentiment = myClassifier.classify(features)  # calls myClassifier which is outside loop at beginning of script
    print("Your sentence was:", sentiment)  # presents result

################################################################################

#   IF / ELIF / ELSE
#   'else' statement used below if user fails to input "t" or "s"
#   program quits, user can follow instruction manual to restart

################################################################################

else:
    input("Command not recognised. Press Enter to close...")
    False
