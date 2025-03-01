package com.example.movie_preview_v2.common;

public enum TheaterType {
    CGV("http://www.cgv.co.kr/search/?query=%uC778%uC0AC"),
    LOTTE("https://www.lottecinema.co.kr/NLCHS/Event/DetailList?code=40"),
    MEGABOX("https://megabox.co.kr/event/curtaincall");

    private final String URL;

    TheaterType(String URL) {
        this.URL = URL;
    }

    public String URL() {
        return URL;
    }
}
