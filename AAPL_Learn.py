
from pymongo import MongoClient
import re
from textblob import TextBlob
from ffnet import ffnet, mlgraph, readdata
import sys
import numpy
from pylab import *

def normalize(mx, mn, val):
    return ((val-mn)/(mx-mn))

def learn(inputD,outputData):
    conec = mlgraph((2,22,12,1))
    net = ffnet(conec)
    print("READING DATA")
    inputData = inputD
    target = numpy.array(outputData)#data[:, -1] #last column

    print ("TRAINING NETWORK...")
    sys.stdout.flush()
    net.train_tnc(inputData, target, maxfun = 5000, messages=1)
    print ("TESTING NETWORK...")
    output, regression = net.test(inputData, target, iprint = 0)
    print(regression)
    Rsquared = regression[0][2]
    maxerr = abs( numpy.array(output).reshape( len(output) ) - numpy.array(target) ).max()
    print ("R-squared:           %s  (should be >= 0.999999)" %str(Rsquared))
    print ("max. absolute error: %s  (should be <= 0.05)" %str(maxerr))
    print ("Is ffnet ready for a stock?")
    try:
        plot( target, 'b--' )
        plot( output, 'k-' )
        legend(('target', 'output'))
        xlabel('pattern'); ylabel('price')
        title('Outputs vs. target of trained network.')
        grid(True)
        show()
        return net
    except ImportError:
        print ("Cannot make plots. For plotting install matplotlib.\n%s" % e)
        return net

def main():
    client = MongoClient()
    client = MongoClient('mongodb://localhost:27017/')
    db = client['tweets']
    collection= db['rawTweets']
    total_during_sen=[]
    total_during_sub=[]
    total_after_sen=[]
    total_after_sub=[]
    total_justopening_sub=[]
    total_justopening_sen=[]
    total_justclosing_sub=[]
    total_justclosing_sen=[]

    dateAfter = 'Nov %02d 0[0-9]:[0-5][0-9]:[0-5][0-9]|1[1-3]:[0-5][0-9]:[0-5][0-9]|14:[0-2][0-9]:[0-5][0-9]|2[1-3]:[0-5][0-9]:[0-5][0-9]'
    dateDuring = 'Nov %02d 14:[3-5][0-9]:[0-9][0-9]|2[0-1]:[0-5][0-9]:[0-5][0-9]|1[5-9]:[0-5][0-9]:[0-5][0-9]'
    datejustopening=  'Nov %02d 09:[0-2][0-9]:[0-5][0-9]'
    datejustclosing = 'Nov %02d 03:[3-5][0-9]:[0-9][0-9]'
    for j in range(3,31):
        during=collection.find({'date': {'$regex': dateDuring%j}})
        after=collection.find({'date': {'$regex': dateAfter%j}})
        justopening=collection.find({'date': {'$regex': datejustopening%j}})
        justclosing=collection.find({'date': {'$regex': datejustclosing%j}})
        during_sen=0
        during_sub=0
        during_total=0
        after_sen=0
        after_sub=0
        after_total=0
        justclosing_total=0
        justopening_total=0
        justopening_sen=0
        justopening_sub=0
        justopening_total=0
        justclosing_sen=0
        justclosing_sub=0
        justclosing_total=0


        for i in during:
            blob = TextBlob(i['text'])
            during_sen+=blob.sentiment.polarity
            during_sub+=blob.sentiment.subjectivity
            during_total+=1

        for i in after:
            blob = TextBlob(i['text'])
            after_sen+=blob.sentiment.polarity
            after_sub+=blob.sentiment.subjectivity
            after_total+=1

        for i in justopening:
            blob = TextBlob(i['text'])
            justopening_sen+=blob.sentiment.polarity
            justopening_sub+=blob.sentiment.subjectivity
            justopening_total+=1

        for i in justclosing:
            blob = TextBlob(i['text'])
            justclosing_sen+=blob.sentiment.polarity
            justclosing_sub+=blob.sentiment.subjectivity
            justclosing_total+=1


        normalized_during_sen=-1 + (2*normalize(during_total,-during_total,during_sen))
        normalized_during_sub=normalize(during_total,0,during_sub)
        normalized_after_sen=-1 + (2*normalize(after_total,-after_total,after_sen))
        normalized_after_sub=normalize(after_total,0,after_sub)

        normalized_justclosing_sen=-1 + (2*normalize(justclosing_total,-justclosing_total,justclosing_sen))
        normalized_justclosing_sub=normalize(justclosing_total,0,justclosing_sub)
        normalized_justopening_sen=-1 + (2*normalize(justopening_total,-justopening_total,justopening_sen))
        normalized_justopening_sub=normalize(justopening_total,0,justopening_sub)


        total_during_sen.append(normalized_during_sen)
        total_after_sen.append(normalized_after_sen)
        total_during_sub.append(normalized_during_sub)
        total_after_sub.append(normalized_after_sub)

        total_justopening_sub.append(normalized_justopening_sub)
        total_justopening_sen.append(normalized_justopening_sen)
        total_justclosing_sub.append(normalized_justclosing_sub)
        total_justclosing_sen.append(normalized_justclosing_sen)


    normalized_after=numpy.column_stack((total_after_sen,total_after_sub))
    normalized_during=numpy.column_stack((total_during_sen,total_during_sub))
    Date=[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
    aaplStoxOpen=[120.79,122.56,121.85,121.08,121,121,120.96,116.9,116.37,116.26,115.2,114.2,112.3,111.38,114.92,115.76,117.64,119.2,119.2,119.2,119.27,117.33,119.21,118.8,118.29,118.3,118.4,118.49]
    aaplStoxClose=[122.57,122,120.92,121.06,120.9,120.7,120.57,116.77,116.11,115.72,112.34,112.8,113.7,114.18,113.69,117.29,118.78,119.3,118.9,118.1,117.75,118.88,118.03,117.9,117.81,117.9,118.2,118.3]
    model_after=learn(normalized_after,aaplStoxOpen)
    model_before=learn(normalized_during,aaplStoxClose)

if __name__ == "__main__":
    main()
