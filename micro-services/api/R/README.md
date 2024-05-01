# R API for QES Micro Service

### Requirements
- R6   : For object oriented API 
- httr : For working with RESTful API

### Classes 

- qes.microsvc.Conn
  - Connection class that gets initialized using username and password
  - Example:
     conn <- qes.microsvc.Conn$new(username = '<enter username here>', password = '<enter password here'>)

- qes.microsvc.Optimizer
  - Optimizer class. Class allows you do the following
    - Run  new optimization
    - Pull data for previously run optimizations
    - List all optimization (failed/successful)
    - Download Weights and Summary file
  - Example:
     conn <- qes.microsvc.Conn$new(username = '<enter username here>', password = '<enter password here'>)
     optimizer <- qes.microsvc.Optimizer(conn)
     View(optimizer$completed())
    

- qes.microsvc.RiskModel
  - Risk Model class. Class allows  

