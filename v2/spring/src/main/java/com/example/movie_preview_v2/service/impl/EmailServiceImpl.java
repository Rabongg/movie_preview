package com.example.movie_preview_v2.service.impl;

import com.example.movie_preview_v2.common.TheaterType;
import com.example.movie_preview_v2.model.dto.MovieInfoDto;
import com.example.movie_preview_v2.model.entity.MovieInfo;
import com.example.movie_preview_v2.service.EmailService;
import jakarta.mail.MessagingException;
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

    private final JavaMailSender mailSender;

    public void sendEmail(String to, String subject, List<MovieInfoDto> movieInfoList) {

        try {
            MimeMessage message = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");

            helper.setTo(to);
            helper.setSubject(subject);

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
                     <style>
                         body { font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; }
                         .container { max-width: 600px; margin: auto; background-color: white; border-radius: 5px;\s
                                      box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 20px; }
                         .header { background-color: #4CAF50; color: white; padding: 15px; text-align: center;\s
                                   border-radius: 5px 5px 0 0; font-size: 20px; font-weight: bold; }
                         .table-container { margin-top: 20px; }
                         table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                         th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
                         th { background-color: #f4f4f4; }
                         .cgv { border-left: 5px solid #ff3d00; }
                         .lotte { border-left: 5px solid #ff9800; }
                         .megabox { border-left: 5px solid #3f51b5; }
                         .footer { text-align: center; padding: 10px; font-size: 12px; color: #777; }
                     </style>
                 </head>
                 <body>
                     <div class="container">
                         <div class="header">🎬 영화 시사회 알림</div>
                         <div class="table-container">
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
                String theaterClass = theater.toLowerCase();
                html_content += String.format("""
                    <table class="%s">
                        <tr>
                            <th colspan="2">%s 시사회</th>
                        </tr>
                        <tr>
                            <th>영화 제목</th>
                            <th>상영 기한</th>
                        </tr>
                """, theaterClass, theater);

                    for (MovieInfoDto movie : movies) {
                        html_content += String.format("""
                    <tr>
                        <td>%s</td>
                        <td>%s</td>
                    </tr>
                """, movie.getTitle(), movie.getDate());
                }
                html_content += "</table>";
            }
        }

        html_content += """
                </div>
               <div class="footer">© 2025 Movie Preview Alarm</div>
               </div>
               </body>
               </html>
            """;

        return html_content;
    }
}
