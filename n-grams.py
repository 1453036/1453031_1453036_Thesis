import numpy
import pickle #built-in file handling module from python
import sys, getopt  #handling commandline params
import os #delete temp file, see saveToFile function for more


#use numpy only
#data file with format, "sequence label"

class glbClass: #singleton class, contains global properties , just for encapsulation
    # Here will be the instance stored.
    __instance = None
    __currentDatasetIndx = 0
    __resultDir = './result/'
    __dataOffset = [0,0,0] #number of data [unlabeled, svr, non-svr]

    data = numpy.array([]) #contain data read from file, type array of strings
    target = numpy.array([],  dtype = str) # array of labels
    numberOfAttr = 0
    listOfAttr = {} #type: dictionary ,template: {attrName1: index,attrName2: index + 1 , ...}, attribute collection from extracting whole dataset
    opts = getopt.getopt(sys.argv[1:],"u:s:n:") # u: unlabeled data file, s: svr data file, n: non-svr data file

    fileList = numpy.array(["./data/unlabeled.txt", "./data/svr.txt", "./data/non-svr.txt"], dtype = str) #read from agr if agr provided, default values for otherwise
    dataFileNames = numpy.array(["unlabeled-data.pkl", "svr-data.pkl", "non-svr-data.pkl"], dtype = str) #save finished data to file with default names
    targetFileNames = numpy.array(["unlabeled-target.pkl", "svr-target.pkl", "non-svr-target.pkl"], dtype = str) #save to finished target data to file with default names


    def init(self):
        for opt, arg in self.opts[0]:
            if opt  == "-u":
                self.fileList[0] = arg
            elif opt == "-s":
                self.fileList[1] = arg
            elif opt == "-n":
                self.fileList[2] = arg

    #doing with local attr
    def appendAttr(self, attrName):
        self.listOfAttr[attrName] = self.numberOfAttr
        self.numberOfAttr = self.numberOfAttr + 1
    def getAttrIndex(self, attrName):
        return self.listOfAttr[attrName]
    def appendTarget(self, label):
        self.target = numpy.append(self.target, label)

    #handling file
    def writeDownRecord(self, record):
        tempFile = open(self.__resultDir + 'temp', 'a')
        pickle.dump(record, tempFile) #write record down to file
        tempFile.close() #apply change to file and clear mem
    def saveToFile(self):
        #standardize data (zeros padding)
        targetFileName = self.__resultDir + self.targetFileNames[self.__currentDatasetIndx]
        numpy.savetxt('./' + targetFileName, self.target, fmt = '%s')
        print '---->Saved target to ' + self.__resultDir + targetFileName

        if(self.__currentDatasetIndx >= 2):


            currentOffset = 0
            currentLine = 0
            dataFileName = self.__resultDir + self.dataFileNames[currentOffset]

            print 'Standardize data and save to file...'
            tempFile = open(self.__resultDir + 'temp', 'r')
            print 'Reading temp file...'
            while True:
                try:
                    record = pickle.load(tempFile) #read record per time 
                    print 'Current line: ' + str(currentLine)
                    print 'Current offset: ' + str(currentOffset)
                    if(currentOffset <2 and currentLine == self.__dataOffset[currentOffset]):
                        print '---->Saved data to ' + self.__resultDir  + dataFileName
                        currentOffset = currentOffset + 1
                        dataFileName = self.__resultDir + self.dataFileNames[currentOffset]
                        print '-------->Reading offset: ' + str(currentOffset)
                    standardizedRecord = numpy.pad(record, (0, self.numberOfAttr - len(record)), 'constant')
                    dataFile = open(dataFileName, 'a') #encoding file, use pickle for file reading
                    pickle.dump(standardizedRecord, dataFile)
                    dataFile.close()
                    currentLine = currentLine + 1

                except(EOFError, pickle.UnpicklingError):
                    break

            attrListFile = open('./result/attr.pkl', 'w')
            pickle.dump(self.listOfAttr, attrListFile)
            attrListFile.close()
            print '---->Saved attr to ./result/attr.pkl'    

            os.remove(self.__resultDir + './temp') #clean out the temp file which occupy lot of space
            print '---->Remove temp file'

        self.__currentDatasetIndx = self.__currentDatasetIndx + 1


    def fetchDataSet(self):
        print '### Current dataset: ' + str(self.fileList[self.__currentDatasetIndx])
        self.data = numpy.genfromtxt(fname = self.fileList[self.__currentDatasetIndx], delimiter = ' ', dtype = (str,str))
        if(self.__currentDatasetIndx is 0):
            self.__dataOffset[self.__currentDatasetIndx] = len(self.data)
        else:
            self.__dataOffset[self.__currentDatasetIndx] =  self.__dataOffset[self.__currentDatasetIndx - 1] + len(self.data)
        print self.__dataOffset



    #---------------singleton implement------------ 
    @staticmethod
    def getInstance():
        """ Static access method. """
        if glbClass.__instance == None:
            glbClass()
        return glbClass.__instance 

    def __init__(self):
        """ Virtually private constructor. """
        if glbClass.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            # self.__middleFile.close() 
            os.mkdir('./result')
            glbClass.__instance = self
    #-----------------------------------------------


def slideWindow(sequence, window):
    extractSeq = sequence[window[0]:window[1]]
    window[0]+=1
    window[1]+=1
    return extractSeq

def ngram(ngramInstance, sequence, n):
    window = [0, n]
    glbObj = glbClass.getInstance()
    while(window[0] <= len(sequence) - n):
        extractSeq = slideWindow(sequence, window)
        if(extractSeq not in glbObj.listOfAttr): #case 1 : new attr found!
            glbObj.appendAttr(extractSeq)
            ngramInstance = numpy.append(ngramInstance, 1)
        else: #case 2: hit from old attr
            attrIndex = glbObj.getAttrIndex(extractSeq)
            ngramInstance[attrIndex] = ngramInstance[attrIndex] + 1
    # print ngramInstance
    return ngramInstance
def loopNgram(dataTuple):
    print 'Start parsing...'
    # print dataTuple
    # print '------------------------'
    sequence = dataTuple[0]
    label = dataTuple[1]
    glbObj = glbClass.getInstance()
    previousNumberOfAttr = glbObj.numberOfAttr #for monitoring logs purpose 
    ngramInstance = numpy.zeros((glbObj.numberOfAttr), dtype=int) #init ngramInstance with already-created attributes
    for i in range(1,40):
        ngramInstance = ngram(ngramInstance, sequence, i) 
    print '->Finish parsing!'
    print '+Current number of attr: ' + str(glbObj.numberOfAttr)
    print 'Increased: ' + str(glbObj.numberOfAttr - previousNumberOfAttr) 
    print '----------------------------------------'
    glbObj.writeDownRecord(ngramInstance)
    glbObj.appendTarget(label)

glbObj = glbClass.getInstance()

def analyze(dataset):
    print 'Total: ' + str(len (dataset))
    print '---------------------------'
    # print glbObj.data
    for index in range(0, len(dataset)):
        # print glbObj.data[index]
        print '-Current tuple index: ' + str(index)
        loopNgram(dataset[index])
    glbObj.saveToFile()




glbObj.init()
print glbObj.fileList

glbObj.fetchDataSet()
analyze(glbObj.data)
glbObj.fetchDataSet()
analyze(glbObj.data)
glbObj.fetchDataSet()
analyze(glbObj.data)

# print glbObj.listOfAttr