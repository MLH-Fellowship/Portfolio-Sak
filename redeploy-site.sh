#!/bin/bash
SESSION="portfolio"
tmux kill-session -t "$SESSION" 2>/dev/null
tmux new-session -s "$SESSION" \
  'cd ~/Portfolio-Sak &&
git fetch && git reset origin/main --hard &&
source .venv/bin/activate &&
pip install -r requirements.txt &&
systemctl restart myporfolio.service
exec bash'
