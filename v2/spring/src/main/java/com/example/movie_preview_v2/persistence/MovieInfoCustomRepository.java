package com.example.movie_preview_v2.persistence;

import com.example.movie_preview_v2.common.TheaterType;
import com.example.movie_preview_v2.model.entity.MovieInfo;
import org.springframework.data.util.Pair;

import java.util.List;

public interface MovieInfoCustomRepository {

    List<MovieInfo> findAllMovieInfoInTitleAndType(List<Pair<String, TheaterType>> pairs);
}
