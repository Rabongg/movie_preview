package com.example.movie_preview_v2.model.entity;

import com.example.movie_preview_v2.common.TheaterType;
import com.example.movie_preview_v2.model.dto.MovieInfoDto;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.ColumnDefault;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.sql.Timestamp;

@Entity
@Getter
@NoArgsConstructor
@Table(name="movie_curtain_call_info")
public class MovieInfo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name= "ID")
    private Long id;

    @Column(name="title", nullable = false, length = 80)
    private String title;

    @Column(name="period", nullable = false, length = 60)
    private String period;

    @Column(name="theater")
    @Enumerated(EnumType.STRING)
    private TheaterType theater;

    @Column(name="is_send", nullable = false)
    @ColumnDefault("false")
    private boolean isSend;

    @CreationTimestamp
    private Timestamp creationTimestamp;

    @UpdateTimestamp
    private Timestamp updateTimestamp;

    public MovieInfo(MovieInfoDto movieInfoDto) {
        this.title = movieInfoDto.getTitle();
        this.period = movieInfoDto.getDate();
        this.theater = TheaterType.valueOf(movieInfoDto.getTheater().toUpperCase());
    }

}
