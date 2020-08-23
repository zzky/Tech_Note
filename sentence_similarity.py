import re
from datetime import datetime

import pandas as pd
import spacy
import math

from sklearn.cluster import KMeans
import numpy as np

from sen2vec import Word, Sentence, sentence_to_vec

from gensim.parsing.preprocessing import STOPWORDS
from gensim.utils import simple_preprocess


import matplotlib.pyplot as plt
import seaborn as sns

from scipy.spatial.distance import cdist



def read_data(filepath, outputPath):
    f = open(filepath)
    result = []
    pattern = '[a-z0-9][A-Z]'
    pattern2 = 'BPM[A-Z]'
    for line in f:
        if line.startswith('When compared with'):
            tmp = re.sub(pattern, lambda x: x.group(0)[0] + '\t' + x.group(0)[1:], line)
            tmp = re.sub(pattern2, lambda x: x.group(0)[0:3] + '\t' + x.group(0)[3:], tmp)
            result.append(tmp)
    f.close()
    pattern_time1 = '\d{2}[- ][A-Za-z]{3}[- ]\d{2,4}( \d{2}:\d{2})?'
    pattern_time2 = '\d{1,2}/\d{1,2}/\d{2,4}( \d{1,2}:\d{1,2}:\d{1,2} AM|PM)?'
    pattern_note1 = ',( )?(\(unconfirmed\))?(.*)(Confirmed by)'
    pattern_note2 = ',( )?(\(unconfirmed\))?(.*)(Reconfirmed by)'
    pattern_note3 = ',( )?(\(unconfirmed\))?(.*)(Electronically by)'
    pattern_note4 = ',( )?(\(unconfirmed\))?(.*)(Electronically signed by)'
    pattern_note5 = ',( )?(\(unconfirmed\))?(.*)(Electronically re-signed by)'
    pattern_note6 = ',( )?(\(unconfirmed\))?(.*)(-----------------------------------------)'
    data = []
    # for item in result:
    #     if re.search(pattern_note,item):
    #         print(re.search(pattern_note,item).group(3))
    # print(result[12])
    # print(re.search(pattern_note,result[12]).group(3))
    for item in result:
        if re.search(pattern_time1, item) and re.search(pattern_time2, item) and (
                re.search(pattern_note1, item) or re.search(pattern_note2, item) or re.search(pattern_note3, item) or re.search(pattern_note4, item) or re.search(pattern_note5, item) or re.search(pattern_note6, item)):
            tmp = []
            time1 = formatTime(re.search(pattern_time1, item).group())
            time2 = formatTime(re.search(pattern_time2, item).group())
            tmp.append(time1)
            tmp.append(time2)
            duration = datetime.strptime(time2, '%Y-%m-%d') - datetime.strptime(time1, '%Y-%m-%d')
            tmp.append(duration.days)
            if re.search(pattern_note1, item):
                tmp.append(re.search(pattern_note1, item).group(3).strip())
            elif re.search(pattern_note2, item):
                tmp.append(re.search(pattern_note2, item).group(3).strip())
            elif re.search(pattern_note3, item):
                tmp.append(re.search(pattern_note3, item).group(3).strip())
            elif re.search(pattern_note4, item):
                tmp.append(re.search(pattern_note4, item).group(3).strip())
            elif re.search(pattern_note5, item):
                tmp.append(re.search(pattern_note5, item).group(3).strip())
            elif re.search(pattern_note6, item):
                tmp.append(re.search(pattern_note6, item).group(3).strip())
            data.append(tmp)
    df = pd.DataFrame(data=data, columns=['Last Time', 'Test Time','Duration','Note'])
    df.to_csv(outputPath, index=None)
    return df


def formatTime(time):
    pattern1 = '(\d{2}-[A-Za-z]{3}-\d{4})( \d{2}:\d{2})?'
    pattern2 = '(\d{2}-[A-Za-z]{3} \d{4})( \d{2}:\d{2})?'
    pattern3 = '(\d{1,2}/\d{1,2}/\d{4})( \d{1,2}:\d{1,2}:\d{1,2} AM|PM)?'
    pattern4 = '(\d{1,2}/\d{1,2}/\d{2})( \d{1,2}:\d{1,2}:\d{1,2} AM|PM)?'
    result = ''
    if re.search(pattern1, time):
        result = datetime.strptime(re.search(pattern1, time).group(1), '%d-%b-%Y').strftime('%Y-%m-%d')
    elif re.search(pattern2, time):
        result = datetime.strptime(re.search(pattern2, time).group(1), '%d-%b %Y').strftime('%Y-%m-%d')
    elif re.search(pattern3, time):
        result = datetime.strptime(re.search(pattern3, time).group(1), '%m/%d/%Y').strftime('%Y-%m-%d')
    elif re.search(pattern4, time):
        result = datetime.strptime(re.search(pattern4, time).group(1), '%m/%d/%y').strftime('%Y-%m-%d')
    else:
        print(time)
    return result

def tokenize(text):
    return [token for token in simple_preprocess(text) if (token not in STOPWORDS)]


def l2_dist(v1, v2):
    sum = 0.0
    if len(v1) == len(v2):
        for i in range(len(v1)):
            delta = v1[i] - v2[i]
            sum += delta * delta
        return math.sqrt(sum)


def get_vec(data):
    embedding_size = 300
    sentences = []
    sentence_list = []
    origin_sentences = []
    duration_list = []
    nlp = spacy.load('en_core_web_lg')
    for index,row in data.iterrows():
        splited_sentences = row['Note'].split('\t')
        for sentence in splited_sentences:
            word_list = []
            for word in tokenize(sentence):
                token = nlp.vocab[word]
                if token.has_vector:
                    word_list.append(Word(word,token.vector))
            if len(word_list) > 0:
                sentence_list.append(Sentence(word_list))
                origin_sentences.append(sentence)
                duration_list.append(row['Duration'])

    # apply single sentence word embedding
    sentence_vector_lookup = dict()
    sentence_vectors = sentence_to_vec(sentence_list, embedding_size)  # all vectors converted together
    if len(sentence_vectors) == len(sentence_list):
        for i in range(len(sentence_vectors)):
            # map: text of the sentence -> vector
            sentence_vector_lookup[origin_sentences[i]] = sentence_vectors[i]
    return origin_sentences,duration_list,sentence_vectors


def draw_distribution(data,textPath, figurePath):
    f = open(textPath, 'w')
    plt.figure()
    for item in data['Note'].drop_duplicates().sort_values().tolist():
        f.write(item + '\n')
    f.close()
    sns.distplot(data['Duration'],bins=30).get_figure().savefig(figurePath)

    print(data['Duration'].value_counts().to_dict())


def hist_output(series,outputPath):
    series['Duration'].value_counts().sort_index().to_csv(outputPath)


if __name__ == '__main__':
    data = read_data('data/0-90.txt', 'data/0-90.csv')
    origin_sentences, duration_list, sentence_vectors = get_vec(data)
    X = np.array(sentence_vectors)

    # K = range(1, 30)
    # meandistortions = []
    # for k in K:
    #     kmeans = KMeans(n_clusters=k)
    #     kmeans.fit(X)
    #     meandistortions.append(sum(np.min(
    #         cdist(X, kmeans.cluster_centers_,
    #               'euclidean'), axi                                                                                       s=1)) / X.shape[0])
    # plt.plot(K, meandistortions, 'bx-')
    # plt.xlabel('k')
    # plt.ylabel(u'平均畸变程度')
    # plt.title(u'用肘部法则来确定最佳的K值')
    # plt.savefig('a.png')

    kmeans = KMeans(n_clusters=10)
    kmeans.fit(X)
    print(kmeans.score(X))
    df = pd.DataFrame(data={'Note':origin_sentences,'Duration':duration_list,'Class':kmeans.labels_})
    print(df)
    df.to_csv('data/result_180-270.csv',index=None)

    # data = pd.read_csv('data/result1.csv')
    #
    # s = data['Duration'].value_counts().sort_index()
    #
    # series1 = data[(data['Class'] == 1) & ((data['Note'].str.contains('No')) | (data['Note'].str.contains('no'))) & (data['Duration'] <= 180)]['Duration'].value_counts().sort_index()
    # series2 = data[(data['Class'] == 3) & (data['Duration'] <= 180) & ~(data['Note'].str.contains('shortened'))]['Duration'].value_counts().sort_index()
    # series3 = data[(data['Class'] == 5) & ~(data['Note'].str.contains('no longer')) & (data['Duration'] <= 180)]['Duration'].value_counts().sort_index()
    # series4 = data[(data['Note'].str.contains('Atrial fibrillation')) & ~(data['Note'].str.contains('replaced Atrial fibrillation')) & ~(data['Note'].str.contains('replaced  Atrial fibrillation')) & ~(data['Note'].str.contains('replaced   Atrial fibrillation')) & (data['Duration'] <= 180)]['Duration'].value_counts().sort_index()
    #
    # # print(sum[:10])
    # # print(series1[:10])
    # df = pd.concat([series1,s],axis=1).dropna()
    # df.columns = ['Count','Sum']
    # df['Percent'] = df.apply(lambda x: x['Count']/ x['Sum'], axis=1)
    # df.to_csv('series1.csv')
    # # print(df)
    # print(df.apply(sum))
    #
    # # plt.bar(df.index,df['Percent'])
    # plt.savefig('series1.png')

    # series2 = data[(data['Class'] == 3) & (data['Duration'] <= 30) & ~(data['Note'].str.contains('shortened'))]
    # series3 = data[(data['Class'] == 5) & ~(data['Note'].str.contains('no')) & (data['Duration'] <= 30)]
    # series4 = data[(data['Note'].str.contains('Atrial fibrillation')) & ~(data['Note'].str.contains('replaced Atrial fibrillation')) & ~(data['Note'].str.contains('replaced  Atrial fibrillation')) & ~(data['Note'].str.contains('replaced   Atrial fibrillation')) & (data['Duration'] <= 30)]
    # draw_distribution(series1,'output/series1.txt','output/series1.png')
    # draw_distribution(series2,'output/series2.txt','output/series2.png')
    # draw_distribution(series3,'output/series3.txt','output/series3.png')
    # draw_distribution(series4,'output/series4.txt','output/series4.png')

    # series1 = data[(data['Class'] == 1) & (data['Label'] == 'negative')]
    # series2 = data[(data['Class'] == 5) & ~(data['Note'].str.contains('shortened'))]
    # series3 = data[(data['Class'] == 3) & (data['Label'] == 'positive') ]
    # series4 = data[(data['Note'].str.contains('Atrial fibrillation')) & ~(
    #     data['Note'].str.contains('replaced Atrial fibrillation')) & ~(
    #     data['Note'].str.contains('replaced  Atrial fibrillation')) & ~(
    #     data['Note'].str.contains('replaced   Atrial fibrillation'))]
    #
    # hist_output(series1,'output/series1.csv')
    # hist_output(series2,'output/series2.csv')
    # hist_output(series3,'output/series3.csv')
    # hist_output(series4,'output/series4.csv')

