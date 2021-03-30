# import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()


import re
import string
import random
from nltk import FreqDist
from nltk import classify
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer


# gives the lemma of each given word
def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []

    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))

    return lemmatized_sentence


# removes hyperlinks, @mentions, stop words and punctuations from the tokens
def remove_noise(tweet_tokens, stop_words=()):
    cleaned_tokens = []
    lemmatizer = WordNetLemmatizer()

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())

    return cleaned_tokens


def get_all_words(cleaned_list):
    for tokens in cleaned_list:
        for token in tokens:
            yield token

def get_tweets_for_models(cleaned_tokens_list):
    for token_tweets in cleaned_tokens_list:
        yield dict(([token, True]) for token in token_tweets)

positive_tweets = twitter_samples.strings('positive_tweets.json')
negative_tweets = twitter_samples.strings('negative_tweets.json')
text = twitter_samples.strings('tweets.20150430-223406.json')
positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

stop_words = stopwords.words('english')

# print(pos_tag(tweet_tokens[0]))
# [('#FollowFriday', 'JJ'), ('@France_Inte', 'NNP'), ('@PKuchly57', 'NNP'), ('@Milipol_Paris', 'NNP'), ('for', 'IN'), ('being', 'VBG'), ('top', 'JJ'), ('engaged', 'VBN'), ('members', 'NNS'), ('in', 'IN'), ('my', 'PRP$'), ('community', 'NN'), ('this', 'DT'), ('week', 'NN'), (':)', 'NN')]

positive_cleaned_tokens_list = []
negative_cleaned_tokens_list = []

# cleaning the positive and negative tweets
for tokens in positive_tweet_tokens:
    positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

for tokens in negative_tweet_tokens:
    negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

positive_tokens_for_model = get_tweets_for_models(positive_cleaned_tokens_list)
negative_tokens_for_model = get_tweets_for_models(negative_cleaned_tokens_list)

#get the freqeuncy of words occured
# freq_dist_pos = FreqDist(positive_tokens_for_model)

positive_dataset = [([tweet_dict, 'Positive']) for tweet_dict in positive_tokens_for_model]
negative_dataset = [([tweet_dict, 'Negative']) for tweet_dict in negative_tokens_for_model]

dataset = positive_dataset + negative_dataset

random.shuffle(dataset)

train_data = dataset[:7000]
test_data = dataset[7000:]

#trained model is stored in classifier
classifier = NaiveBayesClassifier.train(train_data)

# print("Accuracy is: ", classify.accuracy(classifier, test_data))
# print(classifier.show_most_informative_features(10))

#testing on random tweet
# custom_tweet = "I ordered just once from TerribleCo, they screwed up, never used the app again."
custom_tweet = 'Thank you for sending my baggage to CityX and flying me to CityY at the same time. Brilliant service. #thanksGenericAirline'
custom_tokens = remove_noise(word_tokenize(custom_tweet))

print(classifier.classify(dict([token, True] for token in custom_tokens)))