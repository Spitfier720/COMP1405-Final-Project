#Data processing for our search engine.

import crawler
import json
import math

#Get all direct links from a given URL.
def get_outgoing_links(URL):
    return crawler.jsonDict[URL]["links"] if URL in crawler.jsonDict else None

#Get all links that lead to the given URL.
def get_incoming_links(URL):
    validLinks = []

    for link in crawler.jsonDict:
        if(URL in set(crawler.jsonDict[link]["links"])):
            validLinks.append(link)
    
    return validLinks if validLinks else None

#Calculating the quality of a page through determining how likely it is to reach that page.
def get_page_rank(URL):
    return crawler.jsonDict[URL]["pageRank"] if URL in crawler.jsonDict else -1

#Calculate the inverse document frequency.
def get_idf(word):
    totalDocuments = 0
    wordAppears = 0

    for link in crawler.jsonDict:
        wordAppears = wordAppears + 1 if word in crawler.jsonDict[link]["wordCount"] else wordAppears
        totalDocuments += 1
    
    return math.log(totalDocuments / (1 + wordAppears), 2) if wordAppears else 0


#Calculate the term frequency.
def get_tf(URL, word):
    if(URL not in crawler.jsonDict or word not in crawler.jsonDict[URL]["wordCount"]):
        return 0

    return crawler.jsonDict[URL]["wordCount"][word] / crawler.jsonDict[URL]["totalWords"]

#Calculating the tf-idf.
def get_tf_idf(URL, word):
    return math.log(1 + get_tf(URL, word), 2) * get_idf(word)