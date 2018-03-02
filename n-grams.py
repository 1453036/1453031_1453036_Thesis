import numpy

#use numpy only
#data file with format, "sequence label"

class glbClass: #singleton class, contains global properties , just for encapsulation
    # Here will be the instance stored.
    __instance = None
    __middleMatrix = [] #temp array for standardize data (padding zeros) 

    data = numpy.array([]) #contain data read from file, type array of strings
    target = numpy.array([],  dtype = str) # array of labels
    numberOfAttr = 0
    listOfAttr = {} #type: dictionary ,template: {attrName1: index,attrName2: index + 1 , ...}, attribute collection from extracting whole dataset 
    finalMatrix = numpy.array([]) # final result (usable data)

    #private methods
    def __standardizeData(self):
        for record in self.__middleMatrix:
            standardizedRecord = numpy.pad(record, (0, self.numberOfAttr - len(record)), 'constant')
            if(len(self.finalMatrix) is 0):
                self.finalMatrix = standardizedRecord
            else: 
                self.finalMatrix = numpy.vstack((self.finalMatrix, standardizedRecord))

    #public methods
    def appendAttr(self, attrName):
        self.listOfAttr[attrName] = self.numberOfAttr
        self.numberOfAttr = self.numberOfAttr + 1
    def getAttrIndex(self, attrName):
        return self.listOfAttr[attrName]
    def appendRecord(self, record):
        self.__middleMatrix.append(record)
        return 1
    def saveToFile(self):
        self.__standardizeData()
        numpy.savetxt('./data.txt', self.finalMatrix.astype(int),fmt='%i')
        print 'Saved data to ./data.txt'
        numpy.savetxt('./target.txt', self.target, fmt = '%s')
        print 'Saved target to ./target.txt'
    def readFromFile(self, fileName):
        self.data = numpy.loadtxt(fileName, dtype = (str,str))
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

    print dataTuple
    sequence = dataTuple[0]
    label = dataTuple[1]

    glbObj = glbClass.getInstance()
    ngramInstance = numpy.zeros((glbObj.numberOfAttr), dtype=int) #init ngramInstance with already-created attributes
    for i in range(1,40):
        ngramInstance = ngram(ngramInstance, sequence, i) 

    glbObj.appendRecord(ngramInstance)
    glbObj.appendTarget(label)

glbObj = glbClass.getInstance()
# lst1 = loopNgram('PVCKPLLREEVEFQVGLNRYLVGSQLPCEPEPDVAVLTSM')
# lst2 = loopNgram('ACKPLLREEVVFQVGLNQYLVGSQLPCEPEPDVAVLTSML')
# glbObj.saveToFile()
# print glbObj.finalMatrix
glbObj.readFromFile('./input.txt')

for dataTuple in glbObj.data:
    loopNgram(dataTuple)

# print glbObj.target
glbObj.saveToFile()
# print glbObj.numpyListOfAttr()


print glbObj.listOfAttr