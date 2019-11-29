##!python3.7
import boto3
import urllib.request
import sys

#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_function
def download_function(fname, unzipDir=""):
    lam = boto3.client('lambda')
    response = lam.get_function(
        FunctionName=fname
        #,Qualifier=Nil
    )
    url = response['Code']['Location']
    #https://stackabuse.com/download-files-with-python/
    funcZip = fname + '.zip'
    urllib.request.urlretrieve(url, funcZip)
    if unzipDir:
        import zipfile
        with zipfile.ZipFile(funcZip, "r") as zip_ref:
            zip_ref.extractall(unzipDir)

if __name__ == "__main__":
    #download_function('VuNG-login')
    #download_function('Bach-login')
    download_function(sys.argv[1], sys.argv[2])
