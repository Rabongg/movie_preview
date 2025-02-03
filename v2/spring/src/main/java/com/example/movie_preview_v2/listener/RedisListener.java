package com.example.movie_preview_v2.listener;

import com.example.movie_preview_v2.model.dto.MovieInfoDto;
import com.example.movie_preview_v2.service.DatabaseService;
import com.example.movie_preview_v2.service.EmailService;
import com.fasterxml.jackson.core.JsonProcessingException;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.connection.Message;
import org.springframework.data.redis.connection.MessageListener;
import org.springframework.stereotype.Component;
import com.fasterxml.jackson.databind.ObjectMapper;

@Component
@RequiredArgsConstructor
public class RedisListener implements MessageListener {

    @Value("${movie.email.receiver}")
    private String emailReceiver;

    private final ObjectMapper objectMapper;

    private final DatabaseService databaseService;

    private final EmailService emailService;

    @Override
    public void onMessage(Message message, byte[] pattern) {

        MovieInfoDto[] movieInfoList;
        try {
            movieInfoList = objectMapper.readValue(message.toString(), MovieInfoDto[].class);
            emailService.sendEmail(emailReceiver, "시사회 정보 알려드립니다.", movieInfoList);
//          TODO: 로그로 수정
            System.out.println("전송 성공");
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}
