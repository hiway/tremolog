#!/bin/sh

env \
    QUART_APP="tremolog.tremolog:app" \
    QUART_ENV="dev" \
    QUART_DEBUG="True" \
    quart run
