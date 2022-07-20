import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
import sqlite3
import random

#-------------------------------------------------------------------------

#general function to collect data from the site
def parselinks(search_page):
    data={'EntrezSystem2.PEntrez.PMC.Pmc_ResultsPanel.Pmc_DisplayBar.PageSize': '100'}
    encode_data=urllib.parse.urlencode(data).encode('utf-8')
    request=urllib.request.Request(search_page,headers=hdr)
    html = urllib.request.urlopen(request,data=encode_data).read()
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all("div","title"):
        href=re.findall('href="(.+?)"',str(link))
        full_url='https://www.ncbi.nlm.nih.gov'+href[0]
        print(full_url)
        link_for_analyse=Website(full_url)
    print('Data collection ended')  

#collect and count all cell markers using template
def parsemarkers(article):
    count_markers=dict()
    markers=re.findall('CD[0-9]+[a-z|A-Z]*',article)
    for marker in markers:
        marker=marker.upper()
        count_markers[marker]=count_markers.get(marker,0)+1
    return count_markers

#collect and count the names of cell types from the approved list
def parsenames(article,list_of_cells):
    count_cells=dict()
    for cell in list_of_cells:
        count_cells[cell]=article.count(cell)+article.count(cell.capitalize())\
                           +article.count(cell.lower())+article.count(cell.replace('-',' '))
    return count_cells

#put data about markers and cell names in an automatically filled table
def append_in_table(table,obj_dict,art_id):
    conn = sqlite3.connect('cells_markers.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT * FROM '+table)
    column_names=list(map(lambda x: x[0], cur.description))
    cur.execute('INSERT OR IGNORE INTO '+table+'(article_id) VALUES (?)',(art_id,))
    for key,val in obj_dict.items():
        key=key.replace('-','_').replace(' ','_')
        if key in column_names:
            cur.execute('UPDATE '+table+' SET '+key+'='+str(val)+' WHERE article_id=(?)',(art_id,))
        else:
            cur.execute('ALTER TABLE '+table+' ADD '+key+' TEXT')
            cur.execute('UPDATE '+table+' SET '+key+'='+str(val)+' WHERE article_id=(?)',(art_id,))
    conn.commit()
    cur.close()
#-------------------------------------------------------------------------

class Website:
    '''
    initialization of the site, checking the length of the article
    (we will exclude from the analysis articles containing
    only an introduction), assigning an id
    '''
    def __init__(self,search_url):
        
        request=urllib.request.Request(search_url,headers=hdr)
        html = urllib.request.urlopen(request)
        soup = BeautifulSoup(html, 'html.parser')

        all_text=soup.find('article')
        try:
            soup.find(id="reference-list").decompose()
        except:
            pass
        article=str(all_text)

        print(len(article))
        if len(article)<10000:
            print('not full article, just abstract!',search_url)
        else:
            text=all_text.get_text()
            doi=re.findall('doi:\s(\S+[0-9])',text)
            if len(doi)==0:
                doi.append(str(random.randint(10000,20000)))
            art_id=doi[0].replace('.','_').replace('/','_')
            self.parse_markers(article,art_id)
            self.parse_names(article,art_id)

    '''
    launching functions for collecting cell markers and
    cell names, as well as putting this information into a database
    '''
    def parse_markers(self,article,art_id):
        conn = sqlite3.connect('cells_markers.sqlite')
        cur = conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS Collect_Markers(article_id UNIQUE)''')
        cell_markers=parsemarkers(article)
        print(cell_markers)
        append_in_table('Collect_Markers',cell_markers,art_id)

        conn.commit()
        cur.close()

    def parse_names(self,article,art_id):
        
        conn = sqlite3.connect('cells_markers.sqlite')
        cur = conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS Collect_Cells(article_id UNIQUE)''')
        cell_types=parsenames(article,blood_cells)
        print(cell_types)
        append_in_table('Collect_Cells',cell_types,art_id)

        conn.commit()
        cur.close()
    
#--------------------------------------------------------------------------------

if __name__ == '__main__':

    hdr={'user-agent':'Chrome/102.0.5005.63'}

    #list of explored cell types
    blood_cells=['Monocyte','T-lymphocyte','B-lymphocyte','Natural Killer',\
                 'Neutrophil','Eosinophil','Basophil','Macrophage','Erythrocyte','Platelet']

    '''
    path selection procedure: automatic analysis of the first 100 links on request
    or "manual mode" with analysis of links from the list
    '''
    while True:
        print(' Monocyte\n','Neutrophil\n','Eosinophil\n','Basophil\n','Macrophage\n',\
                 'T-lymphocyte\n','B-lymphocyte\n','Natural Killer\n','Erythrocyte\n','Platelet')
        experiment_cell=input('Which type of cell would you like to explore? ')
        if len(experiment_cell)<1:
            break 
        elif experiment_cell not in blood_cells:
            print('Please copy cell type name from list')
        else:
            print('Do you want to collect data automatically? ')
            auto_man_reg=input('Press y/n ')
            if auto_man_reg=='y':
                start_url='https://www.ncbi.nlm.nih.gov/pmc/?term='
                end_url='+markers'
                url=start_url+experiment_cell.lower().replace(' ','+')+end_url
                links=parselinks(url)
            else:
                manual_way=input('Enter additional links separated by comma+space: ')
                man_list=manual_way.replace("'","").split(', ')
                for link in man_list:
                    link_for_analyse=Website(link)







    

