import requests
import time


start_time = time.time()
t = requests.get("https://gitlab.com/kiril159/Finch/-/raw/829d0a8d3cdf228306f02001bbc8c1b25e3d8336/Elastic/elast_to_csv.py")
#print(t.content)
print("--- %s seconds ---" % (time.time() - start_time))