package com.example.movie_preview_v2.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Getter
@AllArgsConstructor
@NoArgsConstructor
@ToString
public class MovieInfoDto {
    @JsonProperty("movie_title")
    private String title;

    @JsonProperty("movie_date")
    private String date;

    private String theater;

}
