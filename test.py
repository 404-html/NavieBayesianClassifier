import glob
import numpy as np


def readStopWord(filename):
    stopword = []
    f = open(filename, "r")
    for i in f.readlines():
        stopword.append(i.strip('\n').strip(' '))
    return stopword

filename = 'stopwords.txt'
common_words = readStopWord(filename)

# 处理训练集，每类文本存在一个字典，一个20个字典，全都保存在一个数组
def loadtrainData(filename, trainlist, start, end):
    # output: train包含20个字典，每个字典是每一类中的出现次数为前1000名的单词和对应的出现次数
    counttag = []
    train = []
    for f in filename:
        d = {}
        for i in range(start, end):
            with open(f[i], 'r', errors="ignore") as fn:
                data = fn.readlines()
                for line in data:
                    line = line.strip()
                    i = 0
                    while i < len(line):
                        word = ""
                        if not valid(line[i]):
                            i += 1
                            continue
                        while i < len(line) and valid(line[i]):
                            if 'A' <= line[i] <= 'Z':
                                word += line[i].lower()
                            else:
                                word += line[i]
                            i += 1
                        if word in common_words or len(word) is 1:
                            continue
                        if word in d.keys():
                            d[word] = d.get(word)+1
                        else:
                            d[word] = 1
        # 20个字典，每个字典是每一类中的单词和出现次数
        trainlist.append(d)
    for num in range(len(trainlist)):
        d, count = extractfeature(trainlist[num], 100)
        train.append(d)
        counttag.append(count)
    # train包含20个字典，每个字典是每一类中的出现次数为前1000名的单词和对应的出现次数
    print("读取训练数据完毕")
    return train, counttag


# 提取这一类中前1000(num)个频率最高的词，存在字典里
def extractfeature(datadict, num):
    d = {}
    times = 0
    count = 0
    # drop = 0
    # while drop < 100:
    #     maxkey = max(datadict, key=datadict.get)
    #     del datadict[maxkey]
    #     drop += 1
    while times < num:
        maxkey = max(datadict, key=datadict.get)
        d[maxkey] = datadict.get(maxkey)
        count += datadict.get(maxkey)
        del datadict[maxkey]
        times += 1
    return d, count


def valid(c):
    if 'a' <= c <= 'z' or 'A' <= c <= 'Z' or '0' <= c <= '9':
        return True
    else:
        return False


# testdata里面只有一个字典元素，存的是测试文本中的单词和出现次数
def nb(traindata, counttag, testdict):
    maxpb = (-2147483647 - 1)
    maxindex = 0
    for i in range(len(traindata)):
        pb = 1
        for d in testdict.keys():
            if d in traindata[i]:
                num = traindata[i].get(d)
                # pb *= pow((num + 1) / (counttag[i] + len(traindata[i])), testdict.get(d))
                # 避免概率相乘向下溢出，用log处理结果
                pb += np.log((num+1)/(counttag[i]+len(traindata[i])))*testdict.get(d)
            else:
                # pb *= (num + 1) / (counttag[i] + len(traindata[i]))
                pb += np.log(1/(counttag[i]+len(traindata[i])))
        # print("i:", i)
        # print("pb:", pb)
        # print("maxpb:", maxpb)
        if pb > maxpb:
            maxpb = pb
            maxindex = i
        # print("maxindex:", maxindex)
    return maxindex


def testdata(filename):
    d = {}
    with open(filename, 'r',  errors="ignore") as fn:
        data = fn.readlines()
        for line in data:
            line = line.strip()
            i = 0
            while i < len(line):
                word = ""
                if not valid(line[i]):
                    i += 1
                    continue
                while i < len(line) and valid(line[i]):
                    if 'A' <= line[i] <= 'Z':
                        word += line[i].lower()
                    else:
                        word += line[i]
                    i += 1
                if word in common_words:
                    continue
                if word in d.keys():
                    d[word] = d.get(word) + 1
                else:
                    d[word] = 1
    # print("d:", len(d))
    # res, count = extractfeature(d, len(d))
    # print("d:", d)

    return d

# groupsum存了20个列表（20个类名），每个子列表里存了1000个文件名
def accuracy(groupsum, traindata, countdata):
    count = 0
    for i in range(len(groupsum)):
        if i is 15:
            for j in range(10, 20):
                test = testdata(groupsum[i][j])
                index = nb(traindata, countdata, test)
                if index is i:
                    count += 1
            print("读取验证数据完毕")
        else:
            for j in range(10, 20):
                # print(len(groupsum[15]))
                test = testdata(groupsum[i][j])
                index = nb(traindata, countdata, test)
                # print("index:", index)
                # print("i:", i)
                if index is i:
                    count += 1
            print("读取验证数据完毕")
    accuracy = count/(10*len(groupsum))
    # accuracy = count / 2
    print("final count:", count)
    return accuracy


if __name__ == "__main__":
    groupsum = []
    groupsum.append(glob.glob(r'20_newsgroups/alt.atheism/*'))
    groupsum.append(glob.glob(r'20_newsgroups/comp.graphics/*'))
    groupsum.append(glob.glob(r'20_newsgroups/comp.os.ms-windows.misc/*'))
    groupsum.append(glob.glob(r'20_newsgroups/comp.sys.ibm.pc.hardware/*'))
    groupsum.append(glob.glob(r'20_newsgroups/comp.sys.mac.hardware/*'))
    groupsum.append(glob.glob(r'20_newsgroups/comp.windows.x/*'))
    groupsum.append(glob.glob(r'20_newsgroups/misc.forsale/*'))
    groupsum.append(glob.glob(r'20_newsgroups/rec.autos/*'))
    groupsum.append(glob.glob(r'20_newsgroups/rec.motorcycles/*'))
    groupsum.append(glob.glob(r'20_newsgroups/rec.sport.baseball/*'))
    groupsum.append(glob.glob(r'20_newsgroups/rec.sport.hockey/*'))
    groupsum.append(glob.glob(r'20_newsgroups/sci.crypt/*'))
    groupsum.append(glob.glob(r'20_newsgroups/sci.electronics/*'))
    groupsum.append(glob.glob(r'20_newsgroups/sci.med/*'))
    groupsum.append(glob.glob(r'20_newsgroups/sci.space/*'))
    groupsum.append(glob.glob(r'20_newsgroups/soc.religion.christian/*'))
    groupsum.append(glob.glob(r'20_newsgroups/talk.politics.guns/*'))
    groupsum.append(glob.glob(r'20_newsgroups/talk.politics.mideast/*'))
    groupsum.append(glob.glob(r'20_newsgroups/talk.politics.misc/*'))
    groupsum.append(glob.glob(r'20_newsgroups/talk.religion.misc/*'))
    # common_words = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not',
    #                 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they',
    #                 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my',
    #                 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if',
    #                 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like',
    #                 'time', 'no', 'just', 'him',
    #                 'know', 'take', 'people', 'into', 'year',
    #                 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then',
    #                 'now', 'look', 'only', 'some',
    #                 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how',
    #                 'our', 'work', 'first', 'well',
    #                 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us', 'is', 'are',
    #                 'was', 'were', 'am', '\n']

    trainlist = []
    traindata, counttag = loadtrainData(groupsum, trainlist, 0, 10)
    print(traindata)
    # accuracy(groupsum, traindata, counttag)










# import glob
# import numpy as np
#
# def loadtrainData(filename, trainlist, start, end):
#     counttag = []
#     for f in filename:
#         d = {}
#         count = 0
#         for i in range(start, end):
#             with open(f[i], 'r') as fn:
#                 data = fn.readlines()
#                 for line in data:
#                     line = line.strip()
#                     i = 0
#                     while i < len(line):
#                         word = ""
#                         if not valid(line[i]):
#                             i += 1
#                             continue
#                         while i < len(line) and valid(line[i]):
#                             if 'A' <= line[i] <= 'Z':
#                                 word += line[i].lower()
#                             else:
#                                 word += line[i]
#                             i += 1
#                         if word in common_words:
#                             continue
#                         count += 1
#                         if word in d.keys():
#                             d[word] = d.get(word)+1
#                         else:
#                             d[word] = 1
#         counttag.append(count)
#         print(d, count)
#         trainlist.append(d)   #20个字典，每个字典是每一类中的单词和出现次数
#         # print(counttag)
#         # print(len(trainlist))
#     return trainlist, counttag
#
#
# def valid(c):
#     if 'a' <= c <= 'z' or 'A' <= c <= 'Z' or '0' <= c <= '9':
#         return True
#     else:
#         return False
#
#
# def nb(traindata, counttag, testdata):  #testdata里面只有一个字典元素，存的是测试文本中的单词和出现次数
#     testdict = testdata[0]
#     maxpb = (-2147483647 - 1)
#     maxindex = 0
#     for i in range(len(traindata)):
#         pb = 1
#         for d in testdict.keys():
#             if d in traindata[i]:
#                 num = traindata[i].get(d)
#                 pb += np.log(num/counttag[i])*testdict.get(d)
#             else:
#                 pb += np.log(1/(counttag[i]+len(testdict)))
#         print("i:", i)
#         print("pb:", pb)
#         print("maxpb:", maxpb)
#         if pb > maxpb:
#             maxpb = pb
#             maxindex = i
#         print("maxindex:", maxindex)
#     return maxindex
#
#
# def testdata(filename):
#     test = []
#     d = {}
#     print("test filename: ", filename)
#     with open(filename, 'r') as fn:
#         data = fn.readlines()
#         for line in data:
#             line = line.strip()
#             i = 0
#             while i < len(line):
#                 word = ""
#                 if not valid(line[i]):
#                     i += 1
#                     continue
#                 while i < len(line) and valid(line[i]):
#                     if 'A' <= line[i] <= 'Z':
#                         word += line[i].lower()
#                     else:
#                         word += line[i]
#                     i += 1
#                 if word in common_words:
#                     continue
#                 if word in d.keys():
#                     d[word] = d.get(word) + 1
#                 else:
#                     d[word] = 1
#     test.append(d)
#     return test
#
#
# #groupsum存了20个列表（20个类名），每个子列表里存了1000个文件名
# def accuracy(groupsum, traindata, countdata):
#     count = 0
#     # for i in range(0, 1):
#     for i in range(len(groupsum)):
#         for j in range(2, 4):
#             # print(len(groupsum[15]))
#             test = testdata(groupsum[i][j])
#             index = nb(traindata, countdata, test)
#             # print("index:", index)
#             # print("i:", i)
#             if index is i:
#                 count += 1
#     accuracy = count/(2*len(groupsum))
#     print(accuracy)
#     return accuracy
#
#
# if __name__ == "__main__":
#     groupsum = []
#     groupsum.append(glob.glob(r'news/aa/*'))
#     groupsum.append(glob.glob(r'news/bb/*'))
#     common_words = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not',
#                     'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they',
#                     'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my',
#                     'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if',
#                     'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like',
#                     'time', 'no', 'just', 'him',
#                     'know', 'take', 'people', 'into', 'year',
#                     'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then',
#                     'now', 'look', 'only', 'some',
#                     'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how',
#                     'our', 'work', 'first', 'well',
#                     'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us']
#     trainlist = []
#     traindata, counttag = loadtrainData(groupsum, trainlist, 0, 2)
#     accuracy(groupsum, traindata, counttag)
#     # nb(traindata, counttag, testdata)
