package com.example.movie_preview_v2.service.impl;

import com.example.movie_preview_v2.common.TheaterType;
import com.example.movie_preview_v2.model.dto.MovieInfoDto;
import com.example.movie_preview_v2.service.EmailService;
import org.apache.commons.text.StringEscapeUtils;

import jakarta.mail.internet.MimeMessage;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Slf4j
@Service
@RequiredArgsConstructor
public class EmailServiceImpl implements EmailService {

    @Value("${movie.email.sender}")
    private String emailSender;

    @Value("${movie.email.receiver}")
    private String[] emailReceiver;

    private final JavaMailSender mailSender;

    private final String SUBJECT = "시사회 정보 알려드립니다.";

    public void sendEmail(List<MovieInfoDto> movieInfoList) {

        try {
            MimeMessage message = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");

            helper.setBcc(emailReceiver);
            helper.setSubject(SUBJECT);

            helper.setFrom(emailSender); // 보내는 사람

            // HTML 내용
            String htmlContent = getEmailContent(movieInfoList);

            helper.setText(htmlContent, true); // 두 번째 인자를 true로 설정하면 HTML 형식으로 전송

            mailSender.send(message);
            log.info("이메일 전송 성공하였습니다.");
        } catch (Exception e) {
            log.error("이메일 전송 실패하였습니다.:");
            log.error(String.format(" 원인: %s", e.getMessage()));
            log.error(e.getMessage());
            throw new RuntimeException(e);
        }

    }

    private String getEmailContent(List<MovieInfoDto> movieInfoDtos) {
        String html_content = """
                <!DOCTYPE html>
                 <html>
                 <head>
                     <title>영화 시사회 알림</title>
                 </head>
                 <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
                     <div class="container" style=" max-width: 600px; margin: auto; background-color: white;\s
                        border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 20px;">
                         <div class="header" style="background-color: #4CAF50; color: white; padding: 15px; text-align: center;\s
                            border-radius: 5px 5px 0 0; font-size: 20px; font-weight: bold;">
                            🎬 영화 시사회 알림
                         </div>
                         <div class="table-container" style="margin-top: 20px;">
                    """;

        Map<String, List<MovieInfoDto>> theaterMap = new HashMap<>();
        theaterMap.put(TheaterType.CGV.name(), new ArrayList<>());
        theaterMap.put(TheaterType.LOTTE.name(), new ArrayList<>());
        theaterMap.put(TheaterType.MEGABOX.name(), new ArrayList<>());

        for (MovieInfoDto movie : movieInfoDtos) {
            String theater = movie.getTheater();
            if (theaterMap.containsKey(theater)) {
                theaterMap.get(theater).add(movie);
            }
        }

        // 각 영화관별로 테이블 생성
        for (String theater : theaterMap.keySet()) {
            List<MovieInfoDto> movies = theaterMap.get(theater);
            if (!movies.isEmpty()) {
                html_content += String.format("""
                    <table style="width: 100%%; border-collapse: collapse; margin-bottom: 20px; %s">
                        <tr>
                            <th colspan="2" style="border: 1px solid #ddd; padding: 10px; text-align: left; background-color: #f4f4f4;">
                                %s 시사회
                            </th>
                        </tr>
                        <tr>
                            <th style="border: 1px solid #ddd; padding: 10px; text-align: left; background-color: #f4f4f4;">
                                영화 제목
                            </th>
                            <th style="border: 1px solid #ddd; padding: 10px; text-align: left; background-color: #f4f4f4;">
                                상영 기한
                            </th>
                        </tr>
                """, getStyleByTheaterType(theater), theater);

                for (MovieInfoDto movie : movies) {
                    html_content += String.format("""
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 10px; text-align: left;">%s</td>
                        <td style="border: 1px solid #ddd; padding: 10px; text-align: left;">%s</td>
                    </tr>
                """, StringEscapeUtils.escapeHtml4(movie.getTitle()), movie.getDate());
                }
                html_content += "</table>";
            }
        }

        html_content += """
                </div>
               <div class="footer" style="text-align: center; padding: 10px; font-size: 12px; color: #777;">
                    © 2025 Movie Preview Alarm
               </div>
               </div>
               </body>
               </html>
            """;

        return html_content;
    }

    private String getStyleByTheaterType(String theaterType) {
        String theaterStyle;
        if (TheaterType.CGV.name().equalsIgnoreCase(theaterType)) {
            theaterStyle = "border-left: 5px solid #ff3d00;";
        } else if (TheaterType.MEGABOX.name().equalsIgnoreCase(theaterType)) {
            theaterStyle = "border-left: 5px solid #3f51b5;";
        } else {
            theaterStyle = "border-left: 5px solid #ff9800;";
        }

        return theaterStyle;
    }
}
