library(igraph)

# Data Query Function
getData<-function(factors){
  wq.getdata(wq.newRequest()$testMode()$runFor(universeName)$from(startDate)$to(endDate)$at(freq)$attr(.jarray(factors)))
}

wq.plotplan<-function(factor){
                g<-graph.data.frame(wq.plan.nodes(factor,'COMPUSTAT'))
                V(g)$label.cex=0.75
                plot(g)
}


# Sector Mask

gics <- read.csv(file = "/mnt/ebs1/data/config/gics_map.csv", header = TRUE)[1:11,]

gicsMap<-gics[,1]
names(gicsMap)<-as.character(gics[,2])

getSectorMask <- function(sectors_names, data){
  
  if(!'GSUBIND' %in% names(data)) {
    stop('GSUBIND not in data')
  }

  sectors_code <- as.character(gicsMap[sectors_names])
  sector_mask <- apply(data[['GSUBIND']],2,function(x){return(substr(x,1,nchar(sectors_code[1])) %in% sectors_code)})
  dimnames(sector_mask)<- dimnames(data[["GSUBIND"]])
  return (sector_mask)
}

getMeltTable <- function(table, nameMatrix){
  namesMap <- nameMatrix[,ncol(nameMatrix)]
  rownames(table) <- namesMap[rownames(table)]
  table_df <- data.frame(t(table))
  table_df$date <- as.Date(rownames(table_df))
  meltTable <- melt(table_df, value.name = 'rate', id.vars = 'date', variable.name = 'CompanyName')
  return(meltTable)
}


## Random Forest Utility Functions


library(randomForest)


neutralize<-function(c_factor,c_date,uniform=TRUE){
  cm_data<-c(c_factor[,c_date])
  tempData<-rep(NA,length(cm_data))
  mask<-is.finite(cm_data)   
  x<-cm_data[mask]
  if(sum(is.finite(x)!=0)){
    diffFactor<-sort(unique(floor(x[is.finite(x)]*10000)/10000))
    map<-lapply(diffFactor,function(y){which(abs(y-x)<0.0001)})
    equalF<-which(sapply(map,function(y){return(length(y)>1)}))
    validX<-x[is.finite(x)]
    idx<-sort.int(validX,index.return=TRUE)$ix
    valueIdx<-rep(NA,length(x))
    if(uniform)
      valueIdx[is.finite(x)][idx]<-(1:sum(is.finite(x)))/(sum(is.finite(x)))
    else
      valueIdx[is.finite(x)][idx]<-qnorm((1:sum(is.finite(x)))/(1+sum(is.finite(x))))
    if(length(equalF)>0){
      for(k in equalF){
        valueIdx[map[[k]]]<-median(valueIdx[map[[k]]],na.rm=T)
      }
    }
    tempData[mask]<-valueIdx
  }
  return(tempData)
}



#' Runs Random Forest by using forward returns as the label
#'
#' @param FMRTN1M 
#' @param factor_data 
#' @param allTraining 
#' @param thresh 
#' @param m_nodes 
#' @param binary 
#' @param minCoverage 
#'
#' @return
#' @export
#'
#' @examples
learnRF<-function(FMRTN1M,factor_data,allTraining,thresh=0.5,m_nodes=10,binary=FALSE,minCoverage=0.6){
  
  getTrainingData<-function(allTraining,FMRTN1M){
    posFactors<-c()
    negFactors<-c()
    for(jj in allTraining){
      selectedReturns<-neutralize(FMRTN1M,jj)
      selectedData<-sapply(factor_data,function(y){return(neutralize(y,jj))})
      availableReturns<-selectedReturns[is.finite(selectedReturns)]
      availableData<-selectedData[is.finite(selectedReturns),]
      threshold<-quantile(availableReturns,prob=c(thresh,1-thresh),na.rm=T)
      neg<-availableReturns<threshold[1]
      pos<-availableReturns>threshold[2]
      posFactors<-rbind(posFactors,availableData[pos,])
      negFactors<-rbind(negFactors,availableData[neg,])
    }
    return(list(posFactors=posFactors,negFactors=negFactors))
  }
  
  
  trainingData<-getTrainingData(allTraining,FMRTN1M)
  posFactors<-trainingData[['posFactors']]
  negFactors<-trainingData[['negFactors']]
  AllFactors<-rbind(posFactors,negFactors)
  posNum<-nrow(posFactors)
  negNum<-nrow(negFactors)
  
  mask<-which(colnames(is.finite(AllFactors))>nrow(AllFactors)*minCoverage)
  AllFactors<-AllFactors[,mask]
  AllFactors[!is.finite(AllFactors)]<-0.5
  label<-c(rep(1,posNum),rep(-1,negNum))
  if(binary)
    label<-factor(label)
  if(m_nodes>0)
    model<-randomForest(AllFactors,y=label,importance=T,maxnodes=m_nodes)
  else
    model<-randomForest(AllFactors,y=label,importance=T)
  return(list(model=model,mask=mask))
}

getScoreRF<-function(factor_data,current_Date,classifier){
  curData<-sapply(factor_data,function(y){
    return(neutralize(y,current_Date))
  })
  allNA<-rowSums(is.finite(curData))==0
  model<-classifier[['model']]
  mask<-classifier[['mask']]
  AllFactors<-curData[,mask]
  AllFactors[!is.finite(AllFactors)]<-0.5
  finalScore<-predict(model,AllFactors)
  names(finalScore)<-rownames(factor_data[[1]])
  finalScore[allNA]<-NA
  return(finalScore)
}

linearCoeffs<-function(FMRTN1M,factor_data,allTraining,minCoverage=0.6,regMethod='ols',stepwise=TRUE){
  getTrainingData<-function(allTraining,FMRTN1M){
    frtn<-c()
    factors<-c()
    for(jj in allTraining){
      selectedReturns<-neutralize(FMRTN1M,jj,uniform=FALSE)
      selectedData<-sapply(factor_data,function(y){return(neutralize(y,jj,uniform=FALSE))})
      availableReturns<-selectedReturns[is.finite(selectedReturns)]
      availableData<-selectedData[is.finite(selectedReturns),]
      frtn<-c(frtn,availableReturns)
      factors<-rbind(factors,availableData)
    }
    return(list(frtn=frtn,factors=factors))
  }
  trainingData<-getTrainingData(allTraining,FMRTN1M)
  frtn<-trainingData[['frtn']]
  AllFactors<-trainingData[['factors']]
  
  mask<-which(colnames(is.finite(AllFactors))>nrow(AllFactors)*minCoverage)
  AllFactors<-AllFactors[,mask]
  AllFactors[!is.finite(AllFactors)]<-0
  frtn[!is.finite(frtn)]<-0
  inputdata<-cbind(frtn,AllFactors)
  eqn<-paste('frtn',paste(colnames(AllFactors),collapse ='+'),sep='~')
  eqn<-as.formula(eqn)
  dataFrame<-as.data.frame(inputdata)
  if(regMethod=='ols')
    reg<-lm(eqn,data=dataFrame)
  else if(regMethod=='gls')
    reg<-gls(eqn,data=dataFrame)
  else if(regMethod=='rlm')
    reg<-rlm(eqn,data=dataFrame)
  else if(regMethod=='lad')
    reg<-lad(eqn,data=dataFrame)
  
  if(stepwise)
    reg<-stepAIC(reg,trace=FALSE)
  return(summary(reg)[[4]][2:nrow(summary(reg)[[4]]),1])
}

getScoreLinear<-function(factor_data,current_Date,coeffs){
  curData<-sapply(factor_data,function(y){
    return(neutralize(y,current_Date,uniform=FALSE))
  })
  allNA<-rowSums(is.finite(curData))==0
  curData[!is.finite(curData)]<-0
  finalScore<-colSums(t(curData[,names(coeffs)])*coeffs)
  names(finalScore)<-rownames(factor_data[[1]])
  finalScore[allNA]<-NA
  return(finalScore)
}

