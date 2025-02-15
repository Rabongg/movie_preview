package com.example.movie_preview_v2.persistence;

import com.example.movie_preview_v2.common.TheaterType;
import com.example.movie_preview_v2.model.entity.MovieInfo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.data.util.Pair;

import java.util.List;

public interface MovieInfoRepository extends JpaRepository<MovieInfo, Long>, MovieInfoCustomRepository {

    @Query("SELECT e FROM MovieInfo e WHERE (e.title, e.theater) IN :pairs")
    List<MovieInfo> findExistingMovieInfo(@Param("pairs") List<Pair<String, TheaterType>> pairs);
}
