# mobile-app/Dockerfile (optional dev container for Flutter web)
FROM cirrusci/flutter:stable

WORKDIR /app
COPY . .
RUN flutter pub get

CMD ["flutter", "run", "-d", "web-server", "--web-port", "8080", "--web-hostname", "0.0.0.0"]
