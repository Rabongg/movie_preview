package com.example.movie_preview_v2.service.impl;

import com.example.movie_preview_v2.common.TheaterType;
import com.example.movie_preview_v2.model.dto.MovieInfoDto;
import com.example.movie_preview_v2.model.entity.MovieInfo;
import com.example.movie_preview_v2.persistence.MovieInfoRepository;
import com.example.movie_preview_v2.service.MovieService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.util.Pair;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.dao.DataIntegrityViolationException;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class MovieServiceImpl implements MovieService {

    private final MovieInfoRepository movieInfoRepository;


    @Override
    public List<MovieInfoDto> findNonExistingMovieInfo(MovieInfoDto[] movieInfDtoList) {
        List<Pair<String, TheaterType>> searchPairList = new ArrayList<>();
        List<MovieInfoDto> result = null;
        try {
            for (MovieInfoDto movieInfo : movieInfDtoList) {
                Pair<String, TheaterType> searchPair = Pair.of(movieInfo.getTitle(), TheaterType.valueOf(movieInfo.getTheater()));
                searchPairList.add(searchPair);
            }
            List<MovieInfo> movieInfoList = movieInfoRepository.findAllMovieInfoInTitleAndType(searchPairList);
            List<MovieInfoDto> infoToDto = movieInfoList.stream().map(MovieInfoDto::new).collect(Collectors.toList());
            result = Arrays.stream(movieInfDtoList).filter(movieInfo -> !infoToDto.contains(movieInfo)).collect(Collectors.toList());
        } catch(Exception e) {
            log.error("데이터 처리 중 에러가 발생했습니다.", e);
        }

        return result;
    }

    @Override
    public void saveMovieInfoData(List<MovieInfoDto> movieInfDtoList) {
        for (MovieInfoDto dto : movieInfDtoList){
            try {
                MovieInfo movieInfo = new MovieInfo(dto);
                movieInfoRepository.save(movieInfo);
            } catch (DataIntegrityViolationException e) {
                log.warn("중복으로 인해 저장 건너뜀: {} - {}", dto.getTitle(), dto.getTheater(), e);
            }
            catch (Exception e) {
                log.error("데이터 저장 중 에러가 발생했습니다.", e);
            }
        }
        log.info("데이터 저장 성공");
    }
}
