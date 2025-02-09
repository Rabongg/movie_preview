package com.example.movie_preview_v2.listener;

import com.example.movie_preview_v2.model.dto.MovieInfoDto;
import com.example.movie_preview_v2.service.MovieService;
import com.example.movie_preview_v2.service.EmailService;
import com.fasterxml.jackson.core.JsonProcessingException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.connection.Message;
import org.springframework.data.redis.connection.MessageListener;
import org.springframework.stereotype.Component;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.List;
import java.util.stream.Collectors;

@Slf4j
@Component
@RequiredArgsConstructor
public class RedisListener implements MessageListener {

    @Value("${movie.email.receiver}")
    private String emailReceiver;

    private final ObjectMapper objectMapper;

    private final MovieService movieService;

    private final EmailService emailService;

    @Override
    public void onMessage(Message message, byte[] pattern) {

        MovieInfoDto[] movieInfoList;
        try {
            log.info("Redis 로부터 받은 정보");
            log.info(message.toString());
            movieInfoList = objectMapper.readValue(message.toString(), MovieInfoDto[].class);

            List<MovieInfoDto> newMovieInfo = movieService.findNonExistingMovieInfo(movieInfoList);

            log.info("저장해야할 데이터 {}", (newMovieInfo.stream()
                    .map(MovieInfoDto::toString)
                    .collect(Collectors.joining(", "))));

            if (!newMovieInfo.isEmpty()) {
                emailService.sendEmail(emailReceiver, "시사회 정보 알려드립니다.", newMovieInfo);
                movieService.saveMovieInfoData(newMovieInfo);
            }

        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        } catch (Exception e) {
            log.error(e.getMessage());
        }
    }
}
