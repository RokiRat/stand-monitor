"""Проверка docker-compose.yml для stand-monitor.

Падает с кодом 1, если у app нет healthcheck или порт слушает не только localhost.
Запуск из корня репозитория: python check_compose.py
"""

import sys

import yaml

COMPOSE_FILE = "docker-compose.yml"
LOCALHOST = "127.0.0.1"


def published_on_localhost(port):
    """Порт в Compose бывает строкой или словарём."""
    if isinstance(port, str):
        left = port.split(":")[0]
        return left == LOCALHOST
    if isinstance(port, dict):
        return port.get("host_ip") == LOCALHOST
    return False


def main():
    with open(COMPOSE_FILE, encoding="utf-8") as fh:
        compose = yaml.safe_load(fh)

    services = compose.get("services") or {}
    errors = []

    app = services.get("app")
    if not app or "healthcheck" not in app:
        errors.append("сервис app: нет ключа healthcheck")

    for name, service in services.items():
        for port in service.get("ports") or []:
            if not published_on_localhost(port):
                errors.append(f"сервис {name}: порт {port!r} без {LOCALHOST}")

    if errors:
        print("compose check failed:")
        for item in errors:
            print(f"- {item}")
        return 1

    print("compose check ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
