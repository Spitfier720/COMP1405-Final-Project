#Self-reminder that these are Python files, not actual modules.
import json
import matmult
import webdev

jsonDict = {}

#A simple function to get data from all our websites using BFS.
def crawl(seed):
    #Since everything must be initialized in the crawl function.
    open("wordidfs.json", "w").close()
    open("data.json", "w").close()

    #Variables that will help us store the links we have yet to search, and to prevent any duplicate links entering.
    linkQueue = {seed}
    visited = set()

    #Using this to merge relative links to base links.
    baseURL = seed.replace("//", "/").split("/")
    
    pageCount = 0

    IDDict = {}

    #We will parse each page until there are no more direct links in our queue.
    while(linkQueue):
        curDict = {}
        links = []
        
        pageCount += 1
        curDict["ID"] = pageCount - 1

        curLink = linkQueue.pop()
        visited.add(curLink)

        IDDict[pageCount - 1] = curLink

        #A progress bar.
        print("Processing", curLink)

        #Changing all newline characters to whitespace for better parsing.
        webData = webdev.read_url(curLink).replace("\n", " ")

        #Getting the title from the webData so that we don't have to search for it later(a little microoptimization).
        webData = webData[webData.find("<title"):]
        webData = webData[webData.find(">") + 1:]
        curDict["title"] = webData[:webData.find("<")]

        #Reading all the webData
        while(True):
            #Cutting down the string methodically until we get our information.
            webData = webData[webData.find("<") + 1:].strip()
            
            #When we have gone through all of the HTML elements.
            if(not webData):
                break
            
            #Using the first letter of the HTML element to find 
            htmlElement = webData[0]
            
            if(htmlElement == "a"):
                #Get the link(absolute or relative) in the href.
                webData = webData[webData.find("href=\"") + 6:]
                directLink = webData[:webData.find("\"")].split("/")

                #Link is relative
                if(directLink[0] == "."):
                    #Create a new list reference so that the original baseURL is not changed.
                    newURL = list(baseURL)

                    #Using reverse indexing to add our base URL to the relative URL.
                    ndx = -1
                    
                    #Changing the new link according to our relative link.
                    for x in range(len(directLink) - 1, 0, -1):
                        newURL[ndx] = directLink[x]
                        ndx -= 1

                    #Since two slashes are lost, I re-add it manually since join() would only add one.
                    links.append("http://" + "/".join(newURL[1:]))

                else:
                    links.append("http://" + "/".join(directLink[1:]))
                
                #Prevent the same page from unnecessarily being parsed twice
                if(links[-1] not in visited):
                    linkQueue.add(links[-1])
                
                #Add new link to visited, if the link is old, it is not added due to the nature of a set.
                visited.add(links[-1])
            
            #Since there can be other HTML elements we don't need, an elif must be used.
            elif(htmlElement == "p"):
                #Account for off-by-one error.
                webData = webData[webData.find(">") + 1:]
                words = webData[:webData.find("<")].strip().split(" ")
                
                curDict["wordCount"] = {}
                totalWords = 0

                for word in words:
                    curDict["wordCount"][word] = curDict["wordCount"].setdefault(word, 0) + 1
                    totalWords += 1
                
                curDict["totalWords"] = curDict.setdefault("totalWords", 0) + totalWords
            
            #For any other HTML element, we need to make sure that we skip it.
            else:
                webData = webData[webData.find(">") + 1:]
        
        curDict["links"] = links
        jsonDict[curLink] = curDict
    
    with open("id.json", "w") as f:
        json.dump(IDDict, f, indent = 4, ensure_ascii = False)
    
    pageRank(pageCount)
    
    return pageCount

#Creating our adjacency matrix for our page rankings.
def pageRank(N):
    adjacencyMatrix = [[0 for x in range(N)] for y in range(N)]
    IDDict = json.load(open("id.json"))
    alpha = 0.1

    #Creation of adjacency matrix, which shows the probability of going to any page from any page.
    for entry in jsonDict:
        for link in jsonDict[entry]["links"]:
            if(jsonDict[entry]["links"]):
                adjacencyMatrix[jsonDict[entry]["ID"]][jsonDict[link]["ID"]] = 1 / len(jsonDict[entry]["links"])
            
            else:
                adjacencyMatrix[jsonDict[entry]["ID"]] = [1 / N for x in range(N)]
    
    adjacencyMatrix = matmult.mult_scalar(adjacencyMatrix, 1 - alpha)
    adjacencyMatrix = [[num + (alpha / N) for num in row] for row in adjacencyMatrix]
    
    
    curVector = [[1 / N for x in range(N)]]
    pastVector = [[]]

    #Since we can't do the euclidean distance yet, I've set the Euclidean Distance to the highest possible value.
    euclideanDist = float('inf')

    #Finding all the pages' probability of getting there.
    while(euclideanDist and euclideanDist > 0.0001):

        #Yet another progress bar.
        print("Euclidean distance between vectors:", euclideanDist)

        pastVector = list(curVector)
        curVector = matmult.mult_matrix(curVector, adjacencyMatrix)

        euclideanDist = matmult.euclidean_dist(curVector, pastVector)
    
    for x in range(N):
        jsonDict[IDDict[str(x)]]["pageRank"] = curVector[0][x]
    
    with open("data.json", "w") as f:
        json.dump(jsonDict, f, indent = 4, ensure_ascii = False)