FROM python:3.11.2-alpine3.17

WORKDIR /app

RUN apk update \
 && apk add --no-cache \
        build-base \
        sdl2-dev \
        freetype-dev \
        sdl2_image-dev \
        sdl2_mixer-dev \
        sdl2_ttf-dev \
        ffmpeg-dev \
        jpeg-dev

RUN python -m pip install --upgrade pip

COPY requirements.txt /app/

RUN python -m pip install -r requirements.txt

COPY pac_man /app/pac_man

CMD [ "python", "-m", "pac_man" ]
