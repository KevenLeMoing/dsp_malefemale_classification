import requests

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

#Define a size limit for files which be downloaded
# We get this value from the end of notebook entitled "getting_voxforge_data.ipynb"
def has_expected_size(url):
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_length = header.get('content-length', None)
    if content_length and content_length > 2e8:  # 200 mb approx
        return False


print (is_downloadable('http://www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Main/16kHz_16bit/1028-20100710-hne.tgz'))