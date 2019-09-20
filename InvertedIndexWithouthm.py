from html.parser import HTMLParser
from bs4 import BeautifulSoup
import re
import os
from nltk import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import mmap
import sys
import linecache


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
# put the tokenids in the file here
myres = set(myres)
my_list_of_terms = []


termfile = open("termids.txt","w",encoding="utf8",errors='ignore')
counter=1
for i, val in enumerate(myres):
    if(val.isalpha()== True):
        for f in files:
            with open(f,encoding="utf8",errors='ignore') as file:
                dataaa=file.read()
                if val in dataaa:
                    termfile.write(str(counter))
                    termfile.write("    ")
                    my_list_of_terms.append(val)
                    termfile.write(val)
                    termfile.write("\n")
                    counter=counter+1

termfile.close()


#########################################################################
###CREATE THE INVERTED INDEX################
# as 
##TERM ID done
## No of times term occured in corpus #                 SEARCH IN THE TERMIDS.TXT done
## no of doc in which term comes  #           done
##(document id in which term comes # position of term in that doc            dO THIS IN oNE GO

### EXTRACTING TERM IDS
################################################
my_list_of_term_id = []
with open("termids.txt", "r",encoding="utf8",errors='ignore') as f:
    lines = f.readlines()
    for line in lines:
        my_list_of_term_id.append(re.findall('\d+', line ))


# ################################################
# ####total no of documents in which the term appears
counter_for_files = 0
list_of_count = []
for term in my_list_of_terms:
    for f in files:
        with open(f,encoding="utf8",errors='ignore') as file:
            dataaa=file.read()
            if term in dataaa:
                counter_for_files = counter_for_files + 1
    list_of_count.append(counter_for_files)
    counter_for_files = 0
# # ########################################################
# # #total no of times a term appears in corpus
mycorpus_appearence=[]
mycorpus_appearence_counter=0
for term in my_list_of_terms:
    for f in files:
        with open(f,encoding="utf8",errors='ignore') as file:
            data3 = file.read()
            for m in re.finditer(term,data3):
                mycorpus_appearence_counter = mycorpus_appearence_counter + 1
    mycorpus_appearence.append(mycorpus_appearence_counter)
    mycorpus_appearence_counter=0
# ########################################################################
# #finds out the terms in docs and their positions as well
docdid=1
lennn=len(my_list_of_terms)
docids_plus_their_positions = []
final_dptp = []
a=0
for term in my_list_of_terms:
    docids_plus_their_positions = []
    for f in files:
        with open(f,encoding="utf8",errors='ignore') as file:
            data2 = file.read()
            if term in data2:
                docids_plus_their_positions.append(docdid)
                for m in re.finditer(term,data2): 
                    docids_plus_their_positions.append(m.start())
        docdid = docdid + 1
    #print(docids_plus_their_positions)
    final_dptp.append(docids_plus_their_positions)
    a=a+1
    docdid=1
 #finaldptp is what you neeed

################################################################


length =len(final_dptp)
# for x in range(length):
#     print(my_list_of_term_id[x],mycorpus_appearence[x],list_of_count[x],final_dptp[x])
    
InvertedIndexfile = open("term_index.txt","w",encoding="utf8",errors='ignore')

# for x in range(length):
#     InvertedIndexfile.write(str(my_list_of_term_id[x]))
#     InvertedIndexfile.write(str(mycorpus_appearence[x]))
#     InvertedIndexfile(str(list_of_count[x]))
#     InvertedIndexfile(str(final_dptp[x]))

##### MAKE AN ARRAY TO APAPEND EVERYTHING TOGETHER

finalappend=[]
tempstorage=[]

for x in range(length):
    tempstorage=[]
    tempstorage.extend(my_list_of_term_id[x])
    tempstorage.append(mycorpus_appearence[x])
    tempstorage.append(list_of_count[x])
    tempstorage.extend(final_dptp[x])
    finalappend.append(tempstorage)


for i in finalappend:
    InvertedIndexfile.write("%s\n" % i)


####################################################################
#  NOW WE TAKE THE INPUT ARGUMENT AND SEARCH WHERE WE GOT THE TERM


my_term_to_find = sys.argv[1]

my_term_to_find_id=[]
mydevilcount=1
with open("termids.txt", "r",encoding="utf8",errors='ignore') as f:
    lines = f.readlines()
    for line in lines:
        if(my_term_to_find in line):
            my_term_to_find_id.append(re.findall('\d+', line ))
            break
        mydevilcount=mydevilcount+1



## NOW WE HAVE ID WE NEED TO EXTRACT FROM THE term_index.txt
line = linecache.getline('term_index.txt',mydevilcount)

stru = line.split(",")

print("Listing for term: ",my_term_to_find )
print("Term ID : ", my_term_to_find_id)
print("Term frequency in corpus : " , stru[1])
print("Number of documents containing term : ",stru[2])