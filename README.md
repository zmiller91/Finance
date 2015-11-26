# Finance

The purpose of this application is to provide plug and play functionality for testing algorithmic trading strategies in a real time environment. 

This application is a daemon that creates a real time trading environment.  It collects daily and real time data from a Yahoo Api; when given real time data this daemon will feed the data to any algorithms living in the Algorithms folder.  These algorithms are user defined and inherit from a Portfolio class; the portfolio class contains methods for buying, selling, and managing open positions.  The Portfolio class also provides methods for inserting an algorithm's performance data.
