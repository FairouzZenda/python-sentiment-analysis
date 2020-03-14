#   References:
#
#   https://www.tutorialspoint.com/python/python_if_else.htm
#       - if, elif, else statement
#   https://docs.python.org/3/tutorial/controlflow.html
#       - if, elif, else statement
#   https://pypi.python.org/pypi/tweet-preprocessor/0.4.0
#       - tweet preprocessor
#   http://www.nltk.org/book/ch06.html
#       - classifying sentiment
#   https://en.wikibooks.org/wiki/A_Beginner%27s_Python_Tutorial/Importing_Modules
#       - importing modules
#   https://www.twilio.com/blog/2017/09/sentiment-analysis-python-messy-data-nltk.html
#       - splitting into training/test datasets


# natural language toolkit
import nltk
from nltk.corpus import twitter_samples
from nltk.corpus import stopwords
# naive bayes classifier
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
import pickle
# my scripts for tokenization/stopwords
from pp_scripts import *
# tweet preprocessor
import preprocessor as pp
# system modules
import json

####################

#   asks user for input, this program has two functions:
#       1. train a new naive bayes classifier and save as naivebayes.pickle
#       2. test an exisiting classifier, saved as naivebayes.pickle

####################

answer = input('Would you like to train or test the NaiveBayesClassifier? Type "train" or "test" and press Enter...\n')

# usr_trn assigned if user selects to train
usr_trn = 'train'
# usr_tst assigned if user selects to test
usr_tst = 'test'

################################################################################

#       IF / ELIF / ELSE
#       if
#       user selects to train classifier

################################################################################

if answer == usr_trn:

    # tag positive samples as 'pos'
    pos_samples = []
    # open twitter_samples
    with open('./Sample Data/twitter_samples/positive_tweets.json') as f:  # opens positive_tweets from Sample Data folder
        for line in f:
            try:  # try and except to get around json.loads(line) decode errors
                each_line = json.loads(line)  # loops line by line
                tweet = pp.clean(each_line['text'])  # preprocesses each tweet, removes hashtags, URLs etc
                tokens = [term for term in myTokenizer(tweet) if term not in stop_words]  # calls myTokenizer function and tokenizes
                features = myFeatures(tokens)  # appends 'True' to tokens
                pos_samples.append((features, "Positive"))  # appends 'Positive' tag to each pos tweet

            except:
                continue

    # tag negative samples as 'neg'
    neg_samples = []
    # open twitter_samples
    with open('./Sample Data/twitter_samples/negative_tweets.json') as f:  # opens positive_tweets from Sample Data folder
        for line in f:
            try:  # try and except to get around json.loads(line) decode errors
                each_line = json.loads(line)  # loops line by line
                tweet = pp.clean(each_line['text'])  # preprocesses each tweet, removes hashtags, URLs etc
                tokens = [term for term in myTokenizer(tweet) if term not in stop_words]  # calls myTokenizer function and tokenizes
                features = myFeatures(tokens)  # appends 'True' to tokens
                neg_samples.append((features, "Negative"))  # appends 'Negative' tag to each neg tweet

            except:
                continue

    total_pos = len(pos_samples)  # totals num of pos samples
    total_neg = len(neg_samples)  # totals num of neg samples
    total_sum = total_pos + total_neg  # total num of samples, pos + neg

    print("\nNumber of positive tweet samples:\t", total_pos)  # print total pos

    print("Number of negative tweet samples:\t", total_neg)  # print total neg

    print("Total number of samples:\t\t", total_sum, "\n")  # print sum

    ####################

    #   section allows user to select train/test ratio
    #   e.g 70% training set / 30% test set
    #       1. user is presented with list of choices
    #       2. user chooses a number which influences if/elif/else statements below
    #       3. if the user inputs an incorrect command, they will return to start of while loop
    #   this wasn't referenced, I created from scratch

    ####################

    print("Select ratio of train/test set...\n")  # tells user to select
    print("#\tTrain\tTest")  # headings
    print("1\t50%\t50%")  # 50/50 split
    print("2\t60%\t40%")  # 60/40 split
    print("3\t70%\t30%")  # 70/30 split
    print("4\t80%\t20%")  # 80/20 split
    print("5\t90%\t10%\n")  # 90/10 split

    while True:  # enter inifinite loop, incorrect commands will return here

        usr_ratio = input("Choose from numbers 1-5 and press Enter...\n")  # user inputs num 1-5

        idx = 2500  # index is 2500 by default - 50/50 split

        if usr_ratio == '1':
            idx = 2500  # user selects '1', 50/50 split
            break  # exit from infinite loop
        elif usr_ratio == '2':
            idx = 3000  # user selects '2', 60/40 split
            break  # exit from infinite loop
        elif usr_ratio == '3':
            idx = 3500  # user selects '3', 70/30 split
            break  # exit from infinite loop
        elif usr_ratio == '4':
            idx = 4000  # user selects '4', 80/20 split
            break  # exit from infinite loop
        elif usr_ratio == '5':
            idx = 4500  # user selects '5', 90/10 split
            break  # exit from infinite loop

        else:  # user fails to enter 1-5
            print("Command not recognised.\n")  # user returns to beginning of loop to enter 1-5 again

    training_set = neg_samples[:idx] + pos_samples[:idx]  # training data set is defined using index selected by user
    test_set = neg_samples[idx:] + pos_samples[idx:]  # test data set is defined using index selected by user
    print("Total size of training set:\t\t", len(training_set))  # prints size of train set
    print("Total size of test set:\t\t\t", len(test_set))  # prints size of test set

    ####################

    #   this section creates sentiment analysis classifier
    #   and trains with training data set

    ####################

    print("\n")  # white space

    # trains classifier with training set
    sentiment_classifier = NaiveBayesClassifier.train(training_set)

    ####################

    #   this section tests the classifier
    #   with test data set and prints accuracy

    ####################

    accuracy = nltk.classify.util.accuracy(sentiment_classifier, test_set)
    # prints 'Accuracy:' with the accuracy percentage
    print("Sentiment analysis classifier has been trained and tested. Accuracy:", accuracy * 100, "%")

    # user is given option to save the classifer with this accuracy, or quit if they do not want to save
    usr_choice = input('To save the NaiveBayesClassifier, press type "s" then press Enter...\nTo quit, type "q" then press Enter...')

    ######################

    #   user chooses to quit
    #   program quits

    ######################

    if usr_choice == 'q':
        False

    ######################

    #   user chooses to save classifier
    #   classifier is saved to pickle file

    ######################

    elif usr_choice == 's':
        # this section saves trained classifier to pickle file to be imported for sentiment analysis
        f = open('naivebayes.pickle', 'wb')
        pickle.dump(sentiment_classifier, f)
        f.close()
        print("Classifier was saved successfully: naivebayes.pickle")  # user friendly info - shows file name

    else:
        print("Command not recognised.")
        False


################################################################################

#       IF / ELIF / ELSE
#       elif
#       user selects test the pre-existing classifier

################################################################################

elif answer == usr_tst:
    f = open('naivebayes.pickle', 'rb')  # pickle is opened
    myClassifier = pickle.load(f)  # assigned to myClassifier
    f.close()

    sentence = input("Enter a sentence to test: ")  # user is asked to input a sentence to test

    text = pp.clean(sentence)  # sentence is tweet preprocessed - in case they copy in a tweet
    tokens = [term for term in myTokenizer(text) if term not in stop_words]  # calls myTokenizer function and tokenizes
    features = myFeatures(tokens)  # appends 'True' to tokens
    print(myClassifier.classify(features))  # prints whether its pos or neg

################################################################################

#       IF / ELIF / ELSE
#       else
#       user selects neither train or test
#       program quits - user can follow instruction manual to restart

################################################################################

else:
    input("Command not recognised. Press Enter to quit...")  # user hits enter and program quits
    False
