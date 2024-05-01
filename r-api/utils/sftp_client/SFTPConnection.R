library(RCurl)
library(R6)
SFTPConnection <- R6Class(
  public = list (
    con = NULL,
    host = NULL,
    userpwd = NULL,
    initialize = function(host, userpwd) {
      self$host <- host
      self$userpwd <- userpwd
    },
    list = function(path, pattern = NULL) {
      url <- sprintf("sftp://%s/%s",self$host,path)
      if (!is.null(self$con)) {
        files <- getURL(url, userpwd = self$userpwd,
                        ftp.use.epsv = FALSE,
                        dirlistonly = TRUE, 
                        curl = self$con)
      } else {
        files <- getURL(url, userpwd = self$userpwd,
               ftp.use.epsv = FALSE,
               dirlistonly = TRUE)
        self$con <- getCurlHandle(ftp.use.epsv = FALSE)
      }
      files <- strsplit(files, "\r*\n")[[1]]
      if (!is.null(pattern)) {
        return(files[grep(pattern,files)])
      }
      return(files)
    },
    get = function(path) {
      url <- sprintf("sftp://%s/%s",self$host,path)
      if (!is.null(self$con)) {
        txt = getURL(url = url, curl = self$con, userpwd = userpwd)
      } else {
        txt = getURL(url = url, userpwd = userpwd)
        self$con <- getCurlHandle(ftp.use.epsv = FALSE)
      }
      return(txt)
    },
    copy = function(dir, files, outdir = getwd()) {
      for (f1 in files) {
        print(f1)
        txt <- self$get(sprintf('%s/%s',dir,f1))
        outfile <- file(basename(f1), "wb")
        writeChar(txt, sprintf('%s/%s',outdir,outfile))
        close(outfile)
      }
    },
    info = function() {
      if (is.null(self$con)) {
        stop("Not Connected")
      }
      return(RCurl::getCurlInfo(self$con))
    }
  )
)

if (F) {
	## Usage
	connection <- SFTPConnection$new("<hostname>","<username>:<password>")
	files <- connection$list("uploads/MacroAgg_Russell_daily/2022/","R1K_USD")
	connection$copy("uploads/MacroAgg_Russell_daily/2022/",files)
}
