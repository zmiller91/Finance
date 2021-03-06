__author__ = 'zmiller'
from Run import Runable
import PortfolioCollection

Run = Runable()
Run.run()


oPortfolioCollection = PortfolioCollection()
aPortfolios = oPortfolioCollection.iteritems()
for oPortfolio in aPortfolios:
    oAlgorithm = oPortfolio['algorithm']
    oAlgorithm.feedData()