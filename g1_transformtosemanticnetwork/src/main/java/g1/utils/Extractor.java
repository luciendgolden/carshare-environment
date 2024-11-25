package g1.utils;

import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONTokener;

import org.apache.commons.csv.*;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;

public class Extractor {

    // 1000 tokens ~ 4000 characters
    private static final int characterLimit = 6000;

    public static List<String> extractNaturalTextData(String data) {
        List<String> response = new ArrayList<>();

        int pos = 0;
        while (data.length() > pos) {
            String sub = data.substring(pos, Math.min(pos + characterLimit, data.length()));
            int period = sub.lastIndexOf(".");
            if (period <= 0 || pos > 4) {
                break;
            }
            sub = sub.substring(0, period+1);
            pos += period + 1;

            response.add(sub);
        }
        return response;
    }

    public static List<String> extractCSVData(String data) {
        List<String> response = new ArrayList<>();
        response.add("");
        try (CSVParser csvParser = CSVParser.parse(data, CSVFormat.DEFAULT)) {
            List<String> headers = new ArrayList<>();
            if (csvParser.getHeaderMap() != null) {
                headers.addAll(csvParser.getHeaderMap().keySet());
            }

            int pos = 0;
            for (CSVRecord record : csvParser) {
                String rawRecord = String.join(",", record.values());
                if (response.get(pos).length() + rawRecord.length() > characterLimit) {
                    response.add("");
                    pos++;
                }
                if (pos > 4)
                    break;
                response.set(pos, response.get(pos) + rawRecord + "\n");
            }

        } catch (Exception e) {

        }

        return response;
    }
}