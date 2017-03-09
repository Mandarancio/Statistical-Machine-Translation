def generate_ttable(source_path, target_path):
    monograms= {}
    bigrams = {}
    s_file = open(source_path)
    t_file = open(target_path)

    s_sentences = s_file.readlines()
    s_sentences = [(x.strip()+' *').split(' ') for x in s_sentences]
    t_sentences = t_file.readlines()
    t_sentences = [(x.strip()+' *').split(' ') for x in t_sentences]

    s_file.close()
    t_file.close()
    for i in range(0,len(s_sentences)):
        s= s_sentences[i]
        t= t_sentences[i]
        N = len(s)
        for j in range(0,N-1):
            si = s[j]
            ti = t[j]
            if si in monograms:
                if ti in monograms[si]:
                    monograms[si][ti]+=1
                else:
                    monograms[si][ti]=1
            else:
                monograms[si]={ti:1}
            si_p1 = s[j+1]
            ti_p1 = t[j+1]
            if (si,si_p1) in bigrams:
                if (ti,ti_p1) in bigrams[si,si_p1]:
                    bigrams[si,si_p1][ti,ti_p1]+=1
                else:
                    bigrams[si,si_p1][ti,ti_p1]=1
            else:
                bigrams[si,si_p1]={(ti,ti_p1):1}
    return monograms, bigrams

def translate_bigram(wi, wi_p1, monograms, bigrams):
    tw = '?'
    #back-off model
    p=0
    if (wi,wi_p1) in bigrams:
        for (tx,ty) in bigrams[wi,wi_p1]:
            prob = bigrams[wi,wi_p1][tx,ty]*monograms[wi][tx]
            if prob > p:
                p= prob
                tw = tx
    elif wi in monograms:
        for tx in monograms[wi]:
            prob = monograms[wi][tx]
            if prob>p:
                p=prob
                tw = tx
    return tw

def translate_sentence(sentence, monograms, bigrams):
    words = (sentence.strip()+' *').split(' ')
    translated = ''
    for i in range(0,len(words)-1):
        translated += translate_bigram(words[i],words[i+1],monograms,bigrams)+' '
    return translated

def translate_file(path, monograms, bigrams):
    with open(path) as f:
      content = f.readlines()
    for i in range(0,len(content)):
      p = content[i]
      print(str(i+1)+'\tS: '+p.strip())
      print('\tT: '+translate_sentence(p,monograms,bigrams))
      print()

source_path = "Arcturan1"
target_path = "centauri1"
sentences_path = "target"

monograms, bigrams = generate_ttable(source_path,target_path)
translate_file(sentences_path, monograms, bigrams)
