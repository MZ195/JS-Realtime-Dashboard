require("dotenv").config();

const config = {
  KafkaHost: "127.0.0.1:9092",
  KafkaTopic: "analyzed_tweets",
};

module.exports = config;
