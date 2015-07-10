import bisect
import itertools
import os.path
import string
import sys

#compute simple median
def median(lst):
    half = len(lst) // 2
    
    if not len(lst) % 2:
        return (lst[half - 1] + lst[half]) / 2.0
    return lst[half]

   
def map_reduce(inputList,mapper,reducer):
    """
    A mapreduce approach for scaling
    Method uses pre-split line (which hadoop / hdfs would split them)
    :param list:
    """
    temp = []
    median_lst = []

    for (key,value) in inputList.items():
        bisect.insort(temp, mapper(value)) #insertion sort
        median_lst.append(reducer(temp))   #append computed median to list

    return median_lst

# mapper function to compute unique words in every line
def mapper(input_value):
  return (len(set(input_value.split())))

# reducer function to compute the median of unique words 
def reducer(temp_value_list):
  return (median(temp_value_list))


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
  # read file line by line
  for line in f:
      tweets[count] = line #use line number as key
      count += 1
  f.close()

  # map_reduce method to compute frequency distribution of words in the file
  mr = map_reduce(tweets, mapper, reducer)
  
  tweets_output.write('\n'.join('%.1f' %x for x in mr))
  tweets_output.close()
  

if __name__ == '__main__':
  os.system('clear')
  if len(sys.argv) != 3:
    print('Require two arguments <fileinput> <fileoutput>')
    sys.exit()
  main(sys.argv) 


