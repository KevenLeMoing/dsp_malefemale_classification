import requests
import pandas as pd

url_voxforge = "http://www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Main/16kHz_16bit/"

path_to_save = "/Users/kevenlemoing/Sites/sandvik_code_assignement/data/downloads/"

# Check if the url contain a downloadable ressource
def is_downloadable(url):
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

#@TODO revoir le check sur la longueur du fichier (faire d'abord convertion puis calcul du max)
def has_expected_size(url):
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_length = header.get('content-length', None)
    if content_length and content_length > 2e8:  # 200 mb approx
        return False

def download(url):
    print ("Start to download {}".format(filename), " which has the size {}".format(size))
    if is_downloadable(url): #and has_expected_size(url):
        r = requests.get(url, allow_redirects=True)
        open(path_to_save+filename, 'wb').write(r.content)
        print ("Start to download {}".format(filename), " which has the size {}".format(size))


scraping_df = pd.read_csv('/Users/kevenlemoing/Sites/sandvik_code_assignement/data/scraping_result.csv',error_bad_lines=False)

for i in range(len(scraping_df['sub_link'])):
    filename = scraping_df['sub_link'][i]
    size = scraping_df['size'][i]
    date = scraping_df['date'][i]

    # Url setted
    url = url_voxforge + filename
    download(url)