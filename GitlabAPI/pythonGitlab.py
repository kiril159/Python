import time
import gitlab
import requests

gl = gitlab.Gitlab()
project = gl.projects.get(f'kiril159/Finch')
sum1 = 0
sum2 = 0

for i in range(30):
    start_time1 = time.time()
    t1 = project.files.get(file_path=f'Elastic/elast.py', ref='master')
    sum1 += time.time() - start_time1
    start_time2 = time.time()
    t2 = requests.get("https://gitlab.com/kiril159/Finch/-/raw/"
                      "829d0a8d3cdf228306f02001bbc8c1b25e3d8336/Elastic/elast_to_csv.py")
    sum2 += time.time() - start_time2
    print(i)


print(f"--- python-new_gitlab is {sum1/30} seconds ---")
print(f"--- API Gitlab is {sum2/30} seconds ---")
