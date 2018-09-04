
# coding: utf-8

# In[11]:


import urllib
from bs4 import BeautifulSoup


# In[69]:


class Scraper:
    def __init__(self):
        pass
        
class BailiiScraper(Scraper):
    def parse(self):
        http = urllib3.PoolManager()
        page = http.request('GET', 'http://www.bailii.org/ew/cases/EWHC/Comm/1995/1.html')
        soup = BeautifulSoup(page.data)
        return soup.body.find('p', text='B e f o r e :').find_all_next(string=False)


# In[70]:


bailii = BailiiScraper()
print(bailii.parse())

