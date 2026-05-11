#!/bin/bash
set -e

export LEDGERGUARD_API_KEY=demo-ledgerguard-key

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
