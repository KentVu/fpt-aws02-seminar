from chalice import Chalice
import json
from collections import namedtuple
from PIL import Image, ImageFilter
import boto3
import io

app = Chalice(app_name='image-resize')
app.debug = True

S3 = boto3.client('s3')

@app.route('/')
def index():
    return {'hello': 'world'}

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

@app.route('/resize', methods=['PUT'])
def resize():
    request = app.current_request
    data = request.raw_body
    reqobj = json2obj(data)
    print(reqobj.srcs3.bucket, reqobj.srcs3.key)
    srcs3 = reqobj.srcs3
    fileobj = S3.get_object(
        Bucket=srcs3.bucket,
        Key=srcs3.key
    )
    filedata = fileobj['Body'].read()
    src_in_mem = io.BytesIO(filedata)
    src_in_mem.seek(0)
    im = Image.open(src_in_mem)
    dests3 = reqobj.dests3
    resizedFiles = []
    for downscale in [2,4,8]:
        outIm = downscaleImg(im, downscale)
        outF = saveImg2File(outIm, im.format)
        outKey = makeDstFilename(dests3.key, "-%dx%d" % outIm.size)
        S3.upload_fileobj(outF, dests3.bucket, outKey)
        resizedFiles.append(outKey)
    return {
        'bucket': reqobj.srcs3.bucket,
        'key': reqobj.srcs3.key,
        'size': "%dx%d" % im.size,
        'outBucket': dests3.bucket,
        'resized': resizedFiles
    }

def downscaleImg(im, downscale):
    x,y = im.size
    out = im.resize((x//downscale,y//downscale))
    return out

def saveImg2File(out, format):
    outF = io.BytesIO()
    out.save(outF, format)
    outF.seek(0)
    return outF

def makeDstFilename(orgFname, tail):
    dot = orgFname.rfind('.')
    return orgFname[:dot] + tail + orgFname[dot:]

def resize_imgF_to_file(srcFile, downscale):
    im = Image.open(srcFile)
    out = downscaleImg(im, downscale)
    outF = saveImg2File(out, im.format)
    return outF

def resize_img_to_file(im, downFactor):
    describeImage(im)
    outIm = downscaleImg(im,downFactor)
    outF = saveImg2File(outIm, im.format)
    return outF, outIm

def resize_imgf(src, dest, downscale):
    im = Image.open(src)
    describeImage(im)
    out = downscaleImg(im, downscale)
    out.save(dest)
    print("saved ", dest)

def describeImageFile(imFile):
    describeImage(Image.open(imFile))

def describeImage(im):
    print(im.getpixel((256, 256)))
    print(im.format, "%dx%d" % im.size, im.mode)

if __name__ == '__main__':
    import sys
    downscale = 2
    outf = "out.jpg"
    print(__name__)
    resize_imgf(sys.argv[1],sys.argv[2],2)

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
