# Create compact functions to backtest and export to pdf
def backtest(wq, data1, factor, in_flag, bins, hard_to_borrow_filter = -1):
    print(factor)
    backtest_request = wq.new_backtest_request()
    backtest_request = backtest_request.forFactor(factor)
    backtest_request = backtest_request.withBins(bins)

    # The IN Flag is 
    backtest_request.withInFlag(in_flag)
    backtest_request.filterHardToBorrow(hard_to_borrow_filter)
        
    res = wq.basic_backtest(data1,backtest_request)
    return res
    
def one_hot_encoding(wq, data1, inflag, classificationFactor, prefix):
    env = wq.env()
    env.run('source("/mnt/ebs1/data/common/R/util.R")')
    env.run(".r1 <- ltool.onehotencoding('{}','{}','{}','{}')".format(data1.name(),inflag,classificationFactor,prefix))
    return env.get("as.numeric(.r1)")

def filter_factor(x, min_count = 12):
    if x is None:
        return True
    ret = x.basket_returns()
    if ret is None:
        return True
    return x.basket_returns().as_matrix().count(axis='columns')['LS'] < min_count
    
    return x.basket_returns().as_matrix().count(axis='columns')['LS'] < min_count

def generate_excel(wq, univ_name, all_factors,all_res):
    
    res_names = [None if filter_factor(x) else x.res.name()  for x in all_res]
    indx = [i for i, n in enumerate(res_names) if n is not None]
    
    indx_rem = [i for i, n in enumerate(res_names) if n is None]
    rem_names = [all_factors[i] for i in indx_rem]
    print('Names Removed')
    print(rem_names)

    res_names_2 = [res_names[i] for i in indx]
    all_res_2 = [all_res[i] for i in indx]
    all_factors_2 = [all_factors[i] for i in indx]
    fnms = 'c("' + '","'.join(all_factors_2) + '")'
    
    wq.env().run("all.res <- list(" + ",".join([x.res.name() for x in all_res_2]) + ")")
    wq.env().run('write.summary.statsALL(list_BacktestBasic = all.res,universeName = "' + univ_name + '",factorName='+ fnms + ',baskets=5)')
    

import pandas as pd
import os
if os.path.isfile('/mnt/ebs1/config/all_factors.csv'):
    all_factors = list(set(pd.read_csv('/mnt/ebs1/config/all_factors.csv').iloc[:,0].to_list()))
else:
    all_factors = []

if os.path.isfile('/mnt/ebs1/config/all_insider_factors.csv'):
    all_factors_insider = list(set(pd.read_csv('/mnt/ebs1/config/all_insider_factors.csv').iloc[:,0].to_list()))
else:
    all_factors_insider = []

