package com.example.movie_preview_v2.service;

import com.example.movie_preview_v2.model.dto.MovieInfoDto;

public interface EmailService {

    public void sendEmail(String to, String subject, MovieInfoDto[] movieInfoList) throws Exception;
}
