### R Class to work with optimizer

library(httr)
library(R6)
library(jsonlite)

qes.microsvc.type.RISKMODEL <- 1
qes.microsvc.type.OPTIMIZATION <- 2
qes.microsvc.type.ATTRIBUTION <- 3
qes.microsvc.type.HEDGEBUILDER <- 9



#' qes.microsvc.Template
#' Generic Template Base Class
#' 
{
qes.microsvc.Template <- R6Class(
  "QESTemplate",
  public = list(
    conn = NULL,
    val = NULL,
    json = NULL,
    initialize = function(conn,val) {
      setup(val)
    },
    setup = function(conn,val){
      self$conn <- conn
      self$json <- fromJSON(toJSON(val$CONTENT))
      val$CONTENT <- NULL
      self$val <- val
    },
    name = function() {
      return(self$val$NAME)
    },
    type = function() {
      return(self$val$TYPE)
    },
    description = function() { 
      return(self$val$DESCRIPTION)
    },
    content = function() {
      return(self$json)
    },
    save = function(name) {
      self$json$`__name__` <- name
      t1 <- switch(self$type(),
             `Risk-Model` = 'risk-model',
             `Optimization` = 'optimization',
             stop('Type not supported'))
      self$conn$post(paste0('template/',t1),self$json)
    }
  )
)
}

#' qes.microsvc.OptimizationTemplate
#' Optimization Template
#' 
{
qes.microsvc.OptimizationTemplate <- R6Class(
  "QESOptimizationTemplate",
  inherit = qes.microsvc.Template,
  public = list (
    initialize = function(conn,raw){
      self$setup(conn,raw)
    },
    get_target_risk = function() {
      return(self$json$target_risk)
    },
    set_target_risk = function(target_risk) {
      self$json$target_risk <- target_risk
    },
    get_bounds = function() {
      c(self$json$lb, self$json$ub)
    },
    set_bounds = function(bounds) {
      self$json$lb <- bounds[1]
      self$json$ub <- bounds[2]
    },
    set_objective = function(objective) {
      self$json$objective <- objective
      return(self)
    },
    max_ADV_trading_participation = function() {
      return(self$json$max_ADV_trading_participation)
    },
    set_max_ADV_trading_participation = function(maxADVPart) {
      self$json$max_ADV_trading_participation <- maxADVPart 
    },
    max_ADV_holding_participation = function() {
      return(self$json$max_ADV_holding_participation)
    },
    set_max_ADV_holding_participation = function(maxADVPart) {
      self$json$max_ADV_holding_participation <- maxADVPart 
    },
    get_max_turnover = function() {
      return(self$json$turnover)
    },
    set_max_turnover = function(turnover) {
      self$json$turnover <- turnover
    },
    set_min_long_weight = function(min_long_weight) {
      self$json$min_long_weight <- min_long_weight
    },
    set_max_long_weight = function(max_long_weight) {
      self$json$max_long_weight = max_long_weight
    },
    set_min_short_weight = function(min_short_weight) {
      self$json$min_short_weight <- min_short_weight
    },
    set_max_short_weight = function(max_short_weight) {
      self$json$max_short_weight = max_short_weight
    },
    set_min_holding = function(min_holding) {
      self$json$min_holding = min_holding
    },
    set_max_number_securities = function(max_securities) {
      self$json$limit_number <- max_securities
    },
    set_risk_model = function(risk_model_id) {
      self$json$risk_model <- list(risk_model_id = risk_model_id)
    },
    get_objective = function() {
      self$json$objective
    },
    get_benchmark = function() {
      self$json$benchmark
    },
    set_benchmark = function(benchmark) {
      self$json$benchmark <- benchmark
      self$json$use_benchmark <- T
    },
    set_use_adv = function(use_adv) {
      self$json$use_ADV <- use_adv
    },
    set_implied_alpha = function(implied_alpha) {
      self$json$implied_alpha <- implied_alpha
    },
    set_lambda = function(lambda) {
      self$json$lambda <- lambda
    },
    set_soft_turnover_penalty = function(soft_turnover_penalty) {
      self$json$soft_turnover_penalty <- soft_turnover_penalty
    },
    set_soft_relative_weight_penalty = function(soft_relative_weight_penalty) {
      self$json$soft_relative_weight_penalty <- soft_relative_weight_penalty
    },
    set_relative_weight_min = function(relative_weight_min) {
      self$json$relative_weight_min <- relative_weight_min
    },
    set_relative_weight_max = function(relative_weight_max) {
      self$json$relative_weight_max <- relative_weight_max
    },
    set_use_tcm = function(use_tcm) {
      self$json$use_tcm <- use_tcm
    },
    set_transaction_model = function(transaction_model) {
      self$json$transaction_model <- transaction_model
    },
    set_trans_cost = function(trans_cost) {
      self$json$trans_cost <- trans_cost
    }
  )
)
}


#' qes.microsvc.RiskModelTemplate
#' Risk Model Template
{
qes.microsvc.RiskModelTemplate <- R6Class(
  "QESRiskModelTemplate",
  inherit = qes.microsvc.Template,
  public = list(
    initialize = function(conn,raw){
      self$setup(conn,raw)
    },
    factors = function() {
      self$json$factors
    },
    add_factor = function(mnemonic, name) {
      self$json$factors <- rbind(self$json$factors,c(mnemonic,name))
    },
    meta = function() {
      self$json$meta
    },
    add_meta = function(mnemonic, name) {
      self$json$factors <- rbind(self$json$meta,c(mnemonic,name))
    },
    cov_matrix_args = function() {
      self$json$covArgs
    },
    set_cov_matrix_interval = function(interval) {
      self$json$covArgs$interval <- interval
    },
    set_cov_matrix_var_half_life = function(var_half_life) {
      self$json$covArgs$var.period <- var_half_life
    },
    set_cov_matrix_covar_half_life = function(covar_half_life) {
      self$json$covArgs$cov.period <- covar_half_life
    },
    options = function() {
      self$json$options
    },
    set_specific_risk_shrinkage = function(shrinkage) {
      if (shrinkage > 1) {
        stop('Shrinkage cannot be greater than one')
      } 
      if (shrinkage < 0) {
        stop('Shrinkage cannot be less than 0')
      }
      self$options$spRisk$shrinkage <- shrinkage
    }
    
  )
)
}

# qes.microsvc.parse_template <- function(content) {
#   x1 <- fromJSON(content,simplifyVector = F)
#   lapply(x1,function(v) fromJSON(toJSON(v)))
# }

#' qes.microsvc.Conn
#' Connection Class
{
qes.microsvc.Conn <- R6Class(
  "QESConnection",
  public = list(
    URL = NULL,
    username = NULL,
    password = NULL,
    jobs = NULL,
    initialize = function(URL = 'https://feed.luoquant.com',
                          username, password){
      self$URL <- URL
      self$username <- username
      self$password <- password
    },
    .authenticate = function(){
      httr::authenticate(self$username, self$password)
    },
    post = function(svc,body) {
      response <- httr::POST(paste0(self$URL,'/',svc),
                      body = body,
                      self$.authenticate(),
                      encode="json")
      rawToChar(response$content)
    },
    delete = function(endpoint) {
      response <- httr::DELETE(paste0(self$URL,'/',endpoint),
                             self$.authenticate())
      rawToChar(response$content)
    },
    upload_file = function(endpoint,file, name) {
      file.1 <- upload_file(file)
      print(paste0(self$URL,'/',endpoint))
      response <- POST(paste0(self$URL,'/',endpoint),
                       body = list(file = file.1,name=name),
                       self$.authenticate(),
                       add_headers("Content-Type" = "multipart/form-data"))
      return(rawToChar(response$content))
    },
    .get = function(svc) {
      response <- httr::GET(paste0(self$URL,'/',svc),self$.authenticate())
    },
    get = function(svc) {
      response <- self$.get(svc)
      rawToChar(response$content)
    },
    .jobs = function() {
      if (is.null(self$jobs)){
        self$refresh_jobs()
      }
      return(self$jobs)
    },
    refresh_jobs = function() {
      jobs <- fromJSON(self$get('job'))
      jobs$STARTTIME <- as.POSIXct(as.Date('1970-01-01')) + jobs$STARTTIME/1e3
      jobs$ENDTIME <- as.POSIXct(as.Date('1970-01-01')) + jobs$ENDTIME/1e3

      idx <- order(jobs$STARTTIME,decreasing = T)
      jobs <- jobs[idx,]
      self$jobs <- jobs
      return(TRUE)
    },
    failed_job = function(type) {
      subset(self$.jobs(),STATUS == 'ERROR' & TYPEID %in% type)
    },
    success_job = function(type) {
      subset(self$.jobs(),STATUS == 'SUCCESS' & TYPEID %in% type)
    },
    get_template = function(type, name) {
      v <- fromJSON(self$get(sprintf('template/%s?type=%s',name,type)),simplifyVector = FALSE)
      if (length(v) > 0) {
        v <- v[[1]]
        if (type == qes.microsvc.type.RISKMODEL) {
          return(qes.microsvc.RiskModelTemplate$new(self,v))
        } else if (type == qes.microsvc.type.OPTIMIZATION) {
          return(qes.microsvc.OptimizationTemplate$new(self,v))
        } else {
          return(v)
        }
      } else {
        return(NULL)
      }
    },
    
    templates = function() {
      templates <- fromJSON(self$get('template'),simplifyVector = FALSE)
      lapply(templates,function(t) {
        switch(t$TYPE,
               'Risk-Model' = qes.microsvc.RiskModelTemplate$new(self,t),
               'Optimization' = qes.microsvc.OptimizationTemplate$new(self,t),
               t)
        })
    },
    risk_templates = function() {
      l1 <- self$templates()
      idx <- sapply(l1,function(x) x$type() == 'Risk-Model')
      return(l1[idx])
    },
    optimization_templates = function() {
      l1 <- self$templates()
      idx <- sapply(l1,function(x) x$type() == 'Optimization')
      return(l1[idx])
    },
    upload_portfolio = function(id,filename) {
      httr::POST(paste0(self$URL,'/portfolio'),
                 body = list(
                   portfolioName = id,
                   file = upload_file(filename)
                 ),
                 self$.authenticate()
                 )
    },
    get_risk_model_builder = function() {
      return(qes.microsvc.RiskModel$new(self))
    },
    get_optimizer = function() {
      return(qes.microsvc.Optimizer$new(self))
    },
    get_catalog = function() {
      return(qes.microsvc.Catalog$new(self))
    }
  )

)
}


#' qes.microsvc.EntitySvc
#' Entity service class (Base)
{
qes.microsvc.EntitySvc <- R6Class(
  "EntityService",
  public = list(
    conn = NULL,
    uuid = NULL,
    svc = NULL,
    version = 1,
    initialize = function(conn, svc,uuid, version = 1) {
      self$conn <- conn
      self$uuid <- uuid
      self$svc <- svc
      self$version = version
    },
    info = function() {
      if (self$version == 1) {
        return(self$conn$get(paste0(self$svc,'/',self$uuid)))
      } else if (self$version == 2) {
        return(self$conn$get(paste0('job/info/',self$uuid)))
      } else {
        stop(sprintf("Version [%s] not supported",self$version))
      }
      
    },
    get = function(path) {
      self$conn$get(paste0(self$svc,'/',self$uuid,'/',path))
    },
    logs = function() {
      if (is.null(self$uuid)) {
        return("No Logs. Either attach an older request or start a new request");
      }
      return(self$conn$get(paste0('logs/',self$uuid)))
    },
    get_rdata = function(path) {
      res <- self$conn$.get(paste0(self$svc,'/',self$uuid,'/',path))
      if (res$status_code == 200) {
        con = rawConnection(res$content)
        return(readRDS(gzcon(con)))
      } else {
        print(rawToChar(res$content))
        stop(paste("Failed to get data for ",path))
      }
    },
    getdf = function(path) {
      content <- self$conn$get(paste0(self$svc,'/',self$uuid,'/',path))
      read.table(text=content,sep=',',header=TRUE, check.names = F)
    },
    wait = function(max_wait_secs = 300) {
      ws <- 0
      info <- fromJSON(self$info())
      while (info$status == 'STARTED' & ws < max_wait_secs) {
        Sys.sleep(5)
        info <- fromJSON(self$info())
        ws <- ws + 5
      }
      return(info)
    },
    get_job_output = function() {
      return(self$get_output())
    },
    get_output = function() {
      if (is.null(self$uuid)) stop("UUID is null. Cannot proceed. Did you forget to run or attach old id")
      info = fromJSON(self$info())
      if (is.null(info)) {
        stop("Job status unknown??")
      }
      if (info$status != 'SUCCESS') {
        stop(sprintf("[%s]  is not in success state ==> [%s]",self$uuid,status))
      }
      content = self$conn$get(sprintf('job/content/%s',self$uuid))
      files = read.table(text=content,sep=',',header=TRUE, check.names = F)
      return(qes.microsvc.JobOutput$new(conn = self$conn, uuid = self$uuid, files = files))
    }
    
  )
)
}

#' qes.microsvc.JobOutput
#' Generic Job Output Class (Base)

{
qes.microsvc.JobOutput <- R6Class(
  classname = "JobOutput",
  public = list(
    conn = NULL,
    uuid = NULL,
    udata  = NULL,
    data = NULL,
    files = NULL,
    initialize = function(conn, uuid, files) {
      self$conn = conn
      self$uuid = uuid
      self$files = files
      self$files$Key <- as.character(self$files$Key)
      self$files$Obj <- sapply(self$files$Key,function(x) {
        dir.1 <- dirname(x)
        if (dir.1 == '.') {
          self$.names(x)
        } else {
          sprintf("%s/%s",dirname(x),self$.names(x))
        }
      })
    },
    
    .raw = function(key) {
      self$conn$get(sprintf('job/data/%s/%s',self$uuid,gsub(x = key, pattern = '/',replacement = '::', fixed = T)))
    },
    
    .get_data = function(key) {
      content = self$.raw(key)
      dtbl <- read.table(text=content,sep=',',header=TRUE, check.names = F)
      
      file = basename(key)
      structure = substr(file,1,1)
      data <- switch(structure, 
                     M = {
                       m <- as.matrix(dtbl[,-1])
                       rownames(m) <- dtbl[,1]
                       m
                     },
                     D = dtbl,
                     V = setNames(dtbl[,1],rownames(dtbl)),
                     S = dtbl[1,1]
      )
      return(data)
    },
    
    get_output = function() {
      if (!is.null(self$data)) return(self$data)
      keys <- setNames(self$files$Key,self$files$Key)
      self$data = self$.deserialize(keys)
      return(self$data)
    },
    
    get_object = function(obj) {
      ix <- which(startsWith(self$files$Obj,obj))
      if (length(ix) == 0) return (NULL)
      files <- self$files[ix,,drop=F]
      if (!is.null(self$data)) {
        return(self$data)
      }
      return(self$.deserialize(setNames(files$Key,files$Key)))
    },
    
    .deserialize = function(keys) {
      info <- t(sapply(keys,function(key) {
        v <- strsplit(key,split='/',fixed=T)[[1]] 
        if (length(v) == 1) {
          return(c('.',v))
        } else {
          return(c(v[1],paste0(v[-1],collapse='/')))
        }
      }))
      
      colnames(info) <- c('Dir','File')
      rownames(info) <- names(keys)
      
      dirs <- unique(info[,'Dir'])
      l2 <- lapply(dirs, function(dir.1) {
        
        ix <- which(info[,'Dir'] == dir.1)
        ckeys <- info[ix,'File']
        names(ckeys) <- rownames(info)[ix]
        if (dir.1 == '.') {
          l1 <- lapply(names(ckeys),function(key.1) {
            print(sprintf("Deserializing %s",key.1))
            data.1 <- self$.get_data(key.1)
          })
          names(l1) <- self$.names(names(ckeys))
          return(l1)
        } else {
          l1 <- list(self$.deserialize(
            setNames(info[ix,'File'],rownames(info)[ix])
            ))
          names(l1) <- dir.1
          return(l1)
        }
      })
      do.call(c,l2)
      
    },
    
    .names = function(keys) {
      sapply(keys,function(key.1) {
        key.1 <- basename(key.1)
        gsub('.csv','',paste(strsplit(key.1,'_',T)[[1]][-1],collapse='_'),fixed=T)
      })
    }
    
  )
)
}

#' qes.microsvc.Catalog
#' Catalog Class to browse universes, factors and templates
{
qes.microsvc.Catalog <- R6Class(
  public = list(
    conn = NULL,
    initialize = function(conn) {
      self$conn <- conn
    },
    get_universes = function() {
      fromJSON(self$conn$get('universe'))
    },
    get_factors = function() {
      fromJSON(self$conn$get('factor'))
    },
    get_meta_factors = function() {
      fromJSON(self$conn$get('meta'))
    },
    get_portfolios = function() {
      fromJSON(self$conn$get('portfolio'))
    },
    get_templates = function() {
      fromJSON(self$conn$get('template'))
    }
    
  )
)
}

#' qes.microsvc.Base
#' Base class for Optimizer and Risk Model
{
qes.microsvc.Base <- R6Class(
  "QESBase",
  public = list(
    conn = NULL,
    esvc = NULL, 
    data = NULL,
    req = NULL,
    jobs = NULL,
    version = 1,
    completed = function() {
      self$conn$success_job(self$typeid)
    },
    failed = function() {
      self$conn$failed_job(self$typeid)
    },
    .setConn = function(conn) {
      self$conn = conn
    },
    .setVersion = function(version) {
      self$version = version
    },
    wait = function(max_wait_secs) {
      if (is.null(self$esvc)) {
        stop('No Optimization Associated with the class, either set id or create new optimization request')
      }
      return(self$esvc$wait(max_wait_secs))
    },
    logs = function() {
      return(self$esvc$logs())
    },
    info = function() {
      if (is.null(self$esvc)) {
        stop(paste('Please create a new ',self$endPoint, ' or attach it to existing by doing set_id'))
      }
      return(fromJSON(self$esvc$info()))
    },
    set_id = function(uuid) {
      self$data <- NULL
      self$esvc <- qes.microsvc.EntitySvc$new(self$conn,self$endPoint,uuid,self$version)
    },
    .set_latest = function(k = 1) {
      self$jobs <- self$completed()
      if (nrow(self$jobs) >= k) {
        self$set_id(self$jobs[k,'UUID'])
      }
    },
    status = function(){
      self$info()$status
    },
    submit_new_request = function(req) {
      self$esvc <- NULL
      self$data <- NULL
      
      
      # print(response)
      # print(rawToChar(response$content))
      self$req <- req
      
      endPoint <- self$endPoint
      # print(endPoint)
      print(req)
      if (self$version == 1) {
        response <- self$conn$post(endPoint,req)
      } else if (self$version == 2) {
        response = self$conn$post(paste0('job/submit/',endPoint), req)
      } else {
        stop(sprintf("Version [%s] not supported",self$version))
      }
      self$esvc <- qes.microsvc.EntitySvc$new(self$conn,endPoint,response,self$version)
    },
    set_user_data = function(name, data, format = 'csv', overwrite = TRUE) {
      
      user_data <- qes.microsvc.UserData$new(conn)
      if (!overwrite) {
        if (user_data$exists(name)) {
          stop(sprintf("Data [%s] exists. Set overwrite to TRUE in order to force overwrite"))
        }
      }
      user_data$upload_data(name = name, data = data, format = format)
      
      
      self$req <- c(self$req, list(user_data = list(name = name, format = format)))
      return(self)
    },
    get_output = function() {
      if (is.null(self$esvc)) {
        stop("Either attach an existing UUID or run a new one")
      }
      return(self$esvc$get_job_output())
    },
    get_data = function(file.num = 1) {
      if (!is.null(self$data)) {
        return(self$data)
      }
      if (is.null(self$esvc)) {
        stop('No Service Associated with the class, either set id or create new service request')
      }
      info <- self$info()
      switch(info$status,
             'STARTED' = stop('Service has not completed yet'),
             'ERROR'   = stop(paste(self$esvc$uuid,' failed with message ==> [', info$message ,']')),
             'SUCCESS' = {}
      )
      
      files <- info$files
      #if (length(files) == 1) {
        ix_rdata <- which(endsWith(files,'.RDS'))
        if (length(ix_rdata) > 0) {
          return(self$esvc$get_rdata(files[ix_rdata[file.num]]))
        }
      #}
      stop('Failed to find files??')
    }
    
  )
)
}


#' qes.microsvc.Attribution
{
  qes.microsvc.Attribution <- R6Class(
    "QESAttribution",
    inherit = qes.microsvc.Base,
    public = list(
      typeid = qes.microsvc.type.ATTRIBUTION,
      endPoint = "attribution",
      jobs = NULL,
      initialize = function(conn) {
        self$.setConn(conn)
        #self$.set_latest()
      },
      new_request = function(risk_model, port_data) {
        if (is.null(port_data)) {
          stop('Port Data Missing')
        }
        if (class(port_data) == 'character') {
          req = list(portfolio = port_data, risk_model = risk_model)    
        } else {
          req = list(risk_model = risk_model, 
                     user_data = list( name = port_data$file, format = 'rdata'),
                     weightAttribute = port_data$weightAttribute)    
        }
        self$submit_new_request(req)
      }
    )
  )
}


#' qes.microsvc.RiskModel
#' Risk Model Builder Class
{
qes.microsvc.RiskModel <- R6Class(
  "QESRiskModel",
  inherit = qes.microsvc.Base,
  public = list(
    typeid = qes.microsvc.type.RISKMODEL,
    endPoint = "risk-model",
    jobs = NULL,
    initialize = function(conn) {
      self$.setConn(conn)
      self$.set_latest()
    },
    dates = function() {
      if (is.null(self$esvc)) {
        stop('Please create a new risk model or attach it to existing by doing set_id')
      }
      info1 <- fromJSON(self$esvc$get(""))
      return(info1$dates)
      
    },
    get_data = function(dated) {
      info1 <- fromJSON(self$esvc$get(dated))
      l1 <- lapply(paste0(dated,"/",info1$files),self$esvc$getdf)
      names(l1) <- paste0(dated,"/",info1$files)
      return(l1)
    },
    download_all = function(outdir) {
      dates <- self$dates()
      if (!dir.exists(outdir)) {
        dir.create(outdir)
      }
      for (dt in dates) {
        print(dt)
        d1 <- self$get_data(dt)
        for (n1 in names(d1)) {
          write.csv(d1[[n1]],file=paste0(outdir,'/',basename(n1)),row.names=F)
        }
      }
      return(TRUE)
    },
    new_request = function(universe, template, startDate, endDate, freq) {
      req <- list(
        universe = universe,
        template = template,
        startDate = startDate,
        endDate = endDate,
        freq = freq
      )
      #print(req)
      self$submit_new_request(req)
    }
  )
)
}

#' qes.microsvc.Optimizer
#' Optimizer Class
{
qes.microsvc.Optimizer <- R6Class(
  "QESOptimizer",
  inherit = qes.microsvc.Base,
  public = list(
    req = list(),
    endPoint = "optimization",
    typeid = qes.microsvc.type.OPTIMIZATION,
    initialize = function(conn) {
      self$.setConn(conn)
    },
    set_alpha = function(alpha) {
      self$req <- c(self$req,list(alpha=alpha))
      return(self)
    },
    set_htb_threshold = function(threshold) {
      self$req <- c(self$req,list(htb_threshold=threshold))
      return(self)
    },
    set_benchmark = function(benchmark) {
      self$req <- c(self$req,list(benchmark=benchmark))
      return(self)
    },
    .bound_df = function(f,.min,.max) {
      data.frame(Factor=f,Min=.min,Max=.max)
    },
    set_neutralization_factors = function(neutralization_factors, factor_min_exposure, factor_max_exposure) {
      self$req <- c(self$req, list(neutralization_factors = 
                      self$.bound_df(neutralization_factors,factor_min_exposure,factor_max_exposure)))
      return(self)
    },
    set_neutralization_factors_abs = function(neutralization_factors, factor_max_exposure) {
      self$req <- c(self$req, list(neutralization_factors_abs = 
                      self$.bound_df(neutralization_factors,0,factor_max_exposure)))
      return(self)
    },
    add_neutralization_matrix = function(neutralization_factors, factor_min_exposure, factor_max_exposure, 
                                         grouping_matrix = NULL, benchmark=FALSE){
      self$req <- c(self$req, list(neutralization_matrix = list(bounds = 
             self$.bound_df(neutralization_factors,factor_min_exposure,factor_max_exposure),
             benchmark = benchmark,
             grouping_matrix = grouping_matrix
             )))
      return(self)
      
    },
    set_adv_factor = function(adv_factor) {
      self$req <- c(self$req, list(adv_factor = adv_factor))
    },
    submit = function(template) {
      if (class(template) == 'character') {
        self$req <- c(self$req,template=template)
      } else {
        self$req$template <- template
      }
      self$submit_new_request(self$req)
    }

  )
)
}

{
qes.microsvc.UserData <- R6Class(
  classname = "UserDataSvc",
  public = list(
    conn1 = NULL,
    initialize = function(conn1) {
        self$conn1 <- conn1
    },
    upload_file = function(name, file) {
      return(self$conn1$upload_file(endpoint = sprintf("port/%s",name), 
                             file = file))
    },
    upload_data = function(name, data, format) {
      tempfile <- tempfile(pattern = name)
      if (format == 'rdata') {
        saveRDS(data,file=tempfile)
      } else {
        write.csv(data,file=tempfile, row.names=F)
      }
      print(tempfile)
      return(self$conn1$upload_file(endpoint = "port", 
                                    file = tempfile, name = name))
    },
    remove_data = function(name) {
      return(self$conn1$delete(endpoint = sprintf("port/%s",name)))
    },
    list_data = function(){
      ports <- fromJSON(self$conn1$get("port"))
      
      ports$Uploaded <- as.POSIXct(ports$Uploaded/1e3, origin = as.Date('1969-12-31'))
      ports$ID <- NULL
      return(ports)
    }, 
    exists = function(name) {
      data <- self$list_data()
      if (is.null(data)) return(F)
      if (nrow(data) == 0) return(F)
      return(name %in% data[,'Name'])
    }
    
  )
)
}


#' qes.microsvc.HedgeBuilder
#' 
{
qes.microsvc.HedgeBuilder <- R6Class(
  classname = "HedgeBuilder",
  inherit = qes.microsvc.Base,
  public = list(
    req = list(),
    endPoint = "hedge",
    typeid = qes.microsvc.type.HEDGEBUILDER,
    initialize = function(conn) {
      self$.setConn(conn)
      self$.setVersion(2)
    },
    set_risk_model = function(risk_model) {
      self$req[['risk_model']] <- risk_model
      return(self)
    },
    set_template_name = function(template_name){
      self$req[['template']] <- template_name
      return(self)
    },
    set_notional_value = function(notional_value) {
      self$req[['notional_value']] <- notional_value
      return(self)
    },
    set_hedge_type = function(hedge_type) {
      self$req[['hedge_type']] <- hedge_type
      return(self)
    },
    
    set_factor_to_hedge = function(factor_to_hedge) {
      ## list of one or more SECTOR, STYLE, COUNTRY, SYSTEMATIC, or other fator name, case sensitive
      self$req[['factor_to_hedge']] <- factor_to_hedge
      return(self)
    },
    set_factor_to_neutralize = function(self, factor_to_neutralize) {
      ## list of one or more SECTOR, STYLE, COUNTRY, SYSTEMATIC, or other fator name, case sensitive
      self$req[['factor_to_neutralize']] <- factor_to_neutralize
      return(self)
    },
    set_auto_neutralization = function(auto_neutralization) {
      ## default is True'''
      self$req[['auto_neutralization']] = auto_neutralization
      return(self)
    },
    
    set_max_number_of_stocks = function(max_number_of_stocks) {
      self$req[['max_number_of_stocks']] = max_number_of_stocks
      return(self)
    },
    set_max_neutral_exposure = function(max_neutral_exposure) {
      self$req[['max_neutral_exposure']] = max_neutral_exposure
      return(self)
    },
    
    set_max_gross_exposure = function(max_gross_exposure) {
      self$req[['max_gross_exposure']] = max_gross_exposure
      return(self)
    },

    add_factor_constraint = function(name, type='Factor', constraint_type='Numerical', target='AfterHedge', lb=999, ub=999, include_target_factors=FALSE) {
      self$req[['factor_constraints']][[length(self$req[['factor_constraints']])+1]] = list(name=name, type=type, constraint_type=constraint_type, target=target, lb=lb, ub=ub, include_target_factors=include_target_factors)
    },
    
    set_max_weight = function(max_weight) {
      self$req[['max_weight']] = max_weight
      return(self)
    },
    
    set_min_weight = function(min_weight) {
      self$req[['min_weight']] = min_weight
      return(self)
    },
    
    set_max_adv_usage = function(max_adv_usage) {
      self$req[['max_adv_usage']] = max_adv_usage
      return(self)
    },
    
    set_default_univ = function(default_univ) {
      ### FMP_UNIV or CORE_FMP_UNIV, not case sensitive'''
      self$req[['default_univ']] = default_univ
      return(self)
    },
    
    set_scalars = function(scalars) {
      ### list of float point'''
      self$req[['scalars']] = scalars
      return(self)
    },
    
    set_hedge_ratio = function(hedge_ratio) {
      ### RISK or EXP or VOLADJEXP'''
      self$req[['hedge_ratio']] = hedge_ratio
      return(self)
    },
    
    set_exclude_condition = function(ma_target=FALSE, 
                                     hard_to_borrow=FALSE,
                                     earning_release_names=FALSE,
                                     dual_listings=FALSE,
                                     portfolio_holdings=FALSE,
                                     firmwide_restrictions=FALSE) {
      self$req[['exclusions']] = list(
          ma_target = ma_target, 
          hard_to_borrow = hard_to_borrow,
          earning_release_names =  earning_release_names,
          dual_listings  =  dual_listings,
          portfolio_holdings  =  portfolio_holdings,
          firmwide_restrictions = firmwide_restrictions
      )
      return(self)
      
    },

    get_results = function() {
      return(qes.microsvc.HedgeOutput$new(self$get_output()))
    }
  )
)
}

qes.microsvc.HedgeOutput <- R6Class(
  classname = "HedgeOutput",
  public = list(
    output = NULL,
    initialize = function(output) {
      self$output <- output
    },
    .get = function(key) {
      paths <- strsplit(key,'/',fixed=T)[[1]]
      v <- self$output$get_object(key)
      if (is.null(v)) return(NULL)
      for (p in paths) {
        v <- v[[p]]
      }
      return(v)
    },
    get_baskets = function() {
      return(self$.get('baskets'))
    },
    get_basket = function(basket_name) {
      self$.get(sprintf("baskets/%s",basket_name))
    },
    get_standalone_summary = function() {
      self$.get("summary/standalone_summary")
    },
    get_afterhedge_summary = function() {
      self$.get("summary/afterhedge_summary")
    },
    get_standalone_attribution = function() {
      self$.get("analysis/standalone_attr")
    },
    get_afterhedge_attribution = function() {
      self$.get("analysis/afterhedge_attr")
    }
  )
)
