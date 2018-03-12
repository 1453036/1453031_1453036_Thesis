import numpy
import pickle #built-in file handling module from python

#use numpy only
#data file with format, "sequence label"

class glbClass: #singleton class, contains global properties , just for encapsulation
    # Here will be the instance stored.
    __instance = None

    data = numpy.array([]) #contain data read from file, type array of strings
    target = numpy.array([],  dtype = str) # array of labels
    numberOfAttr = 0
    listOfAttr = {} #type: dictionary ,template: {attrName1: index,attrName2: index + 1 , ...}, attribute collection from extracting whole dataset 
    finalMatrix = numpy.array([]) # final result (usable data)

    #private methods
    # def __standardizeData(self):
    #     for record in self.__middleMatrix:
    #         standardizedRecord = numpy.pad(record, (0, self.numberOfAttr - len(record)), 'constant')
    #         if(len(self.finalMatrix) is 0):
    #             self.finalMatrix = standardizedRecord
    #         else: 
    #             self.finalMatrix = numpy.vstack((self.finalMatrix, standardizedRecord))

    #public methods
    def appendAttr(self, attrName):
        self.listOfAttr[attrName] = self.numberOfAttr
        self.numberOfAttr = self.numberOfAttr + 1
    def getAttrIndex(self, attrName):
        return self.listOfAttr[attrName]
    # def appendRecord(self, record):
    #     self.__middleMatrix.append(record)
    #     return 1 
    def writeDownRecord(self, record):
        tempFile = open('temp', 'a')
        pickle.dump(record, tempFile) #write record down to file
        tempFile.close() #apply change to file and clear mem
    def saveToFile(self):
        #standardize data (zeros padding)
        print 'Standardize data and save to file...'
        tempFile = open('temp', 'r')
        while True:
            try:
                record = pickle.load(tempFile) #read record per time 
                standardizedRecord = numpy.pad(record, (0, self.numberOfAttr - len(record)), 'constant')
                dataFile = open('data.pkl', 'a') #encoding file, use pickle for file reading
                pickle.dump(standardizedRecord, dataFile)
                dataFile.close()
            except(EOFError, pickle.UnpicklingError):
                break
        print '---->Saved matrix to ./data.pkl'
        # for record in self.__middleMatrix:
        #     standardizedRecord = numpy.pad(record, (0, self.numberOfAttr - len(record)), 'constant')
        #     if(len(self.finalMatrix) is 0):
        #         self.finalMatrix = standardizedRecord
        #     else: 
        #         self.finalMatrix = numpy.vstack((self.finalMatrix, standardizedRecord))
        #---------------------------------------------------------------------------
        numpy.savetxt('./target.txt', self.target, fmt = '%s')
        print '---->Saved target to ./target.txt'
        attrListFile = open('attr.pkl', 'w')
        pickle.dump(self.listOfAttr, attrListFile)
        attrListFile.close()
        print '---->Saved attr to ./attr.pkl'

    def readFromFile(self, fileName):
        self.data = numpy.genfromtxt(fname = fileName, delimiter = ' ', dtype = (str,str))
    def appendTarget(self, label):
        self.target = numpy.append(self.target, label)
    # def numpyListOfAttr(self):
    #     # dictKeys = self.
    #     # return numpy.fromiter(self.listOfAttr.iterkeys() , dtype = 'S128')
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
# lst1 = loopNgram('PVCKPLLREEVEFQVGLNRYLVGSQLPCEPEPDVAVLTSM')
# lst2 = loopNgram('ACKPLLREEVVFQVGLNQYLVGSQLPCEPEPDVAVLTSML')
# glbObj.saveToFile()
# print glbObj.finalMatrix
glbObj.readFromFile('./data/unlabled_40_8k.txt')
print 'Total: ' + str(len (glbObj.data))
print '---------------------------'
it = numpy.nditer(glbObj.data, flags = ['external_loop'], order = 'C')
print it

# print glbObj.data
for index in range(0, len(glbObj.data)):
    # print glbObj.data[index]
    print '-Current tuple index: ' + str(index)
    loopNgram(glbObj.data[index])

# print glbObj.target
glbObj.saveToFile()
print glbObj.numberOfAttr
# print glbObj.numpyListOfAttr()


# print glbObj.listOfAttr