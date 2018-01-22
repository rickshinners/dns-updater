FROM python:alpine
RUN pip install \
        awscli \
        ipgetter
COPY files/update-dns.sh /update-dns.sh
COPY files/update-route53.py /update-route53.py
RUN chmod a+x /update-dns.sh /update-route53.py
VOLUME /config
CMD [ "/update-dns.sh" ]