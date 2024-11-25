package g1.utils;

import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdfconnection.RDFConnection;
import org.apache.jena.rdfconnection.RDFConnectionFuseki;
import org.apache.jena.rdfconnection.RDFConnectionRemoteBuilder;
import org.apache.jena.riot.Lang;
import org.apache.jena.riot.RDFDataMgr;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.io.InputStream;
import java.io.StringReader;

@Component
public class DBConnectorJena {

    private static final Logger logger = LoggerFactory.getLogger(DBConnectorJena.class);

    private final RDFConnectionRemoteBuilder builder;

    public DBConnectorJena(@Value("${jena.dataset.uri}") String datasetUri) {
        this.builder = RDFConnectionFuseki.create().destination(datasetUri);
        // this.loadData();
    }

    private void loadData() {
        Model model = ModelFactory.createDefaultModel();
        try (InputStream in = getClass().getClassLoader().getResourceAsStream("preload.ttl")) {
            if (in == null) {
                logger.error("preload.ttl file not found");
                return;
            }
            RDFDataMgr.read(model, in, Lang.TURTLE);
            try (RDFConnection conn = builder.build()) {
                conn.load(model);
                logger.info("Initialized data");
            }
        } catch (Exception e) {
            logger.error("Error initializing data: ", e);
        }
    }

    public void addData(String data) {
        Model model = ModelFactory.createDefaultModel();
        RDFDataMgr.read(model, new StringReader(data), "http://example.org/g1/", Lang.TURTLE);
        
        try (RDFConnection conn = builder.build()) {
            conn.load(model);
        } catch (Exception e) {
            logger.error("Error adding data: ", e);
        }
    }

    public String fetchSchema() {
        StringBuilder result = new StringBuilder();
        try (RDFConnection conn = builder.build()) {
            String query = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?class WHERE { ?class a rdfs:Class }";
            conn.querySelect(query, qs -> result.append("Class: ").append(qs.getResource("class").toString()).append("\n"));
        } catch (Exception e) {
            logger.error("Error fetching schema: ", e);
        }
        return result.toString();
    }
}
