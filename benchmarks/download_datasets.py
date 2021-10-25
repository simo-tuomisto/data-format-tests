import os.path
import requests
import zipfile
import tarfile

# Define datasets
datasets = {
    'Deep weeds - images': {
        'filename': 'images.zip',
        'extract_path': 'data/deep',
        'google_id': '1xnK3B6K6KekDI55vwJ0vnc2IGoDga9cj',
        'compressed': True,
    },
    'Deep weeds - labels': {
        'filename': 'labels.csv',
        'url': 'https://raw.githubusercontent.com/AlexOlsen/DeepWeeds/master/labels/labels.csv'
    }
}

CHUNK_SIZE = 32768

def download_dataset(url, filepath):
    data_request = requests.get(url)
    if data_request.status_code != 200:
        raise Exception('Failure at downloading!')
    print('Saving dataset to: %s' % filepath)
    with open(filepath, 'wb') as datafile:
        for chunk in data_request.iter_content(CHUNK_SIZE):
            datafile.write(chunk)

def download_drive_dataset(google_id, filepath):
    
    base_url = "https://docs.google.com/uc?export=download"
    session = requests.Session()

    data_request = session.get(base_url, params = { 'id' : google_id }, stream=True)
    token = get_confirm_token(data_request)
    
    if token:
        params = { 'id' : google_id, 'confirm' : token }
        data_request = session.get(base_url, params=params, stream=True)
        
    with open(filepath, "wb") as datafile:
        for chunk in data_request.iter_content(CHUNK_SIZE):
            if chunk:
                datafile.write(chunk)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def extract_file(filename, extract_path):
    if '.zip' in filename:
        datafile = zipfile.ZipFile(filename)
    elif '.tar' in filename or '.tgz' in filename:
        datafile = tarfile.open(filename)
    else:
        raise ValueError('Unknown compression format!')
    datafile.extractall(path=extract_path)
    datafile.close()

for dataset_name, dataset_info in datasets.items():
    filename = dataset_info['filename']
    if not os.path.isdir('data'):
        os.mkdir('data')
    filepath = os.path.join('data', filename)
    if not os.path.isfile(filepath):
        print('Downloading dataset: %s' % dataset_name)
        if 'url' in dataset_info:
            download_dataset(dataset_info['url'], filepath)
        if 'google_id' in dataset_info:
            download_drive_dataset(dataset_info['google_id'], filepath)
    if dataset_info.get('compressed', False):
        print('Extracting dataset: %s' % dataset_name)
        extract_path = dataset_info.get('extract_path', 'data')
        extract_file(filepath, extract_path)