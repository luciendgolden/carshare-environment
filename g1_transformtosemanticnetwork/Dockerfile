FROM openjdk:17-jdk-slim as build

WORKDIR /app

COPY gradlew gradlew.bat /app/
COPY gradle /app/gradle
COPY build.gradle.kts /app/

COPY src /app/src

RUN chmod +x ./gradlew
RUN ./gradlew bootJar

FROM openjdk:17-jdk-slim

COPY --from=build /app/build/libs/g1_transformtosemanticnetwork-1.0.0-release.jar /app/g1_transformtosemanticnetwork.jar

EXPOSE 8081

CMD ["java", "-jar", "/app/g1_transformtosemanticnetwork.jar"]
