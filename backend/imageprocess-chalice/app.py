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
    #data = request.json_body
    #query_params = request.query_params
    data = request.raw_body
    # Parse JSON into an object with attributes corresponding to dict keys.
    #reqobj = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    reqobj = json2obj(data)
    print(reqobj.srcs3.bucket, reqobj.srcs3.key)
    srcs3 = reqobj.srcs3
    fileobj = S3.get_object(
        Bucket=srcs3.bucket,
        Key=srcs3.key
    )
    filedata = fileobj['Body'].read()
    #src_in_mem = io.BytesIO()
    #src_in_mem.write(fileobj['Body'].read())
    src_in_mem = io.BytesIO(filedata)
    #describeImageFile(fileobj['Body'])
    #describeImageFile(src_in_mem)
    #describeImage(Image.frombytes())
    #outF, im, outIm = resize_imgF_to_file(src_in_mem)
    im = Image.open(src_in_mem)
    outIm = downscaleImg(im, downscale)
    outF = saveImg2File(outIm, im.format)
    dests3 = reqobj.dests3
    S3.upload_fileobj(outF, dests3.bucket, dests3.key)
    return {
        'bucket': reqobj.srcs3.bucket,
        'key': reqobj.srcs3.key,
        'size': "%dx%d" % im.size,
        'resized': "%dx%d" % outIm.size
    }

def resize_imgF_to_file(srcFile, downscale):
    im = Image.open(srcFile)
    out = downscaleImg(im, downscale)
    #outF, outIm = resize_img_to_file(im, 2)
    #outF = io.BytesIO()
    #saveImg2File(out, outF, im)
    outF = saveImg2File(out, im.format)
    return outF

def saveImg2File(out, format):
    outF = io.BytesIO()
    out.save(outF, format)
    outF.seek(0)
    return outF

def resize_img_to_file(im, downFactor):
    describeImage(im)
    outIm = downscaleImg(im,downFactor)
    outF = saveImg2File(outIm, im.format)
    return outF, outIm

def downscaleImg(im, downscale):
    x,y = im.size
    out = im.resize((x//downscale,y//downscale))
    return out

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
