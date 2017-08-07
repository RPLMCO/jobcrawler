url = 'https://jobs.rogers.com/search/?q=&sortColumn=referencedate&sortDirection=desc&startrow='

start_urls =[] 
increment = 0
for i in range(14):
	new_url = url+str(increment)
	start_urls.append(new_url)
	increment += 25
print (start_urls)