def slideWindow(sequence, window):
	extractSeq = sequence[window[0]:window[1]]
	window[0]+=1
	window[1]+=1
	return extractSeq

def ngram(sequence, n):
	window = [0, n]
	ngramList = {}
	while(window[0] <= len(sequence) - n):
		extractSeq = slideWindow(sequence, window)
		if(extractSeq not in ngramList):
			ngramList[extractSeq] = 1
		else:
			print 'Match'
			ngramList[extractSeq] += ngramList[extractSeq]
	return ngramList


lst = ngram('SGSWLRDVWDWICTVLTDFKTWLQSGLLPRLPGVPFFSCQ', 2)
print lst
