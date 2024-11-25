tasks.bootJar {
    archiveBaseName.set("g1_transformtosemanticnetwork")
    archiveVersion.set("1.0.0")
    archiveClassifier.set("release")
    archiveExtension.set("jar")
}

tasks.jar {
    enabled = false
}

plugins {
    id("java")
    id("org.springframework.boot") version "3.2.1"
    id("io.spring.dependency-management") version "1.1.4"
}

group = "g1"
version = "0.1"

repositories {
    mavenCentral()
}

dependencies {
    testImplementation(platform("org.junit:junit-bom:5.9.1"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    implementation("org.apache.jena:apache-jena-libs:4.10.0")
    implementation("org.apache.jena:jena-fuseki-main:4.10.0")
    implementation("org.json:json:20231013")
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.apache.commons:commons-csv:1.10.0")
    implementation("com.azure:azure-ai-openai:1.0.0-beta.6")
    // implementation("org.eclipse.rdf4j:rdf4j-runtime:3.7.3")
    implementation("org.eclipse.rdf4j:rdf4j-runtime:4.3.9")
}

tasks.test {
    useJUnitPlatform()
}