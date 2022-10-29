#Creating a primitive search engine.

import crawler
import json
import math
import searchdata

#Return the top 10 pages given a query.
def search(phrase, boost):
    #In case the json file is empty.
    try:
        wordidfs = json.load(open("wordidfs.json"))
    
    except json.JSONDecodeError:
        wordidfs = {}
    
    phrase = phrase.split()
    queryLength = len(phrase)

    queryVector = []
    visitedWords = set()
    
    #Keeping the order of the words so that future tfidfs are calculated correctly.
    orderedWords = []

    leftDenominator = 0

    #Creating the query vector.
    for word in phrase:
        if(word not in visitedWords):
            
            #Only allowing unique parameters in the idf function.
            if(word not in wordidfs):
                wordidfs[word] = searchdata.get_idf(word)
            
            orderedWords.append(word)
            queryVector.append(math.log(1 + phrase.count(word) / queryLength, 2) * wordidfs[word])
            visitedWords.add(word)

    with open("wordidfs.json", "w") as f:
        json.dump(wordidfs, f, indent = 4, ensure_ascii = False)

    cosSimilarities = []

    #Finding the cosine similarity for each page.
    for link in crawler.jsonDict:
        linkVector = []

        numerator = 0
        leftDenominator = 0
        rightDenominator = 0
        index = 0

        #Creating the vector for the current page.
        for word in orderedWords:
            linkVector.append(searchdata.get_tf(link, word) * wordidfs[word])
            
            #Creating the parts of the cosine similarity formula, to also save time.
            numerator += queryVector[index] * linkVector[index]
            leftDenominator += queryVector[index] ** 2
            rightDenominator += linkVector[index] ** 2

            index += 1
        
        #Calculating the cosine similarity, and accounting for possibly dividing by zero.
        denominator = math.sqrt(leftDenominator) * math.sqrt(rightDenominator)

        cosSimilarity = numerator / denominator if denominator != 0 else 0

        cosSimilarities.append({
            "url": link,
            "title": crawler.jsonDict[link]["title"],
            "score": cosSimilarity * crawler.jsonDict[link]["pageRank"] if boost else cosSimilarity
        })

        #Another progress bar.
        print("Cosine Similarity is", cosSimilarity)

    return sorted(cosSimilarities, key = lambda x: x["score"], reverse = True)[:10]