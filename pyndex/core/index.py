import pyndex.util._decorator as dec
import pyndex.core.algorithm as alg
import wrds
import pandas as pd

class Index:

    @staticmethod
    @dec.typeassert(wrds = wrds.sql.Connection,
                    year = int, index = str)
    @dec.supported(index = ["1000","2000","3000"])
    def from_wrds(wrds, year, index, verbose = False):
        if verbose :
            print("Downloading Data ...")
        metadata, stock = alg.download(wrds,year)
        if verbose :
            print("Building Index ...")
        weights_table = alg.build(stock, year, index,
                        metadata)

        return weights_table

    @staticmethod
    @dec.typeassert(year = int)
    def get_calendar(year):
        calendar = alg.get_calendar(year)
        calendar_table = pd.DataFrame(
                        calendar.items(),columns=["event","date"])
        return calendar_table
                
