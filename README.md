Insight Data Engineering - Coding Challenge
===========================================================

## Overview :
The Python code demonstrates a simple tool that could help analyze the community of Twitter users.  
Implemented features in the code samples include 

###1. Computing the total number of times each word has been tweeted (words_tweeted.py)

Example:

For the below three tweets (coming one after the other)

- is #bigdata finally the answer to end poverty? @lavanyarathnam http://ow.ly/o8gt3  #analytics  
- interview: xia wang, astrazeneca on #bigdata and the promise of effective healthcare #kdn http://ow.ly/ot2uj  
- big data is not just for big business. on how #bigdata is being deployed for small businesses: http://bddy.me/1bzukb3  @cxotodayalerts #smb  

The first feature would produce the following total count for each word:

	#analytics  				1
	#bigdata 					3
	#kdn 						1
	#smb 						1
	@cxotodayalerts 			1
	@lavanyarathnam 			1
	and 						1
	answer  					1
	astrazeneca 				1
	being 						1
	big 						2
	business. 					1 
	businesses: 				1
	data 						1
	deployed 					1
	effective 					1
	end 						1
	finally 					1
	for 						2
	healthcare 					1
	how 						1
	http://bddy.me/1bzukb3  	1
	http://ow.ly/o8gt3 	 		1
	http://ow.ly/ot2uj  		1
	interview: 					1
	is  						3
	just 						1
	not 						1
	of 							1
	on 							2
	poverty? 					1
	promise 					1
	small 						1
	the  						2
	to  						1
	wang,						1
	xia 						1



###2. Calculate the median of "unique" words per tweet & update the median as tweets come in (median_unique.py)

Example:

The number of unique words in each tweet from above is 11, 14 & 17 => set of unique words per tweet
is {11} {11, 14}  {11, 14, 17} after first, second and third tweet respectively  

The output is
```
11 
12.5 
14 
```

### Key assumptions about the input 

- The tweets are fed as an input file ->  tweets.txt. 

- The file only contains lowercase letters, numbers, and ASCII characters (e.g. common punctuation and characters like '@', and '#').  

- A word is defined as anything separated by whitespace.

- Each newline is a new tweet


### Files included and submission structure
------------------------------------------

	├── README.md  
	├── run.sh  
	├── src  
	│   ├── median_unique.py  
	│   └── words_tweeted.py  
	├── tweet_input  
	│   └── tweets.txt  
	└── tweet_output  
	    ├── ft1.txt  
	    └── ft2.txt  

## Prerequisites :

- The code is built using `Python version 3.4.3 `

### Libraries used
```
itertools  
itemgetter   
bisect  
```
## Execution :

To run the python code from the parent directory, use the following command

```
$ ./run.sh 
```

## Details about Implementation :

####words_tweeted.py - Compute the total number of times each word has been tweeted

- The program makes one pass over the data, reading each line

- For each line parsed, `tweets{}` list is passed as input list to the map-reduce function 
```
	-map_reduce(inputList,mapper,reducer); 
```
where tweets(line_number) is key, tweets(line) is value 

- the `mapper(input_key,input_value)` function is invoked with tweet line number as key, along with contents of 
  the tweet string.

- The function splits the string into words (delimiter as space) 

- For each occurrence of a word it returns a temporary key and value (word,1)
  
   E.g. line 1 returns 
  [('is', 1), ('#bigdata', 1), ('finally', 1), ('the', 1), ('answer', 1), 
   ('to', 1), ('end', 1), ('poverty?', 1), ('@lavanyarathnam', 1), ('http://ow.ly/o8gt3',1) ('#analytics', 1)]

- for every mapper returned value, the temp list is sorted by key `(x[0])` using the `itertools`

- the `reducer(r_key,r_list)` function is applied to each temp array which returns the sum of the temp values 
  for the temp key

- the program outputs the results to text file `ft1.txt` in the directory `./tweet_output`

####median_unique.py - Calculate the median number of "unique" words per tweet & update the median as tweets come

- The program makes one pass over the data, reading each line

- For each line parsed, `tweets{} `list is passed as inputList to the map-reduce function 
```
map_reduce(inputList,mapper,reducer);  
```
where tweets(line_number) is key, tweets(line) is value
- the `mapper(input_value)` function is invoked with contents of the tweet string.

- The function splits the string into words (delimiter as space) and computes the number of unique word count in 
  each tweet/line

   E.g. line 1 returns [11]

- for every mapper returned value, insertion sort is performed using the `bisect.insort()` which inserts items into the temp list in sorted order. Insertion sort is used since it is much more efficient on large lists since sorting is done in place 

E.g.    after first line    temp -> [11]
        after second line   temp -> [11, 14]
        after third line    temp -> [11, 14, 17]

- the `reducer(temp_value_list)` function is applied to each inout array & returns the median of the sorted array 

The logic uses immediate insertion of every new "unique" word length computed at distributed mappers into a list, compute the new median, and write that value  into the file.

- the program outputs the results to text file `ft2.txt` in the directory `./tweet_output`


####run.sh

 the run script for running the word count and median of unique words 
 It runs with the input directory 'tweet_input' and output the files in the directory 'tweet_output'
```
python ./src/words_tweeted.py ./tweet_input/tweets.txt ./tweet_output/ft1.txt
python ./src/median_unique.py ./tweet_input/tweets.txt ./tweet_output/ft2.txt
```
## Additional Notes :

- This solution works on a single machine.

- Scalability is important and is taken into account as part of the solution by use of map reduce concepts

- for long lists, significant time and memory savings is achieved due to the use of insertion sort algorithm such as this. 

- Sliding window median computation can also be performed if accurate median values are not needed. 


## Time Profiling :

The code was tested against a big 8 MB input file and below are the timing observations.

```
$ time python ./src/words_tweeted.py ./tweet_input/input1.txt ./tweet_output/ft1.txt

real	0m4.497s
user	0m4.132s
sys		0m0.251s
 

$ time python ./src/median_unique.py ./tweet_input/input1.txt ./tweet_output/ft2.txt

real	0m4.190s
user	0m4.027s
sys		0m0.080s 
```
The meaning for the above output measurements are as below :

* real - refers to the actual elasped time
* user - refers to the amount of cpu time spent outside of kernel
* sys - refers to the amount of cpu time spent inside kernel specific functions

By these measures we get a sense of how much cpu cycles per program was used regardless of other programs running on the system by adding together the *sys* and *user*s times.