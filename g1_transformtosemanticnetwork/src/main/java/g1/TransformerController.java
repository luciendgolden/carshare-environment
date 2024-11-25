package g1;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;

import java.io.IOException;
import java.nio.charset.StandardCharsets;

@RestController
@CrossOrigin(origins = "*")
public class TransformerController {

    private static final Logger logger = LoggerFactory.getLogger(TransformerController.class);

    private final TransformerService service;

    @Autowired
    public TransformerController(TransformerService service) {
        this.service = service;
    }

    @GetMapping("/")
    public ResponseEntity<String> getApiDescription() {
        String jsonResponse = "{\n" +
                "  \"apiDescription\": \"Semantic Network Transformer Server API\",\n" +
                "  \"version\": \"1.0.0\",\n" +
                "  \"endpoints\": [\n" +
                "    {\n" +
                "      \"path\": \"/transform\",\n" +
                "      \"method\": \"POST\",\n" +
                "      \"description\": \"Transforms open data formats into RDF triples. Expects a file upload with key 'file'. Supports .csv and .txt formats.\",\n"
                +
                "      \"contentType\": \"multipart/form-data\",\n" +
                "      \"parameters\": {\n" +
                "        \"file\": \"File to be transformed (CSV or TXT format)\"\n" +
                "      },\n" +
                "      \"response\": {\n" +
                "        \"contentType\": \"application/rdf+xml\",\n" +
                "        \"description\": \"RDF triples representing the semantic network derived from the input file.\"\n"
                +
                "      },\n" +
                "      \"examples\": {\n" +
                "        \"request\": {\n" +
                "          \"url\": \"http://localhost:8080/transform\",\n" +
                "          \"method\": \"POST\",\n" +
                "          \"headers\": {\n" +
                "            \"Content-Type\": \"multipart/form-data\"\n" +
                "          },\n" +
                "          \"body\": \"file=@NaturalLanguage.txt\"\n" +
                "        },\n" +
                "        \"response\": {\n" +
                "          \"status\": 200,\n" +
                "          \"body\": \"<rdf:RDF ...>...</rdf:RDF>\"\n" +
                "        }\n" +
                "      }\n" +
                "    }\n" +
                "  ],\n" +
                "  \"notes\": \"Ensure the Docker application is running and accessible. The server expects an OpenAI API key for AI functionalities, configured via environment variables in docker-compose.yml.\",\n"
                +
                "}";

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        return new ResponseEntity<>(jsonResponse, headers, HttpStatus.OK);

    }

    @PostMapping("/transform")
    public ResponseEntity<String> transformData(MultipartFile file) throws IOException {
        String value = new String(file.getBytes(), StandardCharsets.UTF_8);

        // Replace with Unix-style
        String unixValue = value.replace("\r\n", "\n").replace('\"', '\'');

        String type = file.getContentType();

        logger.info("Received a " + type + " file");

        try {
            String response = service.handleTransformation(unixValue, type);
            return ResponseEntity
                    .ok(response);
        } catch (Exception e) {
            return ResponseEntity
                    .badRequest()
                    .body("Data couldn't be processed or File type is not supported");
        }
    }

    @PostMapping("/add/ttl")
    public ResponseEntity<String> addData(@RequestParam("file") MultipartFile file) {
        String type = file.getContentType();

        logger.info("Received a file with content type: " + type);

        try {
            service.handleAddData(new String(file.getBytes(), StandardCharsets.UTF_8));
            return ResponseEntity.ok("Data added successfully");
        } catch (Exception e) {
            logger.error("Error processing data: ", e.getMessage(), e);
            return ResponseEntity.badRequest()
                    .body("Data couldn't be processed or File type is not supported. Error: " + e.getMessage());
        }
    }
}
