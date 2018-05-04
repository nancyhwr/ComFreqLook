import csv
from collections import Counter
from collections import defaultdict
from collections import OrderedDict
from nltk.util import ngrams 
from nltk import FreqDist 
from operator import itemgetter    
import  time, datetime
from itertools import islice



# 18-05-02 Haoran
#input: csv file with sequence records
#output the most common top n frequency with lenghth k


# find the c most common subsequences with lenghth n from a given token list
# n:n-grams; c:top c subsequencies; 
def count_seq(tokens, n, c):
	k_gramfdist = FreqDist()
	k_grams = ngrams(tokens, n)
	k_gramfdist.update(k_grams)
	return k_gramfdist.most_common(c)


# add each subsequnce into a dictionary (common_dict) with cummulated frequency
# common_list: a list of tuple (subsequence, frequency)
def make_dict(common_list, common_dict):

	for el in common_list:
		if el[0] not in common_dict.keys():
			common_dict[el[0]] = el[1]
		else:
			common_dict[el[0]] = common_dict[el[0]]+el[1]
	

# from a csv to find all subsequences and the frequencies and add it to a dictionary
# addr: file address; n: n-gram; c:top c
# pos_dict: label = 1; neg_dict: label = 0
def build_subseq(addr, n, c):

	count = 0
	with open(addr) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			sorted_row = list(OrderedDict(sorted(row.items(), key=lambda item: reader.fieldnames.index(item[0]))).values())
			if count <=1:
				print(count)
				label = sorted_row[0]
				tokens = sorted_row[1:]
				print('tokens=',tokens)
				common_seq = count_seq(tokens, n, c)
				count = count +1
				if label == 1:
					make_dict(common_seq, pos_dict)
				else:
					make_dict(common_seq, neg_dict)
			else:
				return


# common_dict: the dictionary including all subsequnce; top_c: integer, the most common subsequence
def top_subseq(common_dict, top_c):
	return list(islice(common_dict, top_c))

########################################################
## #same as the one above just without "count" loop ####
######################################################## 
# def build_subseq(addr, n, c):
# 	with open(addr) as csvfile:
# 		reader = csv.DictReader(csvfile)
# 		for row in reader:
# 			sorted_row = list(OrderedDict(sorted(row.items(), key=lambda item: reader.fieldnames.index(item[0]))).values())
			
# 			label = sorted_row[0]
# 			tokens = sorted_row[1:]
# 			common_seq = count_seq(tokens, n, c)
# 			count = count +1
# 			if label == 1:
# 				make_dict(common_seq, pos_dict)
# 			else:
# 				make_dict(common_seq, neg_dict)
			

pos_dict = {} # label=1
neg_dict = {} # label=0
address = '/Users/nancy/Documents/IQVIA/data1.csv'
n = 5 # subsequnce length
len_row = 76 # length of a row
c = len_row - n + 1 # number of subsequences with length=5 in each row
top_c = 10 # top 10 most common

build_subseq(address, n, c)
pos_dict = sorted(pos_dict.items(), key = itemgetter(1), reverse = True)
neg_dict = sorted(neg_dict.items(), key = itemgetter(1), reverse = True)
top_neg_dict = top_subseq(neg_dict, top_c)
top_pos_dict = top_subseq(pos_dict, top_c)


print()





