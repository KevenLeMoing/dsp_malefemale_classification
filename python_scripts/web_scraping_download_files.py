import requests
import pandas as pd
import time
from config import constants

start_time = time.time()

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

# Download a file from an url
def download(url):
    print ("Start to download {}".format(filename), " which has the size {}".format(size))
    if is_downloadable(url):
        r = requests.get(url, allow_redirects=True)
        open(constants.downloads_path+filename, 'wb').write(r.content)
        print ("Finish to download {}".format(filename), " which has the size {}".format(size))


# Load url to be requested
scraping_df = pd.read_csv(constants.scraping_result_path,error_bad_lines=False)

# MAIN SCRIPT
for i in range(len(scraping_df['sub_link'])):
    filename = scraping_df['sub_link'][i]
    size = scraping_df['size'][i]
    date = scraping_df['date'][i]

    # Url setted
    url = constants.voxforge_url + filename
    download(url)

print("")
print("--- %s seconds ---" % (time.time() - start_time))
print("")