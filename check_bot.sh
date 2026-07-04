#!/bin/bash
cd /home/administrator/suane-tg-bot
if ! sudo docker compose ps | grep -q "Up"; then
  sudo docker compose restart bot
fi
