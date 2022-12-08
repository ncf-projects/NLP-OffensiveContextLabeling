
import csv
import gensim.downloader as api
import numpy as np
import re
import string

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from scipy import spatial

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

model = api.load("glove-twitter-50")


def compareScore(row, index, score_dict, count):
    if row[index] == "4.0":
        if float(row[13]) > score_dict[index][0]:
            score_dict[index] = (int(count), float(row[13]), str(row[14]))


def getSimilarityKey(training_dataset):

    score_dict = {
        3: (-1, -10, ""),   # sentiment_score
        4: (-1, -10, ""),   # respect_score
        5: (-1, -10, ""),   # insult_score
        6: (-1, -10, ""),   # humiliate_score
        7: (-1, -10, ""),   # status_score
        8: (-1, -10, ""),   # dehumanize_score
        9: (-1, -10, ""),   # violence_score
        10: (-1, -10, ""),  # genocide_score
        11: (-1, -10, ""),  # attack_defend_score
    }

    f = open(training_dataset, encoding="utf8")
    reader = csv.reader(f, delimiter=',')

    count = 0

    for row in reader:

        index = 3

        while index != 12:

            compareScore(row, index, score_dict, count)

            index += 1

        count += 1

    with open('SimilarityKey.txt', 'w'):
        print("Similarity Key created!")

    for key in score_dict:
        if score_dict[key][2] not in open('SimilarityKey.txt', 'r').read():
            with open('SimilarityKey.txt', 'a') as f:
                f.write(score_dict[key][2] + "\n")

    return open('SimilarityKey.txt', 'r').read()


def preprocessingText(input_text):

    # lowercase text
    input_text = input_text.lower()

    # remove numbers
    input_text = re.sub(r'\d+', '', input_text)

    # remove punctuation
    input_text = input_text.translate(
        str.maketrans("", "", string.punctuation))

    # remove whitespace
    input_text = input_text.strip()

    # tokenize
    tokens = word_tokenize(input_text)

    # removing stopwords
    tokens = [token for token in tokens if not token in stop_words]

    for token in tokens:

        # stemming words
        token = stemmer.stem(token)

        # lemmatizing words
        token = lemmatizer.lemmatize(token)

    return tokens


def getVector(input_text):

    return np.sum(np.array([model[token] for token in preprocessingText(input_text) if token in model]), axis=0)  # type: ignore


def getSimilarityScore(text1, text2):

    return 1-spatial.distance.cosine(getVector(text1), getVector(text2))


def main():

    training_dataset = "train.csv"

    similarityKey = getSimilarityKey(training_dataset)

    training_csv = open(training_dataset, encoding='utf8')
    reader = csv.reader(training_csv, delimiter=',')
    next(reader)

    point_nine_list = []
    point_eight_list = []
    point_seven_list = []
    point_six_list = []
    point_five_and_less_list = []

    with open("SimilarityResults.csv", 'w') as f:
        f.write("text,hate_speech_score,similarity_score")

    for row in reader:
        with open("SimilarityResults.csv", 'a', encoding='utf8', errors='ignore') as f:
            text = row[14]
            hate_speech_score = row[13]

            if (str(getVector(text)) != "0.0"):
                similarity_score = getSimilarityScore(text, similarityKey)
                f.write("\n" + text + "," + hate_speech_score +
                        "," + str(similarity_score))
                if (similarity_score >= 0.9):
                    point_nine_list.append(float(hate_speech_score))
                elif (0.8 <= similarity_score < 0.9):
                    point_eight_list.append(float(hate_speech_score))
                elif (0.7 <= similarity_score < 0.8):
                    point_seven_list.append(float(hate_speech_score))
                elif (0.6 <= similarity_score < 0.7):
                    point_six_list.append(float(hate_speech_score))
                elif (similarity_score < 0.6):
                    point_five_and_less_list.append(float(hate_speech_score))

            else:
                f.write("\n" + text + "," + hate_speech_score + "," + str(0.0))

    print("average hate speech score for 0.9+ similarity scores: " +
          str((sum(point_nine_list)/len(point_nine_list))))
    print("average hate speech score for 0.8-0.9 similarity scores: " +
          str((sum(point_eight_list)/len(point_eight_list))))
    print("average hate speech score for 0.7-0.8 similarity scores: " +
          str((sum(point_seven_list)/len(point_seven_list))))
    print("average hate speech score for 0.6-0.7 similarity scores: " +
          str((sum(point_six_list)/len(point_six_list))))
    print("average hate speech score for 0.0-0.5 similarity scores: " +
          str((sum(point_five_and_less_list)/len(point_five_and_less_list))))


if __name__ == "__main__":
    main()
