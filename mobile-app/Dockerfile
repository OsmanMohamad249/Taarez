# mobile-app/Dockerfile (optional dev container for Flutter web)
FROM cirrusci/flutter:stable

WORKDIR /app

# Preconfigure Flutter for web (this will use cached SDK from base image)
RUN flutter config --enable-web && \
    flutter doctor

COPY . .

# Build and serve the web app
# Note: flutter pub get will run at startup since dependencies may change
CMD ["sh", "-c", "flutter pub get && flutter build web --release && python3 -m http.server 8080 --directory build/web"]
