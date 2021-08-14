import os
import sys
import numpy as np
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Read URL from console
if '-url' in sys.argv:
    url = sys.argv[sys.argv.index('-url') + 1]

else:
    raise 'URL not found'
    
if '-skip' in sys.argv:
    skip = int(sys.argv[sys.argv.index('-skip') + 1])
else:
    skip=0

# Predefined list and hashmap
hrefs = []
hashmap={}

# Function
def extract_html(url, save_dir, chapter_name):
    """
    Read the url of each chapter;
    novel_title as the name of the folder;
    chapter_name, extracted from the content page, which will be used to name the article file.
    """
    r=requests.get(url)
    r.encoding='utf-8'
    soup = BeautifulSoup(r.text, features='lxml')
    
    # Extract chapter title of the article from this ESJZone page.
    title_h2=soup.find_all('h2')[0].get_text()
    # Extract the article
    content = soup.find('div',attrs={'class': 'forum-content mt-3'})
    # Create a html file and write content into the file.
    with open('./{}/{}.html'.format(save_dir, chapter_name), 'w', encoding="utf-8") as f:
        f.write(title_h2)
        f.write(content.__str__())


r=requests.get(url)
r.encoding='utf-8'
soup = BeautifulSoup(r.text, features='lxml')

novel_dict = soup.find('div', attrs={'class': 'product-gallery text-center mb-3'})
novel_title = novel_dict.find('img', alt=True)['alt']
novel_title=''.join(x for x in novel_title if x not in '\/:*?<>|')

save_dir='./ESJZone/{}/'.format(novel_title)
if not os.path.exists(save_dir):
    os.mkdir(save_dir)
    
# Check novel_title
print(novel_title)

content = soup.find('div', attrs={'id': 'chapterList'})
links = content.find_all('a')
chapters = content.find_all('p', attrs={'class': None})


for i, link_i in enumerate(tqdm(links)):
    if i < skip:
        continue
    url = link_i.get('href')
    chapter_name0 = chapters[i].get_text()
    chapter_name0 = ''.join(x for x in chapter_name0 if x not in '\/:*?<>|')
    if chapter_name0 in hashmap:
        chapter_name=chapter_name0+'-{}'.format(i)
        hashmap[chapter_name0]+=1
    else:
        chapter_name=chapter_name0
        hashmap[chapter_name0]=1
        
    extract_html(url, save_dir, chapter_name)