from html.parser import HTMLParser
from bs4 import BeautifulSoup
import re
import os
from nltk import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))

def hasAlphanumero(inputString):
    flag= False
    for i in inputString:
        if i.isalnum():
            flag = True
            break
    return flag


# this is my function which is creating tokens using regex
def count_words(text):
    
    counts = dict() 
    lowerText = text.lower()
    split = re.split("[\s.,!?:;\"-]+",lowerText)
    split = [x for x in split if x != '']
    return split
########################################################################


# This is where you input the path for the directory from which the files will be extracted
path = input("Enter your path to the directory: ") 
print(path) 

########################################################################

# this is where all the text is collected from all the files
files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.txt' in file:
            files.append(os.path.join(r, file))
data=""
i=1
docfile = open("docids.txt", "w",encoding="utf8",errors='ignore') # This is the docids file for all the doc names and their ids
for f in files:
    with open(f,encoding="utf8",errors='ignore') as file:
     data1 = file.read()
     myfilename=os.path.basename(file.name)
     docfile.write(str(i))
     docfile.write("    ")
     docfile.write(myfilename)
     docfile.write("\n")
     i=i+1
     data=data+data1

docfile.close() 

########################################################################

# use the beautiful soup library to extract data or text from the html

soup = BeautifulSoup(data,'html.parser')

for script in soup(["script", "style"]):
    script.extract()

text = soup.get_text()
lines = (line.strip() for line in text.splitlines())
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
text = '\n'.join(chunk for chunk in chunks if chunk)

########################################################################

#tokenize all the words using the function defined above
myres = count_words(text)
########################################################################


########################################################################

# put the tokenids in the file here
termfile = open("termids.txt", "w",encoding="utf8",errors='ignore')
for i, val in enumerate(myres):
        termfile.write(str(i))
        termfile.write("    ")
        termfile.write(val)
        termfile.write("\n")

termfile.close()

########################################################################

# Delete all the stop words

stop_words = stopwords.words('stoplist.txt')
myres = [x for x in myres if not x in stop_words]

########################################################################


# Do the stemming Snowball

stemmer = SnowballStemmer('english')
stems=[]
for x in myres:
    x = stemmer.stem(x)
    if x != "":
        stems.append(x)

#print(stems)

########################################################################

###CREATE THE INVERTED INDEX################
# as 
##TERM ID ## No of times term occured in corpus ## no of doc in which term comes ##(document id in which term comes, position of term in that doc)

exp = re.compile(r'^[\+,\-]?[0-9]{1,3}$')

my_list = []
with open("termids.txt", "r",encoding="utf8",errors='ignore') as f:
    lines = f.readlines()
    print(lines)
    for line in lines:
        if re.match(exp, line.strip()):
            my_list.append(int(line.strip()))

InvertedIndexfile = open("term_index.txt","w",encoding="utf8",errors='ignore')

print(my_list)

