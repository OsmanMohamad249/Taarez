# Flutter Environment Configuration

## Overview
The Flutter app uses environment-based configuration through `lib/utils/app_config.dart`. This allows you to run the app with different API endpoints for different environments.

## Default Configuration

By default, the app uses:
- **Android Emulator**: `http://10.0.2.2:8000`
- **iOS Simulator**: `http://localhost:8000`
- **Physical Device**: Your machine's IP address

## Running with Custom Environment

### Option 1: Use --dart-define
```bash
flutter run --dart-define=API_BASE_URL=http://192.168.1.100:8000
```

### Option 2: Use --dart-define-from-file (Flutter 3.7+)
Create a file `config/dev.json`:
```json
{
  "API_BASE_URL": "http://192.168.1.100:8000",
  "ENVIRONMENT": "development"
}
```

Run with:
```bash
flutter run --dart-define-from-file=config/dev.json
```

### Option 3: Create Multiple Configurations

**config/dev.json:**
```json
{
  "API_BASE_URL": "http://10.0.2.2:8000",
  "ENVIRONMENT": "development"
}
```

**config/staging.json:**
```json
{
  "API_BASE_URL": "https://staging-api.tiraz.com",
  "ENVIRONMENT": "staging"
}
```

**config/prod.json:**
```json
{
  "API_BASE_URL": "https://api.tiraz.com",
  "ENVIRONMENT": "production"
}
```

## Available Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_BASE_URL` | Backend API base URL | `http://10.0.2.2:8000` |
| `ENVIRONMENT` | App environment | `development` |

## Network Configuration by Platform

### Android Emulator
- Use `http://10.0.2.2:8000` to access host machine's localhost
- The emulator maps 10.0.2.2 to the host's 127.0.0.1

### iOS Simulator
- Use `http://localhost:8000` directly
- iOS Simulator can access host's localhost directly

### Physical Device
1. Find your machine's IP address:
   - **macOS/Linux**: `ifconfig | grep inet`
   - **Windows**: `ipconfig`
2. Use that IP: `http://192.168.1.X:8000`
3. Ensure backend allows connections from your device IP

## Troubleshooting

### Connection Refused
1. Check if backend is running: `curl http://localhost:8000/health`
2. For physical devices, check firewall settings
3. Verify the correct IP address is being used

### SSL/HTTPS Errors
For development with self-signed certificates, you may need to configure certificate pinning or allow insecure connections (development only).

## Building for Production

```bash
flutter build apk --release --dart-define=API_BASE_URL=https://api.tiraz.com --dart-define=ENVIRONMENT=production
```

## VSCode Configuration

Add to `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Flutter Dev",
      "request": "launch",
      "type": "dart",
      "args": [
        "--dart-define=API_BASE_URL=http://10.0.2.2:8000",
        "--dart-define=ENVIRONMENT=development"
      ]
    },
    {
      "name": "Flutter Production",
      "request": "launch",
      "type": "dart",
      "args": [
        "--dart-define=API_BASE_URL=https://api.tiraz.com",
        "--dart-define=ENVIRONMENT=production"
      ]
    }
  ]
}
```
