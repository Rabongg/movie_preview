package com.example.movie_preview_v2.persistence.impl;

import com.example.movie_preview_v2.common.TheaterType;
import com.example.movie_preview_v2.model.entity.MovieInfo;
import com.example.movie_preview_v2.model.entity.QMovieInfo;
import com.example.movie_preview_v2.persistence.MovieInfoCustomRepository;
import com.querydsl.core.BooleanBuilder;
import com.querydsl.jpa.impl.JPAQueryFactory;
import lombok.RequiredArgsConstructor;
import org.springframework.data.util.Pair;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
@RequiredArgsConstructor
public class MovieInfoCustomRepositoryImpl implements MovieInfoCustomRepository {

    private final JPAQueryFactory jpaQueryFactory;

    @Override
    public List<MovieInfo> findAllMovieInfoInTitleAndType(List<Pair<String, TheaterType>> pairs) {
        QMovieInfo movieInfo = QMovieInfo.movieInfo; // QueryDSL 엔티티 메타 모델
        BooleanBuilder builder = new BooleanBuilder();

        for (Pair<String, TheaterType> pair : pairs) {
            builder.or(movieInfo.title.eq(pair.getFirst()).and(movieInfo.theater.eq(pair.getSecond())));
        }

        return jpaQueryFactory
                .selectFrom(movieInfo)
                .where(builder)
                .fetch();
    }
}
