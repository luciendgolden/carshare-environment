package g1.utils;

import org.eclipse.rdf4j.model.Model;
import org.eclipse.rdf4j.model.util.ModelBuilder;
import org.eclipse.rdf4j.query.QueryResults;
import org.eclipse.rdf4j.repository.Repository;
import org.eclipse.rdf4j.repository.RepositoryConnection;
import org.eclipse.rdf4j.repository.http.HTTPRepository;
import org.eclipse.rdf4j.rio.RDFFormat;
import org.eclipse.rdf4j.rio.Rio;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.stereotype.Component;
import org.springframework.beans.factory.annotation.Value;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

@Component
public class DBConnectorRDF4J {

    private static final Logger logger = LoggerFactory.getLogger(DBConnectorRDF4J.class);

    private Repository repository;

    public DBConnectorRDF4J(@Value("${graphdb.repository.uri}") String repositoryUri,
            @Value("${graphdb.repository.id}") String repositoryId,
            @Value("${graphdb.username}") String username,
            @Value("${graphdb.password}") String password) {
        String fullRepositoryUri = repositoryUri + repositoryId;
        this.repository = new HTTPRepository(fullRepositoryUri);
        ((HTTPRepository) repository).setUsernameAndPassword(username, password);
        this.testConnection();
    }

    public void testConnection() {
        try (RepositoryConnection conn = repository.getConnection()) {
            logger.info("Repository size: " + conn.size());
        } catch (Exception e) {
            logger.error("Connection test failed: ", e);
        }
    }

    public void addData(String data) {
        try (RepositoryConnection conn = repository.getConnection()) {
            Model model = Rio.parse(new ByteArrayInputStream(data.getBytes(StandardCharsets.UTF_8)), "",
                    RDFFormat.TURTLE);
            conn.add(model);
        } catch (Exception e) {
            logger.error("Error adding data: ", e);
        }
    }

    public void addDataWithTransaction(String data) {
        try (RepositoryConnection conn = repository.getConnection()) {
            conn.begin();
            Model model = Rio.parse(new ByteArrayInputStream(data.getBytes(StandardCharsets.UTF_8)), "",
                    RDFFormat.TURTLE);
            conn.add(model);
            conn.commit();
            logger.info("Data added successfully with transaction.");
        } catch (Exception e) {
            logger.error("Error adding data with transaction: ", e);
        }
    }

    public String executeSelectQuery(String queryString) {
        StringBuilder result = new StringBuilder();
        try (RepositoryConnection conn = repository.getConnection()) {
            conn.prepareTupleQuery(queryString).evaluate().forEach(bindingSet -> {
                // Process each binding set in the result
                result.append(bindingSet.toString()).append("\n");
            });
        } catch (Exception e) {
            logger.error("Error executing SELECT query: ", e);
        }
        return result.toString();
    }

    public void executeUpdateQuery(String updateQuery) {
        try (RepositoryConnection conn = repository.getConnection()) {
            conn.prepareUpdate(updateQuery).execute();
            logger.info("Update query executed successfully.");
        } catch (Exception e) {
            logger.error("Error executing UPDATE query: ", e);
        }
    }

    public String fetchSchema() {
        StringBuilder result = new StringBuilder();
        try (RepositoryConnection conn = repository.getConnection()) {
            String query = """
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX carshare: <http://example.org/carshare#>

                    CONSTRUCT {
                      ?class a rdfs:Class .

                      ?property a rdf:Property .

                      ?subclass rdfs:subClassOf ?superclass .

                      ?property rdfs:domain ?domain .
                      ?property rdfs:range ?range .
                    }
                    WHERE {
                      {
                        ?class a rdfs:Class .
                        FILTER(STRSTARTS(STR(?class), STR(carshare:)))
                      } UNION {
                        ?property a rdf:Property .
                        FILTER(STRSTARTS(STR(?property), STR(carshare:)))
                        OPTIONAL { ?property rdfs:domain ?domain . }
                        OPTIONAL { ?property rdfs:range ?range . }
                      } UNION {
                        ?subclass rdfs:subClassOf ?superclass .
                        FILTER(STRSTARTS(STR(?subclass), STR(carshare:)) || STRSTARTS(STR(?superclass), STR(carshare:)))
                      }
                    }
                        """;

            Model schemaModel = QueryResults.asModel(conn.prepareGraphQuery(query).evaluate());

            // Convert the model to a string in Turtle format
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            Rio.write(schemaModel, out, RDFFormat.TURTLE);
            result.append(new String(out.toByteArray(), StandardCharsets.UTF_8));
        } catch (Exception e) {
            logger.error("Error fetching schema: ", e);
        }
        return result.toString();
    }
}
