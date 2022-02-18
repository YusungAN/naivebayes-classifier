
import pickle
import math
from collections import defaultdict
import sys
import re
import pandas as pd
from collections import defaultdict
from PyKomoran import *

with open('text.p', 'rb') as f:
    x_data = pickle.load(f)

sentence = sys.argv[1]

stop_words = 'ㄴ 아 의 에 었 던 는데 어 안 에 100년 10년 ㄴ다 ㄹ ㄴ데 을 를 ㅁ 것 바 수 터 게 처럼 고 랑 다 겠 지 이 가 은 는 하'

n_word_in_normal = 0
n_word_in_bias = 0
normal_txt = x_data[x_data['bias'] == 0]['comments']
bias_txt = x_data[x_data['bias'] == 1]['comments']

for i in normal_txt:
    n_word_in_normal += len(i)
for i in bias_txt:
    n_word_in_bias += len(i)
n_normal = len(x_data[x_data['bias'] == 0])
n_bias = len(x_data[x_data['bias'] == 1])

word_dict = defaultdict(lambda: [0, 0]) # [정상 댓글 속에서의 단어 갯수, 혐오 댓글 속의 단어개수]

for i in x_data[x_data['bias'] == 0]['comments']:
    for j in i:
        word_dict[j][0] += 1

for i in x_data[x_data['bias'] == 1]['comments']:
    for j in i:
        word_dict[j][1] += 1



p_bias = x_data['bias'].mean()
p_normal = 1 - x_data['bias'].mean()

komoran = Komoran("STABLE")

def text_preprocessing(x):
    res = []
    x = re.sub('[,|(|).|!|?|;●|:|‘|’|★|♥|★|♨|^|♡|~|ㆍ|*|=|+|-|@|#|$|%|&]', '', x)
    x = re.sub(r'\d+', '', x)
    x = komoran.get_nouns(x)
    for i in x:
        if i not in stop_words:
            res.append(i);
    return res


def naive_bayes_predict(x):
    laplace_smoothing = 0.5

    tokens = text_preprocessing(x)
    normal_pred_p_log = 0
    bias_pred_p_log = 0
    for i in tokens:
        normal_pred_p_log += math.log((word_dict[i][0]*word_dict[i][0]*word_dict[i][0] + laplace_smoothing)/n_word_in_normal)
        bias_pred_p_log += math.log((word_dict[i][1]*word_dict[i][1]*word_dict[i][0] + laplace_smoothing)/n_word_in_bias)
    normal_pred_p_log += math.log(p_normal)
    bias_pred_p_log += math.log(p_bias)
    return bias_pred_p_log > normal_pred_p_log

print(naive_bayes_predict(sentence))
sys.stdout.flush()
