# Fetching and Analyzing Top 50 Live Cryptocurrency Data

This project fetches live cryptocurrency data for the top 50 cryptocurrencies, analyzes it, and updates an Excel sheet with the latest prices. The data is continuously updated every 5 minutes using an Azure Function.

## Overview

The project performs the following tasks:
1. **Fetch Live Data**: Retrieves the top 50 cryptocurrencies by market capitalization from the CoinGecko API.
2. **Data Analysis**: Analyzes the fetched data to identify the top 5 cryptocurrencies by market cap, calculate the average price of the top 50 cryptocurrencies, and determine the highest and lowest 24-hour percentage price changes.
3. **Generate Report**: Creates a text report summarizing the analysis.
4. **Update SheetDB**: Updates a SheetDB database with the latest cryptocurrency data.

## Setup Instructions


### Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rohitd2103/Fetching-and-Analyzing-Top-50-Live-Cryptocurrency-Data.git
   cd Fetching-and-Analyzing-Top-50-Live-Cryptocurrency-Data
