import itertools
from operator import itemgetter
import os.path
import string
import sys

def map_reduce(inputList,mapper,reducer):
  """
  A mapreduce approach for scaling
  Method uses pre-split line (which hadoop / hdfs would split them)
  :param list:
  """    
  temp = []
  for (key,value) in inputList.items():
    temp.extend(mapper(key,value))
  groups = {}
  # iterate over the sorted temp list grouped by key 
  for key, group in itertools.groupby(sorted(temp), 
                                      lambda x: x[0]):
    groups[key] = list([y for x, y in group])

  # reducer to get final required output  
  return [reducer(temp_key,groups[temp_key])
          for temp_key in groups] 

# mapper function to split the words with space as delimited
def mapper(input_key,input_value):
  return [(word,1) for word in 
          (input_value.split())]

# reducer function to compute the sum of unique words  
def reducer(r_key,r_list):
  return (r_key,sum(r_list))

def main(filepath):
  basepath = os.path.dirname(__file__)
  tweets_output_path = os.path.abspath(os.path.join(basepath,"../",filepath[2])) 
  tweets_input_path = os.path.abspath(os.path.join(basepath,"../",filepath[1]))
  if not os.path.isfile(tweets_input_path):
      sys.exit("Input file not found") 
  tweets_output = open(tweets_output_path,'wb')
  tweets = {}
  count = 0 
  f = open(tweets_input_path, "r")
  for line in f:
      tweets[count] = line # use line number as key
      count += 1
  f.close()

  mr = sorted(map_reduce(tweets, mapper, reducer), key=itemgetter(0))

  # Format output and write to a file
  arr = [ x[0] for x in mr]
  maxlen = len(max(arr,key=len))+5
  for x in mr:
    tweets_output.write(x[0].ljust(maxlen)+str(x[1])+"\n")
  tweets_output.close()

if __name__ == '__main__':
  os.system('clear')
  if len(sys.argv) != 3:
    print('Require two arguments <fileinput> <fileoutput>')
    sys.exit()
  main(sys.argv)   
 
