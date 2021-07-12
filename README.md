# Real-Time Crypto Tracker

## Intoduction
The purpose of this project is to build a real-time predictive analysis dashboard for bitcoin prices.<br/>
This project was the capstone project for [SDA](https://sda.edu.sa/)'s Data Science Bootcamp in cooporation with [CodingDojo](https://www.codingdojo.com/).

Team members:
- [Mamdouh Alomari](https://github.com/MamdouhAlomari)
- [Rawan Alsaedi](https://github.com/RawanAlsaedi)
- [Ruba Yousuf](https://github.com/RubaYousuf)
- [Tahani Albarakati](https://github.com/Tahani-Albarakati)

## Data
The Data used in this project were fetched from 3 sources:
- [Coin Market Cap Website](https://coinmarketcap.com/currencies/bitcoin/)
- [Coin Desk API](https://api.coindesk.com/v1/bpi/currentprice.json)
- [Twitter API](https://developer.twitter.com/en/docs/twitter-api)

## Project Description
In this project we utilized different technologies to come up with a real-time dashboard for bitcoin prices.<br/>
The project went through 4 stages:
- **Stage 1**: Fetch the bitcoin prices from Coin Market Cap web page & Coin Desk API then insert  it into the database.
- **Stage 2**: Fetch tweets from Twitter API, process it through Kafka, then finally insert the tweets as (negative , positive )into the database. 
- **Stage 3**: Read the data from SQL and train the model to predict the price.
- **Stage 4**: Build the dashboard as a web page using React to make it accessible for end users.

![arcitecture!](/images/architecture.gif)


## Visualization
Let's take a look at the price of Bitcoin over the course of a whole day.<br/>
![bitcoin_price!](/images/BTC_Price_11-07-2021.png)

In order for us to capture the uncertainty of bitcoin prices we had to come up with a creative solution!<br/>

## Model
In the modeling process we decided to use 4 different models:
- [ARIMA](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average), which can help us capture seasonality & trends.
- [VARMAX](https://www.analyticsvidhya.com/blog/2018/09/multivariate-time-series-guide-forecasting-modeling-python-codes/), which can help us find relation between the Bitcon price & Tweets
- [SES](https://machinelearningmastery.com/exponential-smoothing-for-time-series-forecasting-in-python/#:~:text=Single%20Exponential%20Smoothing%2C%20SES%20for,smoothing%20factor%20or%20smoothing%20coefficient.), which is the simplest approcach to Time Series Forecasting.
- [Random Forest Regressor](https://en.wikipedia.org/wiki/Random_forest). By using the predictions from the other 3 models, we can train a random forest to help us get better accuracy.

This is an over view of the models performace:<br/>
![all-models!](/images/All_models.png)

## Prpject Structure
`Models` Folder have Jupyter Notebooks for all different models used in the modeling stage.<br/>
`client-react` is the react web application.<br/>
`server` is a Flask back-end for the react web application.<br/>
