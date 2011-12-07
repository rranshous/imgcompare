from PIL import Image

# ty: http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
# ty: http://sprunge.us/WcVJ?py

def average_hash(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.resize((8,8),Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, im.getdata()) / 64.0
    return reduce(lambda x, (y,z): x | (z << y),
                  enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())),
                  0)


def hamming(h1,h2):
    h,d = 0, h1 ^ h2
    while d:
        h += 1
        d &= d - 1
    return h



