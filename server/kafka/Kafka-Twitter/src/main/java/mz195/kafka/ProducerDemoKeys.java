package mz195.kafka;


import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Properties;
import java.util.concurrent.ExecutionException;

public class ProducerDemoKeys {
    public static void main(String[] args) throws ExecutionException, InterruptedException {

        Logger logger = LoggerFactory.getLogger(ProducerDemoKeys.class);

        String bootstrapServers = "127.0.0.1:9092";

        // create producer properties
        Properties properties = new Properties();

        properties.setProperty(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        properties.setProperty(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        properties.setProperty(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

        // create producer
        KafkaProducer<String, String> producer = new KafkaProducer<>(properties);

        String topic = "first_topic";
        String value = "Loop iteration: ";
        String key = "id_";

        for(int i=0; i<10; i++){

            // create producer record
            ProducerRecord<String, String> record = new ProducerRecord<>(topic,key + Integer.toString(i) , value + Integer.toString(i));

            logger.info("Key: " + key  + Integer.toString(i)); // log the key

            // id_0 -> 1
            // id_1 -> 0
            // id_2 -> 2
            // id_3 -> 0
            // id_4 -> 2
            // id_5 -> 2
            // id_6 -> 0
            // id_7 -> 2
            // id_8 -> 1
            // id_9 -> 2


            // send data
            producer.send(record, new Callback() {
                @Override
                public void onCompletion(RecordMetadata recordMetadata, Exception e) {
                    if(e == null){
                        // success
                        logger.info("\nReceived new metadata \n" +
                                "Topic: " + recordMetadata.topic() + "\n" +
                                "Partition: " + recordMetadata.partition() + "\n" +
                                "Offset: " + recordMetadata.offset() + "\n" +
                                "Timestamp: " + recordMetadata.timestamp());
                    } else {
                        logger.error("Error while producing", e);
                    }
                }
            }).get();
        }
        // in case you have multiple messages to send
//        producer.flush();
        // flush & close producer
        producer.close();
    }
}
