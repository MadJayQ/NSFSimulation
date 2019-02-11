# compare.py
# Author: Quentin Goss
# Last Modified: 9/20/18
#
# Compares two files and checks if they are different. Option to update
# FILE_A to FILE_B if the hashes are found to be different.
#
# Usage (debian):
#   To check if two files are different:
#
#      python3 compare.py --filea FILE_A --fileb FILE_B
#
#   To check and update file a to file b:
#
#      python3 compare.py --filea FILE_A --fileb FILE_B --update
#
#   Reverse order (check file b against file a):
#
#      python3 compare.py --filea FILE_A --fileb FILE_B --reverse

def main():
  options = get_options()
  
  if options.reverse:
    s_filea = options.fileb
    s_fileb = options.filea
  else: 
    s_filea = options.filea
    s_fileb = options.fileb
  
  if compare(s_filea,s_fileb):
    print('<%s> and <%s> are the SAME.' % (s_filea, s_fileb))
  else:
    print('<%s> and <%s> are DIFFERENT.' % (s_filea, s_fileb))
    if options.update:
      update(s_filea,s_fileb)
# end def main

# Compare the contents of file A to file B
#
# @param string s_file_a: Filepath to file A
# @param string s_file_b: Filepath to file B
# @param bool return: Are the files the same?
def compare(s_file_a, s_file_b):
  # We can tell if the files are differn't by using md5 hashes.
  s_md5a = md5(s_file_a)
  s_md5b = md5(s_file_b)
  
  print("md5 hashes\nfilea: %s\nfileb: %s" % (s_md5a,s_md5b))
  
  if s_md5a != s_md5b:
    return False
  else:
    return True
  
# def compare(s_file_a, s_file_b):

# Updates file a to become file b
#
# @param string s_file_a: Filepath to file A
# @param string s_file_b: Filepath to file B
def update(s_file_a, s_file_b):
  n = 0
  with open(s_file_b,'r') as file_b:
    with open(s_file_a,'w') as file_a:
      for s_line in file_b:
        n += 1
        print('Updating line [%d]...' % (n), end='\r')
        file_a.write(s_line)
  print()
# end def update(s_file_a, s_file_b):

def get_options():
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option('--filea', help='Path of the 1st file.', action='store', type='string', dest='filea', default='None')
  parser.add_option('--fileb', help='Path of the 2nd file.', action='store', type='string', dest='fileb', default='None')
  parser.add_option('-r','--reverse', help='Compare fileb to filea.', action='store_true', dest='reverse', default=False)
  parser.add_option('-u','--update', help='Update filea to fileb.', action='store_true', dest='update', default=False)
  
  (options, args) = parser.parse_args()
  
  if options.filea == 'None':
    raise Exception('File a is not declared. Please declare using --filea=FILE_A')
  elif options.fileb == 'None':
    raise Exception('File b is not declared. Please declare using --fileb=FILE_B')
    
  return options
# end def get_options()

# Function retrieve from Stack Overflow
# Date retrieved: 9/20/2018
# Answer by: quantumSoup on Aug 7' 2010 19:53
# Edited by: Christoff Roussey on Mar 1' 2016 14:07
# Link: https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
def md5(fname):
  import hashlib  
  hash_md5 = hashlib.md5()
  with open(fname, "rb") as f:
      for chunk in iter(lambda: f.read(4096), b""):
          hash_md5.update(chunk)
  return hash_md5.hexdigest()


main()
