import numpy


class glbClass: #singleton class, contains global properties
    # Here will be the instance stored.
    __instance = None
    __middleMatrix = []


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
        numpy.savetxt('./output.txt', self.finalMatrix.astype(int),fmt='%i')
        print 'Saved to ./output.txt'


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
def loopNgram(sequence):
    glbObj = glbClass.getInstance()
    ngramInstance = numpy.zeros((glbObj.numberOfAttr), dtype=int)
    for i in range(1,40):
        ngramInstance = ngram(ngramInstance, sequence, i)
    return glbObj.appendRecord(ngramInstance)

glbObj = glbClass.getInstance()
lst1 = loopNgram('PVCKPLLREEVEFQVGLNRYLVGSQLPCEPEPDVAVLTSM')
lst2 = loopNgram('ACKPLLREEVVFQVGLNQYLVGSQLPCEPEPDVAVLTSML')

# print len(listOfAttr)
# print len(lst)
# print listOfAttr
# glbObj.saveToFile()
# print glbObj.
glbObj.saveToFile()
print glbObj.finalMatrix

# PVCKPLLREEVEFQVGLNRYLVGSQLPCEPEPDVAVLTSM

# ACKPLLREEVVFQVGLNQYLVGSQLPCEPEPDVAVLTSML

