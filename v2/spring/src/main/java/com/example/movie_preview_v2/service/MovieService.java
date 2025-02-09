package com.example.movie_preview_v2.service;

import com.example.movie_preview_v2.model.dto.MovieInfoDto;
import com.example.movie_preview_v2.model.entity.MovieInfo;

import java.util.List;

public interface MovieService {

    public List<MovieInfoDto> findNonExistingMovieInfo(MovieInfoDto[] movieInfDtoList);

    public void saveMovieInfoData(List<MovieInfoDto> movieInfDtoList);
}
