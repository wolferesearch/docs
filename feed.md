# HTTP API


The QES feed is available via HTTP API. For this the user needs a username and password. Please contact <a href="mailto:sales@wolferesearch.com">Wolfe Sale 
at sales@wolferesearch.com</a> to get username and password setup. 


# Basic Information

Server: http://feed.luoquant.com (The server is currently a non-SSL server, and only support http protocol)

Feed Data Pattern: 

	http://feed.luoquant.com/lquant-factor-feed/<path_to_feed_file>


The URL is protected by a username and password, please speak to wolferesearch sales. 

## Curl command
```sh
curl -u <username>:<password>  -OX  GET 'http://feed.luoquant.com/lquant-factor-feed/GlobalEquityFactors/daily/ANZ/ANZ_19890703.csv’

```



## Python Client Example

```python

from xml.dom import minidom

try:
    # Fall back to Python 2's urllib2
    import urllib2
except ImportError:
    # For Python 3.0 and later
    from urllib import request as urllib2
    


def pp(res):
    '''
        pretty print function
        for xml.
    '''
        
    reparsed = minidom.parseString(res)
    print(reparsed.toprettyxml(indent="\t"))

def client_downloader(username, password, url_path):
    """
        
        Args:
            username: A string username as first arg
            password: A string password as second arg
            url_path: A string url path to the file to 
                      be downloaded
        Desc:
            A client side downloader that downloades 
            the file in question after authtication.
            
            -Uses urllib2 for auth as data dowanload
            -Uses the server returned error messages
            -Parses xml-string to pretty looking xml
        
        NOTE: Tested for python2 and python3
    """
    baseurl = 'http://feed.luoquant.com'
    manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    manager.add_password(None, baseurl, username, password)

    try:
        auth = urllib2.HTTPBasicAuthHandler(manager)
        opener = urllib2.build_opener(auth)
        urllib2.install_opener(opener)
        response = urllib2.urlopen(baseurl + url_path)
        filename = response.url.split("/")[-1]
        with open(filename, 'wb') as f:
            f.write(response.read())
            print("Downloaded and saved! {0}".format(filename))
    except Exception as e:
        print('HTTP ERROR CODE: {0}'.format(e.code))
        err_msg  = e.read()
        if "xml" in err_msg:
            pp(err_msg)
        else:
            print(err_msg)



# for stand alone testing           
if __name__ == "__main__":
    client_downloader("<username>", "<password>", "/lquant-factor-feed/GlobalEquityFactors/daily/ANZ/ANZ_19890704.csv")
```


## R Client Example
```R
library(httr)

# Simple function to download data to temporary file
client_downloader <- function(username, password, url_path){
  

  base_url <- "http://feed.luoquant.com"
  url <- paste0(base_url,url_path)
  response <- GET(url,
                  encode="xml",
                  authenticate(username, password)
  )
  
  if(response$status_code == "200"){
    filename <- tail(strsplit(response$url, "/")[[1]], 1)
    print(paste( filename, "sucessfully downlaoded!", sep = " "))
    bin <- content(response, "raw")
    writeBin(bin, filename)
  }
  else{
    print(paste("HTTP ERROR CODE", response$status_code, sep = ":"))
    if(response$status_code == "404"){
      print("Object not found!")
    }
    if(response$status_code == "403"){
      print("Credentials mismatch!")
    }
  }
}

client_downloader("<username>",
                  "<password>", 
                  "/lquant-factor-feed/GlobalEquityFactors/daily/ANZ/ANZ_19890703.csv"
```
