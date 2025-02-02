package com.example.movie_preview_v2.service.impl;

import com.example.movie_preview_v2.model.dto.MovieInfoDto;
import com.example.movie_preview_v2.model.entity.MovieInfo;
import com.example.movie_preview_v2.service.EmailService;
import jakarta.mail.internet.MimeMessage;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class EmailServiceImpl implements EmailService {

    @Value("${movie.email.sender}")
    private String emailSender;

    private final JavaMailSender mailSender;

    public void sendEmail(String to, String subject, MovieInfoDto[] movieInfoList) throws Exception{
        MimeMessage message = mailSender.createMimeMessage();
        MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");

        helper.setTo(to);
        helper.setSubject(subject);

        helper.setFrom(emailSender); // 보내는 사람

        // HTML 내용

        String htmlContent = getEmailContent(movieInfoList);

        helper.setText(htmlContent, true); // 두 번째 인자를 true로 설정하면 HTML 형식으로 전송

        mailSender.send(message);
    }

    private String getEmailContent(MovieInfoDto[] movieInfoDtos) {
        String html_content = """
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>영화 정보</title>
                        <style>
                            body { font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; }
                            .container { max-width: 600px; margin: auto; background-color: white; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                            .header { background-color: #4CAF50; color: white; padding: 15px; text-align: center; border-radius: 5px 5px 0 0; }
                            .movie { border-bottom: 1px solid #ccc; padding: 15px; }
                            .movie:last-child { border-bottom: none; }
                            .title { font-size: 18px; font-weight: bold; }
                            .date { color: #555; }
                            .cinemas { margin-top: 5px; }
                            .cinema { background-color: #f1f1f1; padding: 5px; border-radius: 3px; display: inline-block; margin-right: 5px; }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <div class="header">
                                <h1>영화 정보</h1>
                            </div>
                            <div class="content">
                    """;

        for (MovieInfoDto movie: movieInfoDtos) {
            html_content += String.format("""
                        <div class="movie">
                            <div class="title">%s</div>
                            <div class="date">상영 기한: %s</div>
                            <div class="cinemas">
                                <strong>영화관: %s</strong>
                            </div>
                        </div>
                    """, movie.getTitle(), movie.getDate(), movie.getTheater());
        }

        html_content += """
                        </div>
                    </div>
                </body>
                </html>
                """;

        return html_content;
    }
}
