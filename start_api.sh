#!/usr/bin/env bash
export QUIMBAYAS_TYPE_STORAGE=fb # firebase
export QUIMBAYAS_API_CREDENTIALS=firebase-sdk.json
export QUIMBAYAS_API_HOST=0.0.0.0
export QUIMBAYAS_API_PORT=7000

python3 -m api.v1.app
