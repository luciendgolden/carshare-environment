package g1.utils;

public class PromptGenerator {

    public static String generatePrompt(String data, String rdfSchema) {

        String promptTemplate = """
                I have a graph database with a specific schema defined in TTL (Turtle) format. I need to extend this graph database by inserting new information. 
                
                Below is the current schema of the graph database:

                %s

                Now, I want to add new information to this graph. Here is the new information that needs to be modeled in TTL:

                %s

                Ensure the new TTL code maintains consistency with the current schema and correctly represents these entities and their relationships as well as the prefix :carshare.

                Please provide the TTL code for adding the above information to the graph database, following the existing schema conventions.

                Only return the turtle code, nothing else.
                """;

        return String.format(promptTemplate, rdfSchema, data).replace("\n", "\\n");

    }

}