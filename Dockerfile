FROM python:3.8-alpine

# Dokerfile's infos
LABEL maintainer="nekoserv" mail="nekoserv@fai.tld"
LABEL description="Alpine + python3 jokes-api"
LABEL website="https://github.com/TODO/docker-jokes-api"
LABEL version="1.0"

# init
ARG UID
ARG GID

# install
RUN [[ -z "$UID" ]] && UID=$(( $RANDOM % 9000 + 1000 )) || UID=$UID && \
    [[ -z "$GID" ]] && GID=$(( $RANDOM % 9000 + 1000 )) || GID=$UID && \
    addgroup -g $GID user && \
    adduser -S -u $UID -G user user && \
    apk add --no-cache curl tzdata unzip && \
    curl -L https://github.com/nekoserv-repository/jokes-api/archive/refs/heads/main.zip -o main.zip && \
    unzip -q main.zip -d /home/user && \
    chown -R user:user /home/user && \
    python -m pip install --upgrade pip && \
    pip install -r /home/user/jokes-api-main/requirements.txt && \
    rm main.zip && \
    rm -rf /root/.cache/pip/ && \
    apk del --purge curl unzip

# drop privileges
USER user

# run!
ENTRYPOINT ["python", "-u", "/home/user/jokes-api-main/main.py"]
