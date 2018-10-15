import argparse
import re 
import random as r

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False)
parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s 1.6', help="Show program's version number and exit.")
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                    help='** = required')
parser.add_argument(
    "-f", "--file", type=str,
    help='** this is the file you\'re targeting to get the lcNrD treatment',required=True)
parser.add_argument("-o", "--out", type=str,
    help='this is the file you want the lcNrD file to output as. Default = same name + _LcNrD')

# store true or false so we can just be like 'if args.lowercase:'
# so use true or false values instead of comparing strings
parser.add_argument('-l', "--lowercase", action='store_true',
    help='add -l to set lowercase to true')
parser.add_argument('-d', "--duplicates", action='store_true',
    help='add -d to remove duplicate elements')
parser.add_argument('-s', "--shuffle", action='store_true',
    help='add -s to shuffle your list')
parser.add_argument('-rf', "--replace_file", action='store_true',
    help='add -rf to replace the original file after lcnrd operation')
parser.add_argument('-bl', "--blank_lines", action='store_true',
    help='add -bl to remove all blank lines')
parser.add_argument('-cmi', "--character_min", type=int, default=0,
    help='limits the minimal amount of chacters required')
parser.add_argument('-cma', "--character_max", type=int,
    help='limits the maximum amount of chacters required')
parser.add_argument('-kr', "--keyword_removal", type=str,
    help='add a -kr to remove lines with the removal keyword, use *.txt or whatever to point to a list of kr')
parser.add_argument('-kk', "--keyword_keep", type=str,
    help='add a -kk to keep only the lines with the keep keyword, use *.txt or whatever to point to a list of kk')
parser.add_argument('-kdb', "--keyword_delete_before", type=str,
    help='add a -kdb to delete all text before the delete before keyword')
parser.add_argument('-kda', "--keyword_delete_after", type=str,
    help='add a -kda to delete all text after the delete after keyword')
parser.add_argument('-kae', "--keyword_add_end", type=str,
    help='add a -kae to add some text to the end of every line')
parser.add_argument('-dli', "--input_delimiter", type=str,
    help='add a -dli to change input delimiter')
parser.add_argument('-dlo', "--output_delimiter", type=str,
    help='add a -dlo to change input delimiter')
parser.add_argument('-nts',"--newline_to_space", action='store_true',
    help ='add -nts to change newline to space (option will be ignored if delimiter is \\n)')
args = parser.parse_args()
print('Grabbing file contents...')

# open the target file & grab its contents. Using `with` like this automatically
# closes the file for us when we leave the indentation.
with open(args.file, "r") as fp:
    text = fp.read()

# let's create an array of the lines
input_delimiter = "\n"
if args.input_delimiter:
    input_delimiter = args.input_input_delimiter
    if args.newline_to_space:
        text = text.replace('\n',' ')
lines = text.split(input_delimiter)

# Remove blank lines
if args.blank_lines:
    # >>> bool('')
    # False
    # >>> bool('literally anything')
    # True
    lines = filter(bool,lines)

# 
if args.keyword_delete_before != None:
    print('removing text before delete keyword...')
    # str.find gives start position of first occurrence of substring
    lines = (line[ line.find(args.keyword_delete_before) :] for line in lines)

# 
if args.keyword_delete_after != None:
    print('removing text after delete keyword...')
    # messy as heck
    lines = (line[: line.find(args.keyword_delete_after) + len(args.keyword_delete_after)] for line in lines) 

# Remove lines that are UNDER min character requirements
if args.character_min > 0:
    print('Removing lines under min character requirements...')
    # note filter objects are lazy; nothing is done on them until they are iterated through or converted into a list/tuple
    lines = filter(lambda line: len(line) > args.character_min,lines)    

# Remove lines that are OVER max character requirements
if args.character_max != None:
    print('Removing lines over max character requirements...')
    lines = filter(lambda line: len(line) < args.character_max,lines)

# this checks if there is a removal keyword & performs this operation if so
if args.keyword_removal != None:
    print('removing lines with removal keyword...')

    # 
    if ("*." in args.keyword_removal):
        print("file used!")
        print('Reading filter keywords...')

        # open the keyword keep file & save a reference to its contents
        with open(args.keyword_removal.replace('*',''), "r") as fp:
            # constant time lookup
            filt = set(fp.read().split('\n'))

        print('filter keywords from file...')
        # constant time lookup for each word in string means o(number of words) + .split() time
        lines = filter(lambda line: not any(word in filt for word in line.split()),lines)
    else:

        lines = filter(lambda line: not any(args.keyword == word for word in line.split()),lines)
        print("keyword used!")

# this checks if there is a removal keyword & performs this operation if so
    print('removing lines without keep keyword...')
if args.keyword_keep != None:

    print('removing lines with removal keyword...')

    # 
    if ("*." in args.keyword_removal):
        print("file used!")
        print('Reading filter keywords...')

        # open the keyword keep file & save a reference to its contents
        with open(args.keyword_removal.replace('*',''), "r") as fp:
            filt = set(fp.read().split('\n'))

        print('filter keywords from file...')
        lines = filter(lambda line: any(word in filt for word in line.split()),lines)
    else:

        lines = filter(lambda line: any(args.keyword == word for word in line.split()),lines)
        print("keyword used!")

# convert to lowercase while we have the initial string. so only one function
# call and no loops needed.
if args.lowercase:
    print('lowercasing contents...')
    lines = (x.lower() for x in lines)

# remove duplicates by making the list a `set` which automatically makes
# everything unique. Again no loops, just 1 function call.
if args.duplicates:
    print('removing duplicates...')
    # note: simply using set does not guarantee that the lines will retain their original ordering 
    # >>> test = set(['aaa','bbb','ccc'])
    # >>> test
    # {'bbb', 'ccc', 'aaa'}
    used = set()
    prev_lines = lines
    lines = []
    for line in lines:
        if not line in used:
            used.add(line)
            lines.append(line)

# 
if args.keyword_add_end != None:
    print('adding keyword to end...')
    lines = (line+args.keyword_add_end for line in lines)

lines = list(lines)
# set the name of the new converted file
if not args.out:
    if args.replace_file:
        print('replacing orginal file...')
        args.out = args.file
    else:
    # ok this is a little bit obscure but its reverse splitting an string into
    # a list once so 'dir/file.txt' -> ['dir/file', 'txt']. then the '*' before
    # it when passed to format tells format to read the list as mulptiple args.
        args.out = "{}_lcNrD.{}".format(*args.file.rsplit(".", 1))

# shuffle the list of content if -s is added
if args.shuffle:
    print('shuffling content...')
    r.shuffle(lines)

# save the converted file
with open(args.out, "w") as fp:
    # strings are immutable in python so every time you add two strings together
    # its creating a brand new one. This gets quickly gets slow with lots of text
    # so we wanna do this as little as possible. Using join on the list means
    # we just make all the string concatenation opertations in one go.
    output_delimiter = "\n"
    if args.output_delimiter:
        output_delimiter = args.output_delimiter
    fp.write(output_delimiter.join(lines))

print('...& DONE!')

# <&=--- CPYTHON MASTER RACE ---=&>