package com.example.movie_preview_v2.config;

import com.example.movie_preview_v2.listener.RedisListener;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.connection.lettuce.LettuceConnectionFactory;
import org.springframework.data.redis.listener.RedisMessageListenerContainer;
import org.springframework.data.redis.listener.PatternTopic;

@Configuration
public class RedisConfig {

    @Value("${movie.redis.host}")
    private String redisHost;

    @Value("${movie.redis.port}")
    private Integer redisPort;

    @Value("${movie.redis.topic}")
    private String redisTopic;


    @Bean
    public RedisConnectionFactory redisConnectionFactory() {
        return new LettuceConnectionFactory(redisHost, redisPort); // Redis 연결 설정
    }

    @Bean
    public RedisMessageListenerContainer redisMessageListenerContainer(RedisConnectionFactory redisConnectionFactory, RedisListener redisListener) {
        RedisMessageListenerContainer container = new RedisMessageListenerContainer();
        container.setConnectionFactory(redisConnectionFactory);  // Redis 연결 설정
        container.addMessageListener(redisListener, new PatternTopic(redisTopic));  // 구독할 채널 지정
        return container;
    }

}
