FROM nginx:latest

RUN apt-get update && apt-get install -y python3 python3-pip

COPY --chmod=755 start.py /usr/src/start.py
RUN rm -f /etc/nginx/conf.d/default.conf

EXPOSE 443

VOLUME /domaindispatcher
WORKDIR /domaindispatcher

STOPSIGNAL SIGTERM

ENTRYPOINT [ "python3", "/usr/src/start.py" ]