package com.github.mz195.kafka.filter.tweets;

import com.google.gson.JsonParser;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.KStream;

import java.util.Properties;

public class StreamsFilterTweets {
    public static void main(String[] args) {
        new StreamsFilterTweets().run();
    }

    public StreamsFilterTweets(){}

    public void run(){

        String bootstrapServers = "127.0.0.1:9092";
        String streamsApplication = "kafka-streams-demo";

        // create properties
        Properties properties = new Properties();
        properties.setProperty(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        properties.setProperty(StreamsConfig.APPLICATION_ID_CONFIG, streamsApplication);
        properties.setProperty(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.StringSerde.class.getName());
        properties.setProperty(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.StringSerde.class.getName());

        // create topology
        StreamsBuilder streamsBuilder = new StreamsBuilder();

        // input topic
        KStream<String, String> inputTopic = streamsBuilder.stream("twitter_tweets");
        KStream<String, String> filteredStream = inputTopic.filter(
                // filter for tweets which author have more then 5,000 followers OR the tweet hace more than 100 retweet
                (k, jsonTweet) -> (extractFollowersFromTweet(jsonTweet) > 5000 || extractRetweetsFromTweet(jsonTweet) > 100)
        );
        filteredStream.to("important_tweets");

        // build the topology
        KafkaStreams kafkaStreams = new KafkaStreams(
                streamsBuilder.build(),
                properties
        );

        // start our streams application
        kafkaStreams.start();
    }

    private static Integer extractFollowersFromTweet(String tweet){
        try {
            return JsonParser.parseString(tweet)
                    .getAsJsonObject()
                    .get("user")
                    .getAsJsonObject()
                    .get("followers_count")
                    .getAsInt();
        } catch (NullPointerException e){
            return 0;
        }
    }

    private static Integer extractRetweetsFromTweet(String tweet){
        try {
            return JsonParser.parseString(tweet)
                    .getAsJsonObject()
                    .get("user")
                    .getAsJsonObject()
                    .get("retweet_count")
                    .getAsInt();
        } catch (NullPointerException e){
            return 0;
        }
    }
}
