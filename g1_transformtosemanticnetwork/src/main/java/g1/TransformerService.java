package g1;

import g1.utils.DBConnectorRDF4J;
import g1.utils.Extractor;
import g1.utils.OpenAIClient;
import g1.utils.PromptGenerator;

import org.json.JSONObject;
import org.json.JSONTokener;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;

import java.util.List;
import java.util.Objects;

import org.springframework.stereotype.Service;

@Service
public class TransformerService {

    private static final Logger logger = LoggerFactory.getLogger(TransformerService.class);

    private final DBConnectorRDF4J dbConnector;

    @Autowired
    public TransformerService(DBConnectorRDF4J dbConnector) {
        this.dbConnector = dbConnector;
    }
    
    public  String handleTransformation(String data, String type) {
        try {
            if (Objects.equals(type, "text/csv")) {
                return handleCSV(data);
            } else if (Objects.equals(type, MediaType.TEXT_PLAIN.toString())) {
                return handleText(data);
            } else {
                return handleOther(data);
            }
        } catch (Exception e) {
            logger.error("Error: " + e);
            throw e;
        }
    }

    public String handleText(String data) {
        logger.info("Text detected");
        List<String> t = Extractor.extractNaturalTextData(data);
        StringBuilder result = new StringBuilder();
        for (String row : t) {
            result.append(this.sendRequest(row)).append("\n");
        }
        return result.toString();
    }

    public String handleCSV(String data) {
        List<String> t = Extractor.extractCSVData(data);
        StringBuilder result = new StringBuilder();
        for (String row : t) {
            result.append(this.sendRequest(row)).append("\n");
        }
        return result.toString();
    }

    public String handleOther(String data) {
        if (data.length() > 6000) {
            throw new RuntimeException("Data is too big");
        }
        return sendRequest(data);
    }

    private String sendRequest(String data) {

        //1. GET RDF Schema from database
        String rdfSchema = dbConnector.fetchSchema();
        logger.info(rdfSchema);

        //2. Generate Prompt for the OpenAI API
        String prompt = PromptGenerator.generatePrompt(data, rdfSchema);
        logger.info(prompt);
        
        //3. Get Response from OpenAI
        String jsonResponse = OpenAIClient.getOpenAIResponse(prompt);
        logger.info(jsonResponse);

        //4. Update database
        String content = extractMessageFromJSONResponse(jsonResponse);
        // dbConnector.addData(content);

        return content;
    }

    public void handleAddData(String data) throws Exception {
        dbConnector.addData(data);
    }    

    private String extractMessageFromJSONResponse(String response) {
        JSONObject json = new JSONObject(new JSONTokener(response));
        JSONObject choice = json.getJSONArray("choices").getJSONObject(0);
        JSONObject message = choice.getJSONObject("message");
        return message.getString("content");
    }
}
