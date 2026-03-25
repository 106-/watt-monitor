SERVICE_NAME := monitor
PROJECT_DIR  := $(shell pwd)
UV           := $(shell which uv)
SERVICE_USER := $(shell whoami)
SERVICE_DEST := /etc/systemd/system/$(SERVICE_NAME).service

.PHONY: install uninstall sync poll probe run

sync:
	uv sync

install: sync
	sed \
		-e 's|@PROJECT_DIR@|$(PROJECT_DIR)|g' \
		-e 's|@UV@|$(UV)|g' \
		-e 's|@USER@|$(SERVICE_USER)|g' \
		monitor.service.tmpl > /tmp/$(SERVICE_NAME).service
	sudo cp /tmp/$(SERVICE_NAME).service $(SERVICE_DEST)
	sudo systemctl daemon-reload
	sudo systemctl enable $(SERVICE_NAME)
	sudo systemctl start $(SERVICE_NAME)
	@echo "Installed: $(SERVICE_DEST)"

run:
	uv run python monitor.py

poll:
	uv run python poll.py

probe:
	uv run python probe.py

uninstall:
	sudo systemctl stop $(SERVICE_NAME)
	sudo systemctl disable $(SERVICE_NAME)
	sudo rm -f $(SERVICE_DEST)
	sudo systemctl daemon-reload
	@echo "Uninstalled: $(SERVICE_DEST)"
