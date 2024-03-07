from math import log10,trunc

def get_sector_level(starting_gics):
    return 1 + trunc(log10(starting_gics) / 2)


def get_sector_id(level):
    if level == 1:
        return 'GSECTOR'
    if level == 2:
        return 'GGROUP'
    if level == 3:
        return 'GIND'
    if level == 4:
        return 'GSUBIND'


def get_sector_ex_cond(gics):
    N = get_sector_level(gics)
    return get_sector_id(N) + '!=' + str(gics)


def get_sector_universe_id(starting_univ, starting_gics):
    if type(starting_univ) == str:
        starting_univ = [starting_univ]
        
    if type(starting_gics) == list:
        return '__OR__'.join([get_sector_universe_id(starting_univ,gic) for gic in starting_gics])
    else:
        N = 1 + get_sector_level(starting_gics)
        postfix = ''.join(['_' for i in range(1, N)]) + str(starting_gics)
        return '__OR__'.join([(univ +  postfix) for univ in starting_univ])

def get_universe_id(starting_univ):
    if type(starting_univ) == str:
        return starting_univ
    return '__OR__'.join(starting_univ)
    

def build_sector_universe(wq, id, starting_univ, starting_gics, start_date,
                          end_date, freq, exclude_gics = [], min_mktcap=0, max_mktcap = -1, 
                          min_adv = -1, exclude_ma = False, marketcap_factor = 'MKTCAP*FXRATE_USD'):
    """

    :param wq: Handle to wq universe
    :param id: Id to the custom universe
    :param starting_univ: Starting universe id (e.g., US_1)
    :param starting_gics: Starting GICS (Any level). For example 25 Can be set to None
    :param start_date: Start Date YYYY-mm-dd
    :param end_date: End Date YYYY-mm-dd
    :param freq: Frequency (e.g., 1m, 1me)
    :param exclude_gics: Excluding GICS, e.g., [2530]
    :param min_mktcap: Minimum market cap
    :return:
    """
    if starting_gics is None:
        univ_id = get_universe_id(starting_univ)
    else:
        univ_id = get_sector_universe_id(starting_univ, starting_gics)

    univ_request = wq.new_univ_request(id)
    univ_request = univ_request.runFor(univ_id).start(start_date).to(end_date).at(freq)
    
    if max_mktcap > 0:
        cond = '({}>{}&&{}<{})'.format(marketcap_factor,min_mktcap,marketcap_factor,max_mktcap)
    else:
        cond = '({}>{})'.format(marketcap_factor,min_mktcap)
        
    if min_adv > 0:
        cond = cond + '&&(ADV_1M_USD>' + str(min_adv) + ')'
        
        
    if len(exclude_gics) > 0:
        cond = cond + '&&(' + ')&&('.join([get_sector_ex_cond(gics) for gics in exclude_gics]) + ')'
        
    
    if exclude_ma:
        cond = cond + '&&(nvl(MA_INDICATOR,0)!=80)'
    
    univ_request.condition(cond)
    return wq.build_univ(univ_request)
