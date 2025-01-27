import json
import login

API_URL = "https://oldschool.runescape.wiki/api.php" #we don't need this to change, so might as well set it here

session, token = login.login(API_URL)

biglist = []
continueval = ""
while True: #run until we break
    params = {
        "action": "query",
        "format": "json",
        "list": "allpages", #ask for a list of all pages
        "apnamespace": "0",
        "apfilterredir": "nonredirects", #without redirects
        "aplimit": 500,
        "apcontinue": continueval #starting here
    }
    print('current OSW progress:', len(biglist))
    response = session.get(API_URL, params=params) #this next section is just to clean up the output
    pagelist = response.json()
    pageclean = pagelist['query']['allpages']

    listclean = [] #make an empty list
    for k in range(len(pageclean)):
        listclean.append(str(pageclean[k]['pageid'])) #and now fill that list with comma separated page ids

    listclean = "|".join(listclean) #Now we have a bunch of bar separated pageids

    params = {
        "action": "query",
        "prop": "revisions",
        "rvprop": "content|ids",
        "format": "json", 
        "pageids": listclean,
    }

    response = session.get(API_URL, params=params) #here we ask for all the info on those pageids
    revision = response.json()
    revision = revision['query']['pages'] #here's the info
    revlist = list(revision) #and here's the pageids to iterate by

    for j in range(len(revlist)): #for as many pages as I grabbed...
        page = revision[revlist[j]] #pull out that page
        tempdict = {
            'title': page['title'],
            'contents': page['revisions'][0]['*'],
            'revid': page['revisions'][0]['revid']
        }
        biglist.append(tempdict)
    
    if 'continue' in pagelist: #if we have a continue section
        continueval = pagelist['continue']['apcontinue'] #grab the continue and send it on back to the start
    else: #if no continue section,
        break #stop the while loop

with open('scrape/contents_osw.json', 'w') as outfile:
    json.dump(biglist, outfile)