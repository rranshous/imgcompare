
## given base dir gets the hash for each image
## and generates list of matches
## caches image hashes

import imghdr
from avg import average_hash, hamming
import os.path
from hashlib import md5
from itertools import combinations
import sys
from findfiles import find_files_iter as findfiles
import json

av_cache = {}
av_cache_path = './av_cache.json'

def populate_av_cache():
    print 'pop cache'
    global av_cache
    if os.path.exists(av_cache_path):
        with open(av_cache_path,'r') as fh:
            av_cache = json.load(fh)
    return av_cache

def save_av_cache():
    print 'save cache'
    global av_cache
    with open(av_cache_path,'w') as fh:
        json.dump(av_cache,fh)
    return av_cache

def iter_image_paths(path):
    for path in findfiles(path):
        with open(path,'r') as fh:
            img_type = imghdr.what(fh)
        if img_type:
            print 'found: %s' % path
            yield path

def get_md5(path):
    """ returns the data's md5 @ path endpoint """
    with open(path,'r') as fh:
        return md5(fh.read()).hexdigest()

def get_image_visual_hash(path):
    # first generate the md5 hash of the image data
    # this is the key for the hash lookup
    key = get_md5(path)

    # check the cache for the key
    av_hash = av_cache.get(key)

    # if the cache was a miss calculate
    if not av_hash:
        av_hash = average_hash(path)
        # update our cache
        av_cache[key] = av_hash
    else:
        print 'cache hit'

    print 'determined hash: %s' % av_hash

    return av_hash

def iter_image_hashes(path):
    """
    yields up (image path, image av hash)
    """
    for file_path in iter_image_paths(path):
        av_hash = get_image_visual_hash(file_path)
        yield (file_path, av_hash)


def iter_matches(path):
    # look for matches
    for img1, img2 in combinations(iter_image_hashes(path),2):
        ham = hamming(img1[1],img2[1])
        if ham < 5:
            print 'found match: %s' % ham
            # match found
            yield img1[0], img2[0]


def run(path):

    # TODO: use context manager
    # populate the hash cache
    populate_av_cache()

    for path1, path2 in iter_matches(path):
        print 'match: %s %s' % (path1,path2)

    # save the cache
    save_av_cache()

if __name__ == '__main__':
    path = os.path.abspath(sys.argv[1])
    print 'checking: %s' % path
    run(path)
