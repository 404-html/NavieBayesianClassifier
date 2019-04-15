class readStopWord:
    def readStopWord(self,filename):
        stopword = []
        f = open(filename,"r", encoding='utf-8')
        for i in f.readlines():
            stopword.append(i.strip('\n').strip(' '))
        return stopword

if __name__ == '__main__':
    so = readStopWord()
    print(so.readStopWord('stopwords.txt'))