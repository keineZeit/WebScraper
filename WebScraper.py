
# coding: utf-8

# In[1]:


import urllib3
import re
from bs4 import BeautifulSoup


# In[2]:


class Scraper:
    
    http = urllib3.PoolManager()
    
    def __init__(self):
        pass
        
class BailiiScraper(Scraper):
    
    head = 'www.bailii.org'
    ptc = 'http'
    
    def links(self, years=(1995, 2019)):
        links = []
        mask = self.ptc + '://' + self.head + '/ew/cases/EWHC/Comm/{0}/'
        
        for year in range(years[0], years[1]):
            page = self.http.request('GET', mask.format(str(year)))
            if page.status != 200:
                continue
            soup = BeautifulSoup(page.data, 'html.parser')
            for link in soup.find_all('a', title=True):
                links.append({"year" : year, "link" : link.get('href')})
            
        return links
            
    
    def docs(self, years=(1995, 2019)):
        docs = []
        links = self.links(years)
        mask = self.ptc + '://' + self.head + '{0}'
        
        count = 1
        for link in links:
            page = self.http.request('GET', mask.format(link['link']))
            if page.status != 200:
                continue
            soup = BeautifulSoup(page.data, 'html.parser')
            header = soup.parties
            #body = soup.findAll(attrs={"name": re.compile("para?")})
            body = soup.findAll('p')
            if (header is None or header == []) or (body is None or body == []):
                continue
            
            _body = self.convert_resultset_to_list(body)
            _body = re.sub(r'\n',' ', str(_body))
            
            header = re.sub(r'\n',' | ', header.get_text())
            docs.append({'name' : 'bailii_' + str(link['year']) + '_' + str(count), 'header' : header, 'body' : _body})
            
            count += 1
                
        return docs
    
    def write_to_file(self, docs, path_to_folder):
        count = 1
        for doc in docs:
            filename = doc['name'] + '.txt'
            file = open(path_to_folder + filename,"w")
            file.write(doc['body'])
            file.close()
            count+=1
    
    def convert_resultset_to_list(self, resultset):
        _list = ''
        phrase_to_begin = u'Crown Copyright ©'
        can_write = False
        for _resultset in resultset:
            _resultset = _resultset.find_all_next(string=True)
            for paragraph in _resultset:
                if paragraph == phrase_to_begin:
                    can_write = True
                    continue
                if paragraph == 'BAILII:':
                    return _list.encode('utf-8')
                if (can_write):
                    if paragraph == '\n':
                        continue
                    _list += paragraph + ' '
        return _list.encode('utf-8')


# In[3]:


bailii = BailiiScraper()
docs = bailii.docs(years=(1995, 1999)) # Returns list with docs as dicts(name, header, body)
bailii.write_to_file(docs, 'output/')


# In[ ]:


#print (docs[0]['body']) # TEST

