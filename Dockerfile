FROM python:alpine
RUN pip install \
        awscli \
        ipgetter2 \
        crontab \
        netaddr
COPY update-dns.py /update-dns.py
ENV PYTHONUNBUFFERED 1
RUN chmod a+x /update-dns.py
CMD [ "/update-dns.py" ]