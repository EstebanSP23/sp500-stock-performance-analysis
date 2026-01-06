# Data Dictionary

## Raw Data (Wide Format)
- Date: Trading date
- [Ticker]_Open: Opening price for ticker
- [Ticker]_High: Daily high
- [Ticker]_Low: Daily low
- [Ticker]_Close: Closing price
- [Ticker]_Volume: Trading volume

## Dimension Table: Stocks & Sectors (sp500_sectors.csv)
| Column       | Description                          | Example              |
|--------------|--------------------------------------|----------------------|
| Ticker      | Stock symbol                         | AAPL                |
| Sector      | GICS Sector                          | Information Technology |
| Industry    | GICS Sub-Industry                    | Technology Hardware |
| Company Name| Full company name                    | Apple Inc.          |

(To be expanded post-transformation)
