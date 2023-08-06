########################################################################################################
# PoC for The Collatz Regular Language
#
# J. Hernandez 2023
########################################################################################################
# This script implements a Proof of Concept from the homonime article. It does not meant to be optimal
# since it tries to be as explicit and trustworthy with that paper as possible.  Please, feel free to 
# refactor it or implement differently.
########################################################################################################
# Execution examples (it always returns Collatz word for n; all the arguments can be combined):
#
# python3 theCollatzRegularLanguage_mod9.py -n 19 -c
# It returns Collatz sequence using n
# [*] Collatz Sequence
# 19, 58, 29, 88, 44, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1
#
# python3 theCollatzRegularLanguage_mod9.py -n 19 -c -r 3
# It returns Collatz sequence using n  while looping r times. r parameter is considered for any other
# argument
# [*] Collatz Sequence
# 19, 58, 29, 88, 44, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1, 4, 2, 1, 4, 2, 1
#
# python3 theCollatzRegularLanguage_mod9.py -n 19 -s1
# It returns stage one using n
# [*] Collatz Word Stage One: group in pairs
# [19, 58], [58, 29], [29, 88], [88, 44], [44, 22], [22, 11], [11, 34], [34, 17], [17, 52], [52, 26], 
# [26, 13], [13, 40], [40, 20], [20, 10], [10, 5], [5, 16], [16, 8], [8, 4], [4, 2], [2, 1]
#
# python3 theCollatzRegularLanguage_mod9.py -n 19 -s2
# It returns stage two using n
# [*] Collatz Word Stage Two: rework pairs
# [1, 4]^1, [4, 2]^3, [11, 34]^1, [16, 8]^4, [8, 4]^2, [4, 2]^1, [11, 34]^0, [16, 8]^1, [17, 52]^0, [16, 8]^2,
# [8, 4]^1, [13, 40]^0, [4, 2]^2, [2, 1]^1, [10, 5]^0, [5, 16]^0, [16, 8]^0, [8, 4]^0, [4, 2]^0, [2, 1]^0, [1, 4]
#
# python3 theCollatzRegularLanguage_mod9.py -n 19 -m
# It returns multiplicities from stage two using n
# [*] Multiplicities for n = 19
# 1, 3, 1, 4, 2, 1, 0, 1, 0, 2, 1, 0, 2, 1, 0, 0, 0, 0, 0, 0

# python3 theCollatzRegularLanguage_mod9.py -n 19 -s3
# It returns stage three using n
# [*] Collatz Word Stage Three: rework multiplicities
# [1, 4]^1, [4, 2]^1, [11, 34]^1, [16, 8]^0, [8, 4]^0, [4, 2]^1, [11, 34]^0, [16, 8]^1, [17, 52]^0, [16, 8]^0, 
# [8, 4]^1, [13, 40]^0, [4, 2]^0, [2, 1]^1, [10, 5]^0, [5, 16]^0, [16, 8]^0, [8, 4]^0, [4, 2]^0, [2, 1]^0, [1, 4]
#
# python3 theCollatzRegularLanguage_mod9.py -n 19 -dfa
# It returns the path on the DFA M for the word from Collatz sequence using n
# [*] Digesting Collatz Word using DFA M
#	 [+] From [s] to [1, 4] using transition .......... 1
#	 [+] From [1, 4] to [4, 2] using transition ....... 1
#	 [+] From [4, 2] to [11, 34] using transition ..... 1
#	 [+] From [11, 34] to [16, 8] using transition .... 1
#	 [+] From [16, 8] to [8, 4] using transition ...... 0
#	 [+] From [8, 4] to [4, 2] using transition ....... 0
#	 [+] From [4, 2] to [11, 34] using transition ..... 1
#	 [+] From [11, 34] to [16, 8] using transition .... 0
#	 [+] From [16, 8] to [17, 52] using transition .... 1
#	 [+] From [17, 52] to [16, 8] using transition .... 0
#	 [+] From [16, 8] to [8, 4] using transition ...... 0
#	 [+] From [8, 4] to [13, 40] using transition ..... 1
#	 [+] From [13, 40] to [4, 2] using transition ..... 0
#	 [+] From [4, 2] to [2, 1] using transition ....... 0
#	 [+] From [2, 1] to [10, 5] using transition ...... 1
#	 [+] From [10, 5] to [5, 16] using transition ..... 0
#	 [+] From [5, 16] to [16, 8] using transition ..... 0
#	 [+] From [16, 8] to [8, 4] using transition ...... 0
#	 [+] From [8, 4] to [4, 2] using transition ....... 0
#	 [+] From [4, 2] to [2, 1] using transition ....... 0
#	 [+] From [2, 1] to [1, 4] using transition ....... 0
#
# [*] Collatz Word for n = 19 IS ACCEPTED BY THE DFA M
#
# [*] Collatz Word mod9 for n = 19
# 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0

from argparse import ArgumentParser
import sys
import os

# Returns Collatz value
def collatzValue(n):
    if n % 2 == 0:
        return int(n/2)
    else:
        return 3*n+1

# Returns n mod 2
def modTwo(n):
    return n % 2

# Returns n mod 9
def modNine(n):
    return n % 9

# Returns Collatz sequence using f(n) with numberOfRootLoops 4,2,1 loops
def buildCollatzSequence(n, numberOfRootLoops):
	rootCounter = 0
	collatzRootWasRepeated = False
	collatzSequence = []
	collatzSequence.append(n)
	while not collatzRootWasRepeated:
		n = collatzValue(n)
		collatzSequence.append(n)
		if n == 1:
			if rootCounter == numberOfRootLoops - 1:
				collatzRootWasRepeated = True
			rootCounter += 1
	return collatzSequence


# DFA with s+(2*9) states digesting Collatz words
# State s (initial state)
def state_s(transition):
	currentState = '[s]'
	print('[*] Digesting Collatz Word using DFA M')
	nextState={
		0:'[18, 9]',
		1:'[1, 4]',
		2:'[2, 1]',
		3:'[3, 10]',
		4:'[4, 2]',
		5:'[5, 16]',
		6:'[6, 3]',
		7:'[7, 22]',
		8:'[8, 4]',
		9:'[9, 28]',
		10:'[10, 5]',
		11:'[11, 34]',
		12:'[12, 6]',
		13:'[13, 40]',
		14:'[14, 7]',
		15:'[15, 46]',
		16:'[16, 8]',
		17:'[17, 52]',
	}
	if (nextState.get(transition) == None):
		print('\t [-] In state ' + currentState+ ' with unexpected transition ' + str(transition))
		return None
	print('\t [+] From ' + currentState + ' to ' + nextState.get(transition) + ' using transition ' + printFromTransitionTo(currentState, nextState.get(transition), transition))
	return nextState.get(transition)

# State [18,9]
def state_18_9(transition):
	currentState = '[18, 9]'
	nextState={
		0:'[18, 9]',
		1:'[9, 28]',
	}
	if (nextState.get(transition) == None):
		print('\t [-] In state ' + currentState+ ' with unexpected transition ' + str(transition))
		return None
	print('\t [+] From ' + currentState + ' to ' + nextState.get(transition) + ' using transition ' + printFromTransitionTo(currentState, nextState.get(transition), transition))
	return nextState.get(transition)

# State [1, 4]
def state_1_4(transition):
	currentState = '[1, 4]'
	nextState={
		0:'[4, 2]',
		1:'[4, 2]',
	}
	if (nextState.get(transition) == None):
		print('\t [-] In state ' + currentState+ ' with unexpected transition ' + str(transition))
		return None
	print('\t [+] From ' + currentState + ' to ' + nextState.get(transition) + ' using transition ' + printFromTransitionTo(currentState, nextState.get(transition), transition))
	return nextState.get(transition)

# State [2,1]
def state_2_1(transition):
	currentState = '[2, 1]'
	nextState={
		0:'[1, 4]',
		1:'[10, 5]',
	}
	if (nextState.get(transition) == None):
		print('\t [-] In state ' + currentState+ ' with unexpected transition ' + str(transition))
		return None
	print('\t [+] From ' + currentState + ' to ' + nextState.get(transition) + ' using transition ' + printFromTransitionTo(currentState, nextState.get(transition), transition))
	return nextState.get(transition)

# State [3,10]
def state_3_10(transition):
	currentState = '[3, 10]'
	nextState={
		0:'[10, 5]',
		1:'[10, 5]',
	}
	if (nextState.get(transition) == None):
		print('\t [-] In state ' + currentState+ ' with unexpected transition ' + str(transition))
		return None
	print('\t [+] From ' + currentState + ' to ' + nextState.get(transition) + ' using transition ' + printFromTransitionTo(currentState, nextState.get(transition), transition))
	return nextState.get(transition)

# State [4,2]
def state_4_2(transition):
	currentState = '[4, 2]'
	nextState={
		0:'[2, 1]',
		1:'[11, 34]',
	}
	if (nextState.get(transition) == None):
		print('\t [-] In state ' + currentState+ ' with unexpected transition ' + str(transition))
		return None
	print('\t [+] From ' + currentState + ' to ' + nextState.get(transition) + ' using transition ' + printFromTransitionTo(currentState, nextState.get(transition), transition))
	return nextState.get(transition)

# State [5, 16]
def state_5_16(transition):
	currentState = '[5, 16]'
	nextState={
		0:'[16, 8]',
		1:'[16, 8]',
	}
	if (nextState.get(transition) == None):
		print('\t [-] In state ' + currentState+ ' with unexpected transition ' + str(transition))
		return None
	print('\t [+] From ' + currentState + ' to ' + nextState.get(transition) + ' using transition ' + printFromTransitionTo(currentState, nextState.get(transition), transition))
	return nextState.get(transition)

# State [6,3]
def state_6_3(transition):
	currentState = '[6, 3]'
	nextState={
		0:'[3, 10]',
		1:'[12, 6]',
	}
	if (nextState.get(transition) == None):
		print('\t [-] In state ' + currentState+ ' with unexpected transition ' + str(transition))
		return None
	print('\t [+] From ' + currentState + ' to ' + nextState.get(transition) + ' using transition ' + printFromTransitionTo(currentState, nextState.get(transition), transition))
	return nextState.get(transition)

# State [7,22]
def state_7_22(transition):
	currentState = '[7, 22]'
	nextState={
		0:'[4, 2]',
		1:'[4, 2]',
	}
	if (nextState.get(transition) == None):
		print('\t [-] In state ' + currentState+ ' with unexpected transition ' + str(transition))
		return None
	print('\t [+] From ' + currentState + ' to ' + nextState.get(transition) + ' using transition ' + printFromTransitionTo(currentState, nextState.get(transition), transition))
	return nextState.get(transition)

# State [8,4]
def state_8_4(transition):
	currentState = '[8, 4]'
	nextState={
		0:'[4, 2]',
		1:'[13, 40]',
	}
	if (nextState.get(transition) == None):
		print('\t [-] In state ' + currentState+ ' with unexpected transition ' + str(transition))
		return None
	print('\t [+] From ' + currentState + ' to ' + nextState.get(transition) + ' using transition ' + printFromTransitionTo(currentState, nextState.get(transition), transition))
	return nextState.get(transition)

# State [9,28]
def state_9_28(transition):
	currentState = '[9, 28]'
	nextState={
		0:'[10, 5]',
		1:'[10, 5]',
	}
	if (nextState.get(transition) == None):
		print('\t [-] In state ' + currentState+ ' with unexpected transition ' + str(transition))
		return None
	print('\t [+] From ' + currentState + ' to ' + nextState.get(transition) + ' using transition ' + printFromTransitionTo(currentState, nextState.get(transition), transition))
	return nextState.get(transition)

# State [10,5]
def state_10_5(transition):
	currentState = '[10, 5]'
	nextState={
		0:'[5, 16]',
		1:'[14, 7]',
	}
	if (nextState.get(transition) == None):
		print('\t [-] In state ' + currentState+ ' with unexpected transition ' + str(transition))
		return None
	print('\t [+] From ' + currentState + ' to ' + nextState.get(transition) + ' using transition ' + printFromTransitionTo(currentState, nextState.get(transition), transition))
	return nextState.get(transition)

# State [11,34]
def state_11_34(transition):
	currentState = '[11, 34]'
	nextState={
		0:'[16, 8]',
		1:'[16, 8]',
	}
	if (nextState.get(transition) == None):
		print('\t [-] In state ' + currentState+ ' with unexpected transition ' + str(transition))
		return None
	print('\t [+] From ' + currentState + ' to ' + nextState.get(transition) + ' using transition ' + printFromTransitionTo(currentState, nextState.get(transition), transition))
	return nextState.get(transition)

# State [12,6]
def state_12_6(transition):
	currentState = '[12, 6]'
	nextState={
		0:'[6, 3]',
		1:'[15, 46]',
	}
	if (nextState.get(transition) == None):
		print('\t [-] In state ' + currentState+ ' with unexpected transition ' + str(transition))
		return None
	print('\t [+] From ' + currentState + ' to ' + nextState.get(transition) + ' using transition ' + printFromTransitionTo(currentState, nextState.get(transition), transition))
	return nextState.get(transition)

# State [13,40]
def state_13_40(transition):
	currentState = '[13, 40]'
	nextState={
		0:'[4, 2]',
		1:'[4, 2]',
	}
	if (nextState.get(transition) == None):
		print('\t [-] In state ' + currentState + ' with unexpected transition ' + str(transition))
		return None
	print('\t [+] From ' + currentState + ' to ' + nextState.get(transition) + ' using transition ' + printFromTransitionTo(currentState, nextState.get(transition), transition))
	return nextState.get(transition)

# State [14,7]
def state_14_7(transition):
	currentState = '[14, 7]'
	nextState={
		0:'[7, 22]',
		1:'[16, 8]',
	}
	if (nextState.get(transition) == None):
		print('\t [-] In state ' + currentState + ' with unexpected transition ' + str(transition))
		return None
	print('\t [+] From ' + currentState + ' to ' + nextState.get(transition) + ' using transition ' + printFromTransitionTo(currentState, nextState.get(transition), transition))
	return nextState.get(transition)

# State [15,46]
def state_15_46(transition):
	currentState = '[15, 46]'
	nextState={
		0:'[10, 5]',
		1:'[10, 5]',
	}
	if (nextState.get(transition) == None):
		print('\t [-] In state ' + currentState + ' with unexpected transition ' + str(transition))
		return None
	print('\t [+] From ' + currentState + ' to ' + nextState.get(transition) + ' using transition ' + printFromTransitionTo(currentState, nextState.get(transition), transition))
	return nextState.get(transition)

# State [16,8]
def state_16_8(transition):
	currentState = '[16, 8]'
	nextState={
		0:'[8, 4]',
		1:'[17, 52]',
	}
	if (nextState.get(transition) == None):
		print('\t [-] In state ' + currentState + ' with unexpected transition ' + str(transition))
		return None
	print('\t [+] From ' + currentState + ' to ' + nextState.get(transition) + ' using transition ' + printFromTransitionTo(currentState, nextState.get(transition), transition))
	return nextState.get(transition)

# State [17, 52]
def state_17_52(transition):
	currentState = '[17, 52]'
	nextState={
		0:'[16, 8]',
		1:'[16, 8]',
	}
	if (nextState.get(transition) == None):
		print('\t [-] In state ' + currentState + ' with unexpected transition ' + str(transition))
		return None
	print('\t [+] From ' + currentState + ' to ' + nextState.get(transition) + ' using transition ' + printFromTransitionTo(currentState, nextState.get(transition), transition))
	return nextState.get(transition)

# Returns boolean based on DFA acceptance
def isCollatzWordAcceptedByDfa(collatzWord): 
	n = len(collatzWord)
	i = 0
	fsmCurrentState = '[s]'
	while (i <= n-1):
		if fsmCurrentState == '[s]':
				fsmCurrentState = state_s(collatzWord[i])
		elif fsmCurrentState ==  '[18, 9]':
				fsmCurrentState = state_18_9(collatzWord[i])
		elif fsmCurrentState ==  '[1, 4]':
				fsmCurrentState = state_1_4(collatzWord[i])
		elif fsmCurrentState ==  '[2, 1]':
				fsmCurrentState = state_2_1(collatzWord[i])
		elif fsmCurrentState ==  '[3, 10]':
				fsmCurrentState = state_3_10(collatzWord[i]) 
		elif fsmCurrentState ==  '[4, 2]':
				fsmCurrentState = state_4_2(collatzWord[i]) 
		elif fsmCurrentState ==  '[5, 16]':
				fsmCurrentState = state_5_16(collatzWord[i]) 
		elif fsmCurrentState ==  '[6, 3]':
				fsmCurrentState = state_6_3(collatzWord[i]) 
		elif fsmCurrentState ==  '[7, 22]':
				fsmCurrentState = state_7_22(collatzWord[i]) 
		elif fsmCurrentState ==  '[8, 4]':
				fsmCurrentState = state_8_4(collatzWord[i]) 
		elif fsmCurrentState ==  '[9, 28]':
				fsmCurrentState = state_9_28(collatzWord[i])
		elif fsmCurrentState ==  '[10, 5]':
				fsmCurrentState = state_10_5(collatzWord[i])
		elif fsmCurrentState ==  '[11, 34]':
				fsmCurrentState = state_11_34(collatzWord[i])
		elif fsmCurrentState ==  '[12, 6]':
				fsmCurrentState = state_12_6(collatzWord[i])
		elif fsmCurrentState ==  '[13, 40]':
				fsmCurrentState = state_13_40(collatzWord[i])
		elif fsmCurrentState ==  '[14, 7]':
				fsmCurrentState = state_14_7(collatzWord[i])
		elif fsmCurrentState ==  '[15, 46]':
				fsmCurrentState = state_15_46(collatzWord[i])
		elif fsmCurrentState ==  '[16, 8]':
				fsmCurrentState = state_16_8(collatzWord[i])
		elif fsmCurrentState ==  '[17, 52]':
				fsmCurrentState = state_17_52(collatzWord[i])
		else:
			return False
		i = i + 1
	return True

# Prints sequence values
def printSequence(banner, sequence):
	print(banner + '\n', end='')
	for i in range(len(sequence)-1):
		print(sequence[i], end =', ')
	print(sequence[len(sequence)-1])

# Prints sequence length
def printSequenceLength(sequence):
	print('[*] Collatz Sequence Length\n'+ str(len(sequence)))

# Prints from->transition->to tabulated
def printFromTransitionTo(nodeA, nodeB, transition):
	aligned = ''
	bold = '\033[1m'
	normal = '\033[0m'
	transition = str(transition)
	if(len(nodeA) + len(nodeB) == 9):
		aligned = '.......... ' + bold + transition + normal
	if(len(nodeA) + len(nodeB) == 10):
		aligned = '......... ' + bold + transition + normal
	if(len(nodeA) + len(nodeB) == 11):
		aligned = '........ ' + bold + transition + normal
	if(len(nodeA) + len(nodeB) == 12):
		aligned = '....... ' + bold + transition + normal
	if(len(nodeA) + len(nodeB) == 13):
		aligned = '...... ' + bold + transition + normal
	if(len(nodeA) + len(nodeB) == 14):
		aligned = '..... ' + bold + transition + normal
	if(len(nodeA) + len(nodeB) == 15):
		aligned = '.... ' + bold + transition + normal
	return aligned

# Prints a blank line
def printNewLine():
	print('')

# Returns the base pair from a Collatz pair
def processCollatzBasePair(collatzPairElementOne, collatzPairElementTwo):
	if (modNine(collatzPairElementOne) == 0) and (modNine(collatzPairElementTwo) == 0) and (collatzPairElementOne / 18 == collatzPairElementTwo / 9):
		return [18,9]
	if (modNine(collatzPairElementOne) == 1) and (modNine(collatzPairElementTwo) == 4) and ((collatzPairElementOne - 1) / 18 == (collatzPairElementTwo - 4) / 54):
		return [1,4]
	if (modNine(collatzPairElementOne) == 2) and (modNine(collatzPairElementTwo) == 1) and ((collatzPairElementOne - 2) / 18 == (collatzPairElementTwo - 1 )/ 9):
		return [2,1]
	if (modNine(collatzPairElementOne) == 3) and (modNine(collatzPairElementTwo) == 1) and ((collatzPairElementOne - 3) / 18 == (collatzPairElementTwo - 10) / 54):
		return [3,10]
	if (modNine(collatzPairElementOne) == 4) and (modNine(collatzPairElementTwo) == 2) and ((collatzPairElementOne - 4) / 18 == (collatzPairElementTwo - 2) / 9):
		return [4,2]
	if (modNine(collatzPairElementOne) == 5) and (modNine(collatzPairElementTwo) == 7) and (modTwo(collatzPairElementOne) == 1) and ((collatzPairElementOne - 5) / 18 == (collatzPairElementTwo - 16) / 54):
		return [5,16]
	if (modNine(collatzPairElementOne) == 6) and (modNine(collatzPairElementTwo) == 3) and ((collatzPairElementOne - 6) / 18 == (collatzPairElementTwo - 3) / 9):
		return [6,3]
	if (modNine(collatzPairElementOne) == 7) and (modNine(collatzPairElementTwo) == 4) and ((collatzPairElementOne - 7) / 18 == (collatzPairElementTwo - 22) / 54):
		return [7,22]
	if (modNine(collatzPairElementOne) == 8) and (modNine(collatzPairElementTwo) == 4) and ((collatzPairElementOne - 8) / 18 == (collatzPairElementTwo - 4) / 9):
		return [8,4]
	if (modNine(collatzPairElementOne) == 0) and (modNine(collatzPairElementTwo) == 1) and ((collatzPairElementOne - 9) / 18 == (collatzPairElementTwo - 28) / 54):
		return [9,28]
	if (modNine(collatzPairElementOne) == 1) and (modNine(collatzPairElementTwo) == 5) and ((collatzPairElementOne - 10) / 18 == (collatzPairElementTwo - 5) / 9):
		return [10,5]
	if (modNine(collatzPairElementOne) == 2) and (modNine(collatzPairElementTwo) == 7) and ((collatzPairElementOne - 11) / 18 == (collatzPairElementTwo - 34) / 54):
		return [11,34]
	if (modNine(collatzPairElementOne) == 3) and (modNine(collatzPairElementTwo) == 6) and ((collatzPairElementOne - 12) / 18 == (collatzPairElementTwo - 6) / 9):
		return [12,6]
	if (modNine(collatzPairElementOne) == 4) and (modNine(collatzPairElementTwo) == 4) and ((collatzPairElementOne - 13) / 18 == (collatzPairElementTwo - 40) / 54):
		return [13,40]
	if (modNine(collatzPairElementOne) == 5) and (modNine(collatzPairElementTwo) == 7) and (modTwo(collatzPairElementOne) == 0) and ((collatzPairElementOne - 14) / 18 == (collatzPairElementTwo - 7) / 9):
		return [14,7]
	if (modNine(collatzPairElementOne) == 6) and (modNine(collatzPairElementTwo) == 1) and ((collatzPairElementOne - 15) / 18 == (collatzPairElementTwo - 46) / 54):
		return [15,46]
	if (modNine(collatzPairElementOne) == 7) and (modNine(collatzPairElementTwo) == 8) and ((collatzPairElementOne - 16) / 18 == (collatzPairElementTwo - 8) / 9):
		return [16,8]
	if (modNine(collatzPairElementOne) == 8) and (modNine(collatzPairElementTwo) == 7) and ((collatzPairElementOne - 17) / 18 == (collatzPairElementTwo - 52) / 54):
		return [17,52]

# Returns the multiplicity for a Collatz pair; any equation from [c, c_k-1] can be used
def processCollatzMultiplicity(collatzPairElementOne, collatzPairElementTwo):
	if (modNine(collatzPairElementOne) == 0) and (modNine(collatzPairElementTwo) == 0) and (collatzPairElementOne / 18 == collatzPairElementTwo / 9):
		return int(collatzPairElementOne / 18)
	if (modNine(collatzPairElementOne) == 1) and (modNine(collatzPairElementTwo) == 4) and ((collatzPairElementOne - 1) / 18 == (collatzPairElementTwo - 4) / 54):
		return int((collatzPairElementOne - 1) / 18)
	if (modNine(collatzPairElementOne) == 2) and (modNine(collatzPairElementTwo) == 1) and ((collatzPairElementOne - 2) / 18 == (collatzPairElementTwo - 1 )/ 9):
		return int((collatzPairElementOne - 2) / 18)
	if (modNine(collatzPairElementOne) == 3) and (modNine(collatzPairElementTwo) == 1) and ((collatzPairElementOne - 3) / 18 == (collatzPairElementTwo - 10) / 54):
		return int((collatzPairElementOne - 3) / 18)
	if (modNine(collatzPairElementOne) == 4) and (modNine(collatzPairElementTwo) == 2) and ((collatzPairElementOne - 4) / 18 == (collatzPairElementTwo - 2) / 9):
		return int((collatzPairElementOne - 4) / 18)
	if (modNine(collatzPairElementOne) == 5) and (modNine(collatzPairElementTwo) == 7) and (modTwo(collatzPairElementOne) == 1) and ((collatzPairElementOne - 5) / 18 == (collatzPairElementTwo - 16) / 54):
		return int((collatzPairElementOne - 5) / 18)
	if (modNine(collatzPairElementOne) == 6) and (modNine(collatzPairElementTwo) == 3) and ((collatzPairElementOne - 6) / 18 == (collatzPairElementTwo - 3) / 9):
		return int((collatzPairElementOne - 6) / 18)
	if (modNine(collatzPairElementOne) == 7) and (modNine(collatzPairElementTwo) == 4) and ((collatzPairElementOne - 7) / 18 == (collatzPairElementTwo - 22) / 54):
		return int((collatzPairElementOne - 7) / 18)
	if (modNine(collatzPairElementOne) == 8) and (modNine(collatzPairElementTwo) == 4) and ((collatzPairElementOne - 8) / 18 == (collatzPairElementTwo - 4) / 9):
		return int((collatzPairElementOne - 8) / 18)
	if (modNine(collatzPairElementOne) == 0) and (modNine(collatzPairElementTwo) == 1) and ((collatzPairElementOne - 9) / 18 == (collatzPairElementTwo - 28) / 54):
		return int((collatzPairElementOne - 9) / 18)
	if (modNine(collatzPairElementOne) == 1) and (modNine(collatzPairElementTwo) == 5) and ((collatzPairElementOne - 10) / 18 == (collatzPairElementTwo - 5) / 9):
		return int((collatzPairElementOne - 10) / 18)
	if (modNine(collatzPairElementOne) == 2) and (modNine(collatzPairElementTwo) == 7) and ((collatzPairElementOne - 11) / 18 == (collatzPairElementTwo - 34) / 54):
		return int((collatzPairElementOne - 11) / 18)
	if (modNine(collatzPairElementOne) == 3) and (modNine(collatzPairElementTwo) == 6) and ((collatzPairElementOne - 12) / 18 == (collatzPairElementTwo - 6) / 9):
		return int((collatzPairElementOne - 12) / 18)
	if (modNine(collatzPairElementOne) == 4) and (modNine(collatzPairElementTwo) == 4) and ((collatzPairElementOne - 13) / 18 == (collatzPairElementTwo - 40) / 54):
		return int((collatzPairElementOne - 13) / 18)
	if (modNine(collatzPairElementOne) == 5) and (modNine(collatzPairElementTwo) == 7) and (modTwo(collatzPairElementOne) == 0) and ((collatzPairElementOne - 14) / 18 == (collatzPairElementTwo - 7) / 9):
		return int((collatzPairElementOne - 14) / 18)
	if (modNine(collatzPairElementOne) == 6) and (modNine(collatzPairElementTwo) == 1) and ((collatzPairElementOne - 15) / 18 == (collatzPairElementTwo - 46) / 54):
		return int((collatzPairElementOne - 15) / 18)
	if (modNine(collatzPairElementOne) == 7) and (modNine(collatzPairElementTwo) == 8) and ((collatzPairElementOne - 16) / 18 == (collatzPairElementTwo - 8) / 9):
		return int((collatzPairElementOne - 16) / 18 )
	if (modNine(collatzPairElementOne) == 8) and (modNine(collatzPairElementTwo) == 7) and ((collatzPairElementOne - 17) / 18 == (collatzPairElementTwo - 52) / 54):
		return int((collatzPairElementOne - 17) / 18)

def	printHeader():
	os.system('clear')
	print('###################################################################################################################')
	print('#                                                                                                                 #')
	print('#  PoC for The Collatz Regular Language                                                                           #')
	print('#                                                                                                                 #')
	print('#  Computes the Collatz word based on the parameter n and mod9 operation.                                         #')
	print('#  Some parameters can be specified to show intermediate steps and M acceptance.                                  #')
	print('#                                                                                                                 #')
	print('#                                                                                             J. Hernandez 2023   #')
	print('###################################################################################################################')

# Main 
if __name__ == '__main__' : 
	printHeader()
	parser = ArgumentParser()
	parser.add_argument('-n', type=int, default=1, help='Number to compute Collatz sequence; by default, n=1')
	parser.add_argument('-r', type=int, default=1,  help='Number or cycles to iterate; by default, r=1')
	parser.add_argument('-c', action='store_true', help='Show the Collatz sequence for n')
	parser.add_argument('-l', action='store_true', help='Show the lenght of the Collatz sequence')
	parser.add_argument('-s1', action='store_true', help='Show stage 1 for Collatz word representation')
	parser.add_argument('-s2', action='store_true', help='Show stage 2 for Collatz word representation')
	parser.add_argument('-s3', action='store_true', help='Show stage 3 for Collatz word representation')
	parser.add_argument('-m', action='store_true', help='Show raw multiplicities')
	parser.add_argument('-dfa', action='store_true', help='Test Collatz word using DFA M')

	args = parser.parse_args()

	n = args.n

	numberOfRootLoops = args.r

	printHeader()

	if n < 1:
		printNewLine()
		print('[!] Invalid value for Collatz function: n must be greater than 0')
		printNewLine()
		sys.exit()

	if numberOfRootLoops < 1:
		printNewLine()
		print('[!] Invalid value for loop repetitions: r must be greater than 0')
		printNewLine()
		sys.exit()

	collatzSequence = buildCollatzSequence(n, numberOfRootLoops)

	collatzSequenceRepresentationStageOneList = []
	basePairsList = []
	multiplicitiesList = []
	collatzWord = [int(n%18)]

	for i in range(len(collatzSequence) - 1):
		collatzSequenceRepresentationStageOneList.append([collatzSequence[i], collatzSequence[i+1]]) 
		basePairsList.append(processCollatzBasePair(collatzSequence[i], collatzSequence[i+1]))
		multiplicitiesList.append(processCollatzMultiplicity(collatzSequence[i], collatzSequence[i+1]))
		collatzWord.append(modTwo(multiplicitiesList[i]))

	if args.c:
		printNewLine()
		printSequence('[*] Collatz Sequence', collatzSequence)

	if args.l:
		printNewLine()
		printSequenceLength(collatzSequence)

	if args.s1:
		printNewLine()
		printSequence('[*] Collatz Word Stage One: group in pairs', collatzSequenceRepresentationStageOneList)

	if args.s2:
		printNewLine()
		collatzSequenceRepresentationStageTwo = []
		for i in range(len(basePairsList)):
			collatzSequenceRepresentationStageTwo.append('{}^{}'.format(basePairsList[i],multiplicitiesList[i]))
		collatzSequenceRepresentationStageTwo.append('[1, 4]')
		printSequence('[*] Collatz Word Stage Two: rework pairs', collatzSequenceRepresentationStageTwo)

	if args.s3:
		printNewLine()
		collatzSequenceRepresentationStageThree = []
		for i in range(len(basePairsList)):
			collatzSequenceRepresentationStageThree.append('{}^{}'.format(basePairsList[i],modTwo(multiplicitiesList[i])))
		collatzSequenceRepresentationStageThree.append('[1, 4]')
		printSequence('[*] Collatz Word Stage Three: rework multiplicities', collatzSequenceRepresentationStageThree)

	if args.m:
		printNewLine()
		printSequence('[*] Multiplicities for n = ' + str(n), multiplicitiesList)

	if args.dfa:
		printNewLine()
		if (isCollatzWordAcceptedByDfa(collatzWord)):
			printNewLine()
			print('[*] Collatz Word for n = ' + str(n) + ' IS ACCEPTED BY THE DFA M')
		else:
			printNewLine()
			print('[*] Collatz Word for n = ' + str(n) + ' IS NOT ACCEPTED BY THE DFA M')

	printNewLine()
	printSequence('[*] Collatz Word mod9 for n = ' + str(n), collatzWord)

	printNewLine()
