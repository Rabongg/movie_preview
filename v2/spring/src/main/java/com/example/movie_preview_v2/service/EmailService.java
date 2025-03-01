package com.example.movie_preview_v2.service;

import com.example.movie_preview_v2.model.dto.MovieInfoDto;

import java.util.List;

public interface EmailService {

    public void sendEmail(List<MovieInfoDto> movieInfoList) throws Exception;
}
