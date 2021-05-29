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
    apk add --no-cache curl tzdata && \
    curl -L https://github.com/nekoserv-repository/jokes-api/archive/refs/heads/main.tar.gz -o main.tar.gz && \
    tar xzf main.tar.gz --strip 1 -C /home/user && \
    chown -R user:user /home/user && \
    rm main.tar.gz && \
    apk del --purge curl

# drop privileges
USER user

# dependencies
RUN cd && \
    pip3 install --no-cache-dir --upgrade --user pip && \
    pip3 install --no-cache-dir --no-warn-script-location --user -r /home/user/requirements.txt

# run!
ENTRYPOINT ["python", "-u", "/home/user/jokes-api.py"]
