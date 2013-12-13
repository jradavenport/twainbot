
import nltk
import re
import pickle


raw = open('tom_sawyer_shrt.txt').read()

### this is how the basic Punkt sentence tokenizer works
#sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')
#sents = sent_tokenizer.tokenize(raw)

### train & tokenize text using text
sent_trainer = nltk.tokenize.punkt.PunktSentenceTokenizer().train(raw)
sent_tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer(sent_trainer)
# break in to sentences
sents = sent_tokenizer.tokenize(raw)
# get sentence start/stop indexes
sentspan = sent_tokenizer.span_tokenize(raw)



###  Remove \n in the middle of setences, due to fixed-width formatting
for i in range(0,len(sents)-1):
    sents[i] = re.sub('(?<!\n)\n(?!\n)',' ',raw[sentspan[i][0]:sentspan[i+1][0]])

for i in range(1,len(sents)):
    if (sents[i][0:3] == '"\n\n'):
        sents[i-1] = sents[i-1]+'"\n\n'
        sents[i] = sents[i][3:]


### Loop thru each sentence, fix to 140char
i=0
tweet=[]
while (i<len(sents)):
    if (len(sents[i]) > 140):
        ntwt = int(len(sents[i])/140) + 1
        words = sents[i].split(' ')
        nwords = len(words)
        for k in range(0,ntwt):
            tweet = tweet + [
                re.sub('\A\s|\s\Z', '', ' '.join(
                words[int(k*nwords/float(ntwt)):
                      int((k+1)*nwords/float(ntwt))]
                ))]
        i=i+1
    else:
        if (i<len(sents)-1):
            if (len(sents[i])+len(sents[i+1]) <140):
                nextra = 1
                while (len(''.join(sents[i:i+nextra+1]))<140):
                    nextra=nextra+1
                tweet = tweet+[
                    re.sub('\A\s|\s\Z', '',''.join(sents[i:i+nextra]))
                    ]        
                i = i+nextra
            else:
                tweet = tweet+[re.sub('\A\s|\s\Z', '',sents[i])]
                i=i+1
        else:
            tweet = tweet+[re.sub('\A\s|\s\Z', '',sents[i])]
            i=i+1


### A last pass to clean up leading/trailing newlines/spaces.
for i in range(0,len(tweet)):
    tweet[i] = re.sub('\A\s|\s\Z','',tweet[i])

for i in range(0,len(tweet)):
    tweet[i] = re.sub('\A"\n\n','',tweet[i])


###  Save tweets to pickle file for easy reading later
output = open('tweet_list.pkl','wb')
pickle.dump(tweet,output,-1)
output.close()


listout = open('tweet_lis.txt','w')
for i in range(0,len(tweet)):
    listout.write(tweet[i])
    listout.write('\n-----------------\n')

listout.close()

