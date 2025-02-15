package com.example.movie_preview_v2.model.dto;

import com.example.movie_preview_v2.model.entity.MovieInfo;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.ToString;

import java.util.Objects;

@Getter
@NoArgsConstructor
@ToString
public class MovieInfoDto {
    @JsonProperty("movie_title")
    private String title;

    @JsonProperty("movie_date")
    private String date;

    private String theater;

    public MovieInfoDto(MovieInfo movieInfo) {
        this.title = movieInfo.getTitle();
        this.date = movieInfo.getPeriod();
        this.theater = String.valueOf(movieInfo.getTheater());
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        MovieInfoDto that = (MovieInfoDto) o;
        return getTitle().equals(that.getTitle()) && getDate().equals(that.getDate()) && getTheater().equals(that.getTheater());
    }

    @Override
    public int hashCode() {
        return Objects.hash(getTitle(), getDate(), getTheater());
    }
}
