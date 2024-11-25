package g1.utils;

import org.json.JSONObject;
import org.json.JSONTokener;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class OpenAIClient {
    private static final Logger logger = LoggerFactory.getLogger(OpenAIClient.class);

    private static final String apiKey = System.getenv("OPENAI_API_KEY");
    private static final String url = "https://api.openai.com/v1/chat/completions";
    private static final String model = "gpt-4";

    public static String getOpenAIResponse(String prompt) {
        HttpURLConnection connection = null;
        try {
            URL obj = new URL(url);
            connection = (HttpURLConnection) obj.openConnection();
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Authorization", "Bearer " + apiKey);
            connection.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
    
            String body = "{\"model\": \"" + model + "\", \"messages\": [{\"role\": \"user\", \"content\": \"" + prompt + "\"}]}";
            connection.setDoOutput(true);
    
            try (OutputStream os = connection.getOutputStream()) {
                byte[] input = body.getBytes(StandardCharsets.UTF_8);
                os.write(input, 0, input.length);
            }
    
            int responseCode = connection.getResponseCode();
            InputStream inputStream = responseCode == 200 ? connection.getInputStream() : connection.getErrorStream();
            StringBuilder response = new StringBuilder();
            try (BufferedReader br = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8))) {
                String line;
                while ((line = br.readLine()) != null) {
                    response.append(line.trim());
                }
            }
    
            if (responseCode == 200) {
                return response.toString();
            } else {
                logger.error("OpenAI API error response: " + response);
                return "Error: Received HTTP code " + responseCode + " from OpenAI API.";
            }
        } catch (IOException e) {
            logger.error("OpenAI API request failed: ", e);
            return "Error: API request failed due to an exception.";
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
    }
}
