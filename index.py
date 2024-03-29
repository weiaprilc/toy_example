#!/bin/env python
from collections import deque
import os, glob, os.path
import sys
import re
from operator import itemgetter

if len(sys.argv) != 3:
  print >> sys.stderr, 'usage: python index.py data_dir output_dir' 
  os._exit(-1)

def mylistdir(directory):
    """A specialized version of os.listdir() that ignores files that
    start with a leading period."""
    filelist = os.listdir(directory)
    return [x for x in filelist
            if not (x.startswith('.'))]

total_file_count = 0
root = sys.argv[1]
out_dir = sys.argv[2]
if not os.path.exists(out_dir):
  os.makedirs(out_dir)

# this is the actual posting lists dictionary
# word id -> {position_in_file, doc freq}
posting_dict = {}
# this is a dict holding document name -> doc_id
doc_id_dict = {}
# this is a dict holding word -> word_id
word_dict = {}
# this is a queue holding block names, later used for merging blocks
block_q = deque([])

# function to count number of files in collection
def count_file():
  global total_file_count
  total_file_count += 1
  # print >> sys.stderr, 'you must provide implementation'

# function for printing a line in a postings list to a given file
def print_posting(posting_dict_file, word_id, posts):
  # a useful function is f.tell(), which gives you the offset from beginning of file
  # you may also want to consider storing the file position and doc frequence in posting_dict in this call
  freq = len(posts)
  offset = file.tell()
  print >> sys.stderr, offset
  posting_line = str(word_id) + ":" + ",".join(str(id) for id in posts)+'\n'
  posting_dict[word_id] = [offset,freq]
  posting_dict_file.write(posting_line)
  
# function for merging two lines of postings list to create a new line of merged results
def merge_posting (line1, line2):
  # don't forget to return the resulting line at the end
  print >> sys.stderr, 'you must provide implementation'
  return None

doc_id = -1
word_id = 0

for dir in sorted(mylistdir(root)):
  print >> sys.stderr, 'processing dir: ' + dir
  dir_name = os.path.join(root, dir)
  block_pl_name = out_dir+'/'+dir 
  # append block names to a queue, later used in merging
  block_q.append(dir)
  block_pl = open(block_pl_name, 'w')
  term_doc_list = []
  for f in sorted(os.listdir(dir_name)):
    count_file()
    file_id = os.path.join(dir, f)
    doc_id += 1
    doc_id_dict[file_id] = doc_id
    fullpath = os.path.join(dir_name, f)
    file = open(fullpath, 'r')
    for line in file.readlines():
      tokens = line.strip().split()
      for token in tokens:
        if token not in word_dict:
          word_dict[token] = word_id
          word_id += 1
        term_doc_list.append( (word_dict[token], doc_id) )
  print >> sys.stderr, 'sorting term doc list for dir:' + dir
  # sort term doc list
  # (you need to provide implementation)
  sorted_term_doc_list = sorted(set(term_doc_list), key=itemgetter(0,1))
  print >> sys.stderr, 'print posting list to disc for dir:' + dir
  # write the posting lists to block_pl for this current block 
  # (you need to provide implementation)

  #block_pd_name = out_dir+'/'+dir+'_posting_dict'
  #block_pd = open(block_pd_name, 'w')


  current_word_id = None
  current_posts = []
  for rec in sorted_term_doc_list:
    if current_word_id != rec[0]:
      
      if current_word_id is not None:
        posting_line = str(current_word_id) + ":" + ",".join(str(id) for id in current_posts)+'\n'
        block_pl.write(posting_line)
        current_posts = []
      
      current_word_id = rec[0]
      current_posts = []
      current_posts.append(rec[1]) #come back to this
    else:
      current_posts.append(rec[1])
  if current_posts:
    posting_line = str(current_word_id) + ":" + ",".join(str(id) for id in current_posts)+'\n'
    block_pl.write(posting_line)

  block_pl.close()

print >> sys.stderr, '######\nposting list construction finished!\n##########'

print >> sys.stderr, '\nMerging postings...'

def popLeftOrNone(p):
 if len(p) > 0:
   posting = p.popleft()
 else:
   posting = None
 return posting

def loadPostingsList(line):
  ls = deque([])

while True:
  if len(block_q) <= 1:
    break
  b1 = block_q.popleft()
  b2 = block_q.popleft()
  print >> sys.stderr, 'merging %s and %s' % (b1, b2)
  b1_f = open(out_dir+'/'+b1, 'r')
  b2_f = open(out_dir+'/'+b2, 'r')
  comb = b1+'+'+b2
  comb_f = open(out_dir + '/'+comb, 'w')
  # (provide implementation merging the two blocks of posting lists)
  # write the new merged posting lists block to file 'comb_f'

  list1 = []
  list2 = []
  for line in b1_f:
    list1.append([int(id.strip()) for id in line.strip().replace(':',',').split(',')])
  for line in b2_f:
    list2.append([int(id.strip()) for id in line.strip().replace(':',',').split(',')])

  deque1 = deque(list1)
  deque2 = deque(list2)

  rec1 = popLeftOrNone(deque1)
  rec2 = popLeftOrNone(deque2)

  while rec1 is not None and rec2 is not None:
    if rec1[0] == rec2[0]:
      posts1 = [id for id in rec1[1:]]
      posts2 = [id for id in rec2[1:]]
      comb_f.write(str(rec1[0]) + ":" + ",".join(str(id) for id in sorted(set(posts1 + posts2)))+'\n')

      rec1 = popLeftOrNone(deque1)
      rec2 = popLeftOrNone(deque2)
    elif rec1[0] < rec2[0]:
      posts1 = [id for id in rec1[1:]]
      comb_f.write(str(rec1[0]) + ":" + ",".join(str(id) for id in posts1)+'\n')
      rec1 = popLeftOrNone(deque1)
    else:
      posts2 = [id for id in rec2[1:]]
      comb_f.write(str(rec2[0]) + ":" + ",".join(str(id) for id in posts2)+'\n')
      rec2 = popLeftOrNone(deque2)

  while rec1 is not None:
    posts1 = [id for id in rec1[1:]]
    comb_f.write(str(rec1[0]) + ":" + ",".join(str(id) for id in posts1)+'\n')
    rec1 = popLeftOrNone(deque1)

  while rec2 is not None:
    posts2 = [id for id in rec2[1:]]
    comb_f.write(str(rec2[0]) + ":" + ",".join(str(id) for id in posts2)+'\n')
    rec2 = popLeftOrNone(deque2)
    


  b1_f.close()
  b2_f.close()

  comb_f.close()
  #os.remove(out_dir+'/'+b1)
  #os.remove(out_dir+'/'+b2)
  block_q.append(comb)

    
print >> sys.stderr, '\nPosting Lists Merging DONE!'

# rename the final merged block to corpus.index
final_name = block_q.popleft()
os.rename(out_dir+'/'+final_name, out_dir+'/corpus.index')



corpus_file = open(out_dir+'/corpus.index', 'r')

offset = corpus_file.tell()
for line in iter(corpus_file.readline, ''):
  temp = line.strip().replace(':',',').split(',')
  freq = len(temp) - 1
  posting_dict[str(temp[0])] = (offset, freq)
  offset = corpus_file.tell()


# print all the dictionary files
doc_dict_f = open(out_dir + '/doc.dict', 'w')
word_dict_f = open(out_dir + '/word.dict', 'w')
posting_dict_f = open(out_dir + '/posting.dict', 'w')
print >> doc_dict_f, '\n'.join( ['%s\t%d' % (k,v) for (k,v) in sorted(doc_id_dict.iteritems(), key=lambda(k,v):v)])
print >> word_dict_f, '\n'.join( ['%s\t%d' % (k,v) for (k,v) in sorted(word_dict.iteritems(), key=lambda(k,v):v)])
print >> posting_dict_f, '\n'.join(['%s\t%s' % (k,'\t'.join([str(elm) for elm in v])) for (k,v) in sorted(posting_dict.iteritems(), key=lambda(k,v):v)])
doc_dict_f.close()
word_dict_f.close()
posting_dict_f.close()

print total_file_count