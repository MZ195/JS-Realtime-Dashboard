# REAL-TIME CRYPTO TRACKER

## INTRODUCTION
The purpose of this project is to build a real-time predictive analysis dashboard for bitcoi prices.<br/>
The project was the capstone project for [SDA](https://sda.edu.sa/)'s Data Science Bootcamp in cooporation with [CodingDojo](https://www.codingdojo.com/).

The team members:
- [Mamdouh Alomari](https://github.com/MamdouhAlomari)
- [Rawan Alsaedi](https://github.com/RawanAlsaedi)
- [Ruba Yousuf](https://github.com/RubaYousuf)
- [Tahani Albarakati](https://github.com/Tahani-Albarakati)

## PROJECT DESCRIPTION
In this project we utilized different technologies to come up with a real-time dashboard for bitcoin prices.<br/>
The project went through 4 stages:
- **Stage 1**: Fetch the bitcoin prices from Coin Market Cap web page and insert  it into database.
- **Stage 2**: Fetch tweets from Twitter API, process it through Kafka, then finally insert the tweets as (negative , positive )into database. 
- **Stage 3**: Read the data from SQL and train the model to predict the price.
- **Stage 4**: Build the dashboard as a web page using react to make it accessible for the end user.

![arcitecture!](/icons/architecture.gif)

## PROJECT STRUCTURE
`Data` Folder have all the datasets used to train the models.<br/>
`Models` Folder have Jupyter Notebooks for all different models used in the modeling stage.<br/>
`client-react` is the react web application.<br/>
`server` is a Flask back-end for the react web application.<br/>
