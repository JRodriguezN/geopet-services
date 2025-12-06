#!/usr/bin/env bash
set -e

# Levanta la app y el stack de monitoreo (Prometheus + Node Exporter + Grafana)

docker compose -f docker-compose.monitoring.yml up --build
