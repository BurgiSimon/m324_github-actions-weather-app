# MQTT Wetterstationen

![CI/CD Pipeline](https://github.com/solerbus/m324_github-actions-weather-app/actions/workflows/ci-cd.yml/badge.svg)

Dieses Projekt simuliert verteilte Wetterstationen, die Messdaten über MQTT an einen Broker senden.

## Setup

1. Starte alles mit:
   ```bash
   docker-compose up --build
   ```

2. Öffne ein neues Terminal und starte den Subscriber:
   ```bash
   cd subscriber
   pip install -r requirements.txt
   python main.py
   ```

## Aufgabe

- Abonniere Wetterdaten vom Topic `weather`
- Speichere die Daten sinnvoll (z. B. JSON-Datei, SQLite)
- Erstelle einfache Auswertungen (Durchschnitt, Verlauf, usw.)

## CI/CD Pipeline

Dieses Projekt verfügt über eine vollautomatische CI/CD Pipeline mit GitHub Actions:

### Pipeline-Jobs

1. **Lint** - Überprüft den Python-Code mit ruff
2. **Test** - Führt pytest-Tests mit Coverage-Reporting aus
3. **Docker Build & Push** - Erstellt und veröffentlicht das Docker-Image auf DockerHub

### Automatisches Publishing

- **Docker Image**: `solerbus/m324-mqtt`
- **Trigger**: Bei jedem Push auf den `main` Branch
- **Tags**: `latest` und `sha-<commit-hash>`
- **Voraussetzung**: Alle Tests und Linting-Checks müssen erfolgreich sein

### Pull Request Checks

Pull Requests durchlaufen automatisch Lint- und Test-Checks. Das Docker-Image wird nur bei Merges in `main` publiziert.

## Lokale Entwicklung

### Tests ausführen

```bash
cd stations
python3 -m venv .venv
source .venv/bin/activate  # Oder: .venv\Scripts\activate auf Windows
pip install -r requirements-dev.txt
pytest -v --cov=. --cov-report=term-missing
```

### Linting ausführen

```bash
cd stations
ruff check station1.py test_station1.py
```

### Docker Image lokal bauen

```bash
cd stations
docker build -t weather-station .
docker run -e STATION_ID=WS-TEST -e INTERVAL=5 weather-station
```

## Docker Image von DockerHub verwenden

```bash
docker pull solerbus/m324-mqtt:latest
docker run -e STATION_ID=WS-01 -e INTERVAL=5 solerbus/m324-mqtt:latest
```
