from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
from factors_common import all_factors, backtest, generate_excel
from gics_util import build_sector_universe

def prev_weekday(adate=date.today()):
    """

    """
    adate -= timedelta(days=1)
    while adate.weekday() > 4:  # Mon-Fri are 0-4
        adate -= timedelta(days=1)
    return adate


SOFTWARE_CORE_FACTOR = ['EPSYLD_GRO_DIVY_BB_EV_RND', 'CFO_TEV', 'SALE_EV_FY1',
                        'GP_TEQ', 'CFRNOA', 'GR_INTR_SPS',
                        'G1_G_91_QQ',
                        'E2_L_91_NET_SCORE',
                        'E2_G_91_YY_MARKET_SHARE', 'E2_G_91_2YY_MARKET_SHARE', 'E2_G_91_2QQ_MARKET_SHARE',
                        'G2_L_364_OV_CURRENT', 'G2_L_364_RO_CURRENT', 'GTWO_G_91_2QQ_APV', 'GTWO_L_364_SOULTR',
                        'ES_SALE_FY1_R3M', 'ES_EBIT_FY1_R3M', 'MA_30_75']

NEUT_FACTOR_PREFIX = 'Neut_'
PERCENTILE_FACTOR_PREFIX = 'PERCENTILE_'

VOLWEIGHTED_FACTOR_NAME = 'VolWeightedScore'
EQUIWEIGHTED_FACTOR_NAME = 'EquiWeightedScore'
SPECWEIGHTED_FACTOR_NAME = 'SpecifiedWeightedScore'

RUSSELL_3K = 'USC_2668795'


class StockScreener:
    """
        Software Screener Class. Provides convienient way to
    """

    def __init__(self, wq,
                 starting_univ=RUSSELL_3K,
                 end_date=prev_weekday(),
                 months_to_go_back=84,  # Five Years
                 min_mktcap=1e9,
                 sector_neutralize=True,
                 do_optimization=True,
                 starting_gics=45,
                 exclude_gics=[4520, 4530, 451020]
                 ):

        """
            Contructor for Software Screener.

            Parameters
            ----------
            wq : lquantPy.LQuant.LQuant
                LQuant Gateway Object
            starting_univ : str
                Starting Universe Id for building the software universe
            end_date: datetime.date
                End date of the analysis. Defaults to last weekday
            months_to_go_back: int
                Number of months to go back. Defaults to 84 months (~7 years)
            min_mktcap: float
                Minimum market for building the universe. Defaults to 1 billion
            sector_neutralize: boolean
                Boolean flag to neutralize the factor using the sector flag.
            do_optimization: boolean
                Boolean flag to enable/disable optimization
            starting_gics: int
                GICS to filter the broader universe on
            exclude_gics: list(str)
                List of GICS to be excluded from the software universe
        """
        self.wq = wq
        self.starting_univ = starting_univ
        self.start_date = end_date - relativedelta(months=months_to_go_back)
        self.end_date = end_date
        self.min_mktcap = min_mktcap
        self.sector_neutralize = sector_neutralize
        self.do_optimization = do_optimization
        self.starting_gics = starting_gics
        self.exclude_gics = exclude_gics
        self.custom_univ = 'Custom_Universe'
        self.ref_factors = ['TICKER', 'COMPANYNAME']
        self.analytics = None
        self.factors = []
        self.data = None
        self.req = None
        self.freq = '1m'
        self.analytics = None
        self.excl_tickers = []
        self.opt_neut_factors = []
        self.volWeights = None
        self.bins = 5
        self.backtest_results = None
        self.base_score_factor = None
        self.opt_factors = []
        self._OPT_WEIGHT_ = 'OPT_WEIGHT'
        self.__source__()

    def get_start_date(self):
        """
            Returns start date in string format

            Returns
            -------
            String representation of start date

        """
        return self.start_date.strftime('%Y-%m-%d')

    def get_end_date(self):
        """
            Returns end date in string format

            Returns
            -------
            String representation of end date

        """
        return self.end_date.strftime('%Y-%m-%d')

    def build_universe(self):
        """
            Builds the sector universe.

            Returns
            -------
            Itself
        """
        univ_id = build_sector_universe(
            wq=self.wq, id=self.custom_univ,
            starting_univ=self.starting_univ,
            starting_gics=self.starting_gics,
            start_date=self.get_start_date(),
            min_mktcap=self.min_mktcap,
            end_date=self.get_end_date(),
            freq=self.freq,
            exclude_gics=self.exclude_gics)

        if univ_id is None:
            raise Exception("Internal Error occurred while trying to build universe. See Log File")

        return self

    def __source__(self):
        self.wq.env().run('library(lqrisk)')
        return self

    def reset(self):
        self.data = None
        self.req = None

    def get_data(self, factors=SOFTWARE_CORE_FACTOR, opt_neut_factors=['SALE_EV_FY1']):
        """
            Fetches data from the warehouse to do the analysis

            Parameters
            ----------
            factors : list(str)
                List of factors to build the screener on
            opt_neut_factors: list(string)
                List of factors to use for neutralizing the weights in optimization. Only used when
                optimization is set to True
        """

        if self.data:
            raise Exception("Get data can be called only once. Do you intend to create a new object?")

        self.factors = factors
        self.opt_neut_factors = opt_neut_factors

        req = self.wq.new_request()
        req = req.runFor(self.custom_univ)
        req = req.start(self.get_start_date())
        req = req.to(self.get_end_date())
        req = req.at(self.freq)
        req = req.attr(*tuple(factors))
        req = req.a('QES_GSECTOR')
        req = req.a('COMPANYNAME')
        req = req.a('TICKER')

        if self.do_optimization:
            req = req.a('ADV_1M_USD')
            for f1 in opt_neut_factors:
                req = req.a(f1)

        req = req.addForwardReturn()  # Add forward return
        req = req.addInFlag()  # Add in universe flag

        self.data = self.wq.get_data(req)
        self.req = req
        self.analytics = self.wq.multi_factor_analysis(self.data, req.inFlag())

        if self.excl_tickers:
            self.analytics.exclude_tickers(self.excl_tickers)
        return self

    def exclude_tickers(self, tickers=['MSTR', 'RIOT', 'TTD', 'ENV']):
        """
            Exclude tickers from the universe

            Parameters
            ----------
            ticker : list(str)
                List of tickers to exclude from the univer
        """
        self.excl_tickers = tickers
        if self.analytics:
            self.analytics.exclude_tickers(tickers)
        return self

    def mask(self):
        """
            Masks factors. Only factor values that are in the universe is kept.

        """

        self.analytics.mask_factors(self.factors)
        self.analytics.mask_factors(self.opt_neut_factors)
        return self

    def add_neutralize_scores(self):
        """
            Neutralizes scores to make them ready for multi-factor z-score

        """

        if not self.sector_neutralize:
            return False

        # Neutralize all factors
        for ff in self.factors:
            self.analytics.basic_neutralize_factor(NEUT_FACTOR_PREFIX + ff, ff, 'z_normal', 'QES_GSECTOR')

        return self

    def add_percentile_scores(self):
        """
            Add percentile scores to the data set

        """

        for ff in self.factors:
            self.analytics.basic_neutralize_factor(PERCENTILE_FACTOR_PREFIX + ff, ff, 'percentile', 'QES_GSECTOR')

        return self

    def get_factor_coverage(self):
        """
            Returns factor coverage matrix

            Returns
            -------
            Pandas data frame with factor coverage
        """

        return pd.DataFrame({factor: self.data[factor].as_matrix().count() for factor in self.factors})

    def get_factor_coverage_ratio(self):
        """
            Returns factor coverage ratio

            Returns
            -------
            Pandas data frame with factor coverage ratio
        """
        univ_count = self.get_universe_count()
        return pd.DataFrame({factor: self.data[factor].as_matrix().count() / univ_count for factor in factors})

    def get_universe_count(self):
        """
            Returns factor coverage matrix

            Returns
            -------
            Array containing the time series of the count of securities in the universe
        """
        return self.data[self.request.inFlag()].as_matrix().sum()

    def composite_factors(self):
        """
            Return list of composite factors
        """

        return self.common([VOLWEIGHTED_FACTOR_NAME, EQUIWEIGHTED_FACTOR_NAME, SPECWEIGHTED_FACTOR_NAME])

    def neut_factors(self):
        """
            Return list of neutralized
        """
        return self.common([NEUT_FACTOR_PREFIX + f1 for f1 in self.factors])

    def get_active_factors(self):
        """
            Returns list of factors for which backtest will be run

            Returns
            -------
            Array containing the list of factors
        """
        all_active_factors = list(self.factors)
        if self.sector_neutralize:
            # Capture all factors in one list prior to
            all_active_factors += self.neut_factors()

        return all_active_factors + self.composite_factors()

    def get_factors(self):
        """
            Returns list of factors that will be used in multi-factor scoring

            Returns
            -------
            Array containing the list of factors
        """
        if self.sector_neutralize:
            return self.neut_factors()
        else:
            return self.factors

    def add_vol_weighted_score(self, period=12):
        """
            Adds vol weighted score to the data set


            Parameters
            -------
            period: int
                Period for computing the factor volatility

            Returns
            -------
            Itself
        """
        factors = self.get_factors()
        volWeights = self.analytics.get_vol_weights('volWeights', factors, period=period)
        self.volWeights = volWeights
        self.analytics.multi_factor_score(VOLWEIGHTED_FACTOR_NAME, factors, 'volWeights')
        return self

    def add_equal_weighted_score(self):
        """
            Adds equi-weighted score to the data set


            Returns
            -------
            Itself
        """

        factors = self.get_factors()
        weights = [1 / len(factors) for f in factors]
        self.analytics.multi_factor_score(EQUIWEIGHTED_FACTOR_NAME, factors, weights)
        return self

    def add_weighted_score(self, weights):
        """
            Adds specified-weighted score to the data set

            Parameters
            -------
            weights: dictionary(str->float)
                Weights for the factors

            Returns
            -------
            Itself
        """
        factor_weights = [weights[f] for f in self.factors]
        self.analytics.multi_factor_score(SPECWEIGHTED_FACTOR_NAME, self.factors, factor_weights)
        return self

    def contains(self, factor):
        """
            Check if a factor is in the data object

            Parameters
            -------
            factor: str
                Name of the factor
        """
        return factor in self.data.names()

    def backtest_contains(self, factor):
        """
            Check if a factor is in the backtest object

            Parameters
            -------
            factor: str
                Name of the factor
        """
        if not self.backtest_results:
            return False

        return factor in self.backtest_results.factors

    def common(self, factors):
        """
            Returns common factors between in the data object

            Parameters
            -------
            factors: list(str)
                List of factors to intersect with
        """
        return list(set(factors) & set(self.data.names()))

    def backtest_opt_weight(self, name, bins = 0):
        """
            Runs the backtest for optimized weights
        """
        if not self.backtest_results:
            return False

        if not self.contains(name):
            return False

        if self.backtest_contains(name):
            return False

        breq = self.wq.new_backtest_request()

        if bins == 0: 
            breq.forFactor(self.base_score_factor) 
            breq.weightFactor(name)
        else: 
            breq.forFactor(name) 
            breq.withBins(bins)

        opt_performance = self.wq.basic_backtest(data=self.data, req=breq)
        self.backtest_results.backtest_results = self.backtest_results.backtest_results + [opt_performance]
        self.backtest_results.factors = self.backtest_results.factors + [name]
        return True

    def add_optimized_weights(self, 
			      name,
			      base_score_factor=EQUIWEIGHTED_FACTOR_NAME,
                              max_weight=0.1,
                              notional=5e7,
                              turnover_penalty=0.005,
                              max_adv=0.05,
                              maximum_htb_score=1.0,
                              minimum_adv_for_inclusion=1e6,
			      bins = 0
                              ):

        """
            Adds optimized weights to the data sets

            Parameters
            -------
            name: str
                Name of the basket 
            base_score_factor: str
                Name of the base weights to use for optimization
            max_weight: float
                Maximum weight to allow for each security
            notional: float
                Notional value of the portfolio. Defaults to 50 million
            turnover_penalty: float
                Turnover penalty applied and added to the objective function. Default is 0.005
            max_adv: float
                Maximum ADV for the position. Defaults to 5%
            maximum_htb_score: int
                Maximum Hard to Borrow Score to keep in the portfolio. Defaults to 1, so any
                security with score > 1 is excluded
            minimum_adv_for_inclusion: float
                Minimum ADV value for a stock to be included in the portflio. Defaults to 1 million.
            bins: int 
               	Number of bins for building the tracking long/short basket. Defaults to 0 means the signal weighted 
	


            Returns
            -------
            Itself. Add OPT_WEIGHT to the data object
        """

        if not self.do_optimization:
            raise Exception("Optimization can be only run if do_otpimization is set")

        if self.contains(name):
            raise Exception("Optimization already run for [{}]. Please pick another name".format(name))

        self.base_score_factor = base_score_factor
        portfolio_build_request = self.wq.new_portfolio_request(notional)
        portfolio_build_request = portfolio_build_request.factorWeight(base_score_factor, bins)
        portfolio_build_request = portfolio_build_request.maxWeight(max_weight)
        portfolio_build_request = portfolio_build_request.filterHardToBorrow(maximum_htb_score)
        portfolio_build_request = portfolio_build_request.turnoverPenalty(turnover_penalty)

        if len(self.opt_neut_factors) > 0: 
            portfolio_build_request = portfolio_build_request.neutFactors(self.opt_neut_factors)

        portfolio_build_request.neutSector(['QES_GSECTOR'])
        portfolio_build_request = portfolio_build_request.minAdv(minimum_adv_for_inclusion)
        portfolio_build_request = portfolio_build_request.maxADV(max_adv);

        self.wq.build_portfolio(data=self.data, req=portfolio_build_request)
        self.wq.env().run("mode({}[['IN']])<-'numeric'".format(self.data.name()))
        self.wq.env().run("{}[['{}']] <- {}[['{}']]".format(self.data.name(),name,self.data.name(),self._OPT_WEIGHT_))
        self.wq.env().run("{}[['{}']] <- NULL".format(self.data.name(),self._OPT_WEIGHT_))
        self.opt_factors = self.opt_factors + [ name ]

        self.backtest_opt_weight(name)
        return self



    def get_correlation_chart(self):
        """
            Returns correlation chart for all factors

            Returns
            -------
            Itself
        """
        if self.backtest_results is None:
            raise Exception("Correlation can be only called after backtest")
        return self.backtest_results.plot_return_correlation(self.get_factors() + self.composite_factors())

    def run_backtest(self, bins=5):
        """
            Runs backtest for all active factors.

            Parameters
            -------
            bins: int
                Number of buckets to build the long/short portfolio

            Returns
            -------
            Itself
        """
        self.bins = bins
        self.backtest_results = self.analytics.backtest(factors=self.get_active_factors(),
                                                        bins=bins, align=False)
        for n1 in self.opt_factors: 
            self.backtest_opt_weight(n1)
	        
        return self

    def export_to_csv(self, filename='Multi-Factor-Custom_Universe-Monthly.csv'):
        """
            Exports all data to a CSV file

            Parameters
            -------
            filename: str
                Filename to which CSV to be written

            Returns
            -------
            None
        """
        df = self.data.as_large_data_frame()
        ### Converting all data to pandas
        return df.to_csv('Multi-Factor-Custom_Universe-Monthly.csv', index=False)

    def export_returns_to_csv(self, postfix='Monthly Quintile Returns.csv'):

        if not self.backtest_results:
            raise Exception("Export can be only called after backtest")

        backtest_results = self.backtest_results
        composite_factors = self.composite_factors()

        for i in range(0, len(backtest_results.factors)):
            res = backtest_results.get(i).wealth().as_matrix().transpose()
            factor_name = backtest_results.factors[i]
            if factor_name in composite_factors:
                res.to_csv(factor_name + ' ' + postfix)
            else:
                res.to_csv('output/' + factor_name + ' ' + postfix)
        return True

    def export_returns_to_excel(self, excel_file_name='Custom_Universe_Monthly_All_Factors3'):
        if not self.backtest_results:
            raise Exception("Export can be only called after backtest")

        # Arg1: Name of the Universe
        # Arg2: Number of baskets in the backtest
        self.backtest_results.generate_excel(excel_file_name, self.bins)
        return True
