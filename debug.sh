#!/bin/sh

env \
    QUART_APP="tremolo:app" \
    QUART_ENV="dev" \
    QUART_DEBUG="True" \
    quart run
