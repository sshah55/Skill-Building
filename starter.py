import yfinance as yf
import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math
from secrets import FMP_API_TOKEN

stocks = pd.read_csv('sp_500_stocks.csv')