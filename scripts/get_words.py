# get n most popular english words

# Use Peter Norvig's list of 1/3 million most frequent words according to
# Google ngram (norvig.com/ngrams) (norvig.com/ngrams/count_1w.txt)

n = 50000
words = []

with open('count_1w.txt') as f:
    for i, line in enumerate(f):
        if i == n:
            break
        words.append(line.split()[0])

txt = open('words.txt', 'w+')
for item in words:
    txt.write(item + '\n')
