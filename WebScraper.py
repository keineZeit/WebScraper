
# coding: utf-8

# In[19]:


import urllib3
from bs4 import BeautifulSoup


# In[27]:


class Scraper:
    def __init__(self):
        pass
        
class BailiiScraper(Scraper):
    def docs(self):
        docs = []
        http = urllib3.PoolManager()
        mask = 'http://www.bailii.org/ew/cases/EWHC/Comm/{0}/{1}.html'
        
        for y in range(1996, 1998):
            print ('year ' + str(y))
            for n in range(370, 400):
                page = http.request('GET', mask.format(str(y), str(n)))
                if page.status != 200:
                    continue
                soup = BeautifulSoup(page.data, 'html.parser')
                context = soup.find('p', text='B e f o r e :')
                if context is None:
                    continue
                docs.append(context.find_all_next(string=False))
                
        return docs


# In[28]:


bailii = BailiiScraper()
docs = bailii.docs()


# In[29]:


len(docs)

