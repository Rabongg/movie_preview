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
                emailService.sendEmail(newMovieInfo);
                movieService.saveMovieInfoData(newMovieInfo);
            }
        } catch (Exception e) {
            log.error("Redis로부터 받은 데이터 처리 중에 에러가 발생했습니다.", e);
        }
    }
}
