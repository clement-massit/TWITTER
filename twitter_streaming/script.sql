set NAMES 'UTF8';


DROP TABLE IF EXISTS tweets_streaming;
CREATE TABLE tweets_streaming (
    id_tweet int(100) NOT NULL AUTO_INCREMENT, 
    created_at varchar(100), 
    user_name varchar(100), 
    text_contenu varchar(255), 
    latitude varchar(100), 
    longitude varchar(100), 
    place varchar(100), 
    id_place varchar(100),
    PRIMARY KEY (id_tweet),
    FOREIGN KEY (id_place) REFERENCES polygon(id_place)

);



DROP TABLE IF EXISTS polygon;
CREATE TABLE polygon (
    id_place varchar(100), 
    place varchar(100), 
    lat_1 varchar(100), 
    long_1 varchar(100), 
    lat_2 varchar(100), 
    long_2 varchar(100), 
    lat_3 varchar(100), 
    long_3 varchar(100), 
    lat_4 varchar(100), 
    long_4 varchar(100), 
    lat_5 varchar(100),  
    long_5 varchar(100)
);


