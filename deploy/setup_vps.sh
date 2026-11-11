#!/usr/bin/env bash
# FUTURESCOUT AI: put the REPORT AGENT on a small always-on Linux server (Ubuntu 22.04 or 24.04), so the owner's laptop
# can be off. Run once, as root, on the new server:
#
#     bash setup_vps.sh git@github.com:OWNER/futurescout-ai.git
#
# What it does: makes a user "futurescout", installs Python and git, makes an SSH key for GitHub (you add it to the
# repository as a deploy key WITH write access), clones the repository, installs the backend, copies the published
# snapshot (backend/site_data) into backend/runs as the starting data, and installs a service that keeps
# `scripts/market_agent.py --publish` running and restarts it after a crash or a reboot.
#
# It also installs a second service for the TRADING agent (`scripts/fund_trade.py watch --publish`), which is left
# switched OFF: the owner turns it on only after deciding to put the trading key on the server (see deploy/VPS.md).
#
# What it does NOT do: it never writes a key or a secret. You create /home/futurescout/futurescout/.env yourself
# (see deploy/VPS.md) and then start the services.
set -euo pipefail

REPO="${1:?usage: bash setup_vps.sh git@github.com:OWNER/futurescout-ai.git}"
APP_USER=futurescout
HOME_DIR="/home/${APP_USER}"
APP_DIR="${HOME_DIR}/futurescout"

if [ "$(id -u)" -ne 0 ]; then echo "run this as root (sudo bash setup_vps.sh ...)"; exit 1; fi

echo "== 1/6 packages"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3 python3-venv python3-pip git ca-certificates >/dev/null

echo "== 2/6 user ${APP_USER}"
id -u "${APP_USER}" >/dev/null 2>&1 || adduser --disabled-password --gecos "" "${APP_USER}" >/dev/null

echo "== 3/6 SSH key for GitHub"
sudo -u "${APP_USER}" bash -c 'mkdir -p ~/.ssh && chmod 700 ~/.ssh && [ -f ~/.ssh/id_ed25519 ] || ssh-keygen -q -t ed25519 -N "" -C "futurescout-report-agent" -f ~/.ssh/id_ed25519'
sudo -u "${APP_USER}" bash -c 'ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts 2>/dev/null; sort -u ~/.ssh/known_hosts -o ~/.ssh/known_hosts'
echo
echo "Add this PUBLIC key to the repository on GitHub: Settings -> Deploy keys -> Add deploy key,"
echo "title 'report agent server', tick 'Allow write access'. (It is a public key: safe to copy.)"
echo
cat "${HOME_DIR}/.ssh/id_ed25519.pub"
echo
read -r -p "Press Enter when the deploy key is added... " _

echo "== 4/6 code"
if [ -d "${APP_DIR}/.git" ]; then
  sudo -u "${APP_USER}" git -C "${APP_DIR}" pull -q --rebase
else
  sudo -u "${APP_USER}" git clone -q "${REPO}" "${APP_DIR}"
fi
# commits made by the agent (site data updates) carry the same author as the repository's latest commit
NAME="$(sudo -u "${APP_USER}" git -C "${APP_DIR}" log -1 --format=%an)"
MAIL="$(sudo -u "${APP_USER}" git -C "${APP_DIR}" log -1 --format=%ae)"
sudo -u "${APP_USER}" git -C "${APP_DIR}" config user.name "${NAME}"
sudo -u "${APP_USER}" git -C "${APP_DIR}" config user.email "${MAIL}"

echo "== 5/6 Python environment and starting data"
sudo -u "${APP_USER}" bash -c "cd '${APP_DIR}' && python3 -m venv .venv && .venv/bin/python -m pip install -q --upgrade pip && .venv/bin/python -m pip install -q -e backend"
# starting data: the published snapshot becomes backend/runs (never overwrites files that are already there)
sudo -u "${APP_USER}" bash -c "mkdir -p '${APP_DIR}/backend/runs' && cp -rn '${APP_DIR}/backend/site_data/.' '${APP_DIR}/backend/runs/'"
if [ ! -f "${APP_DIR}/.env" ]; then
  sudo -u "${APP_USER}" cp "${APP_DIR}/.env.example" "${APP_DIR}/.env"
  chmod 600 "${APP_DIR}/.env"
fi

echo "== 6/6 service"
cat > /etc/systemd/system/futurescout-agent.service <<UNIT
[Unit]
Description=FUTURESCOUT AI report agent (Agent Market jobs, topic proposals, research, seals, publishing)
After=network-online.target
Wants=network-online.target

[Service]
User=${APP_USER}
WorkingDirectory=${APP_DIR}/backend
ExecStart=${APP_DIR}/.venv/bin/python scripts/market_agent.py --publish
Environment=PYTHONUNBUFFERED=1
Restart=always
RestartSec=30
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
UNIT
cat > /etc/systemd/system/futurescout-trader.service <<UNIT
[Unit]
Description=FUTURESCOUT AI trading agent (buys reports, trades inside the owner's limits, stakes the report agent's earnings)
After=network-online.target
Wants=network-online.target

[Service]
User=${APP_USER}
WorkingDirectory=${APP_DIR}/backend
ExecStart=${APP_DIR}/.venv/bin/python scripts/fund_trade.py watch --publish
Environment=PYTHONUNBUFFERED=1
Restart=always
RestartSec=60
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
UNIT
systemctl daemon-reload
systemctl enable -q futurescout-agent
# futurescout-trader is installed but NOT enabled: the owner switches it on (deploy/VPS.md, "Trading agent")

echo
echo "Installed. The agent is NOT started yet: it needs your keys."
echo "  1. Fill in the keys:   sudo -u ${APP_USER} nano ${APP_DIR}/.env      (see deploy/VPS.md for the list)"
echo "  2. Start it:           systemctl start futurescout-agent"
echo "  3. Watch it:           journalctl -u futurescout-agent -f"
echo "Stop the report agent on your laptop first: two agents would both take the same jobs."
echo "The trading agent is installed but off. To use it, read 'Trading agent' in deploy/VPS.md first."
