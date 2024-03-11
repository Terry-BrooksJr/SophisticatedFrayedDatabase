FROM python:3.11

ENV PYTHONUNBUFFERED=1
ENV PYTHON_VERSION=3.11.2
WORKDIR /src/app/
 
EXPOSE 8080/tcp

RUN apt-get update && \
    apt-get upgrade --yes 

# Install Doppler CLI
RUN apt-get install -y apt-transport-https ca-certificates curl gnupg && \
    curl -sLf --retry 3 --tlsv1.2 --proto "=https" 'https://packages.doppler.com/public/cli/gpg.DE2A7741A397C129.key' | gpg --dearmor -o /usr/share/keyrings/doppler-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/doppler-archive-keyring.gpg] https://packages.doppler.com/public/cli/deb/debian any-version main" | tee /etc/apt/sources.list.d/doppler-cli.list && \
    apt-get update && \
    apt-get -y install doppler

RUN useradd --create-home report

COPY --chown=report requirements.txt /requirements.txt


# Copy the rest of the project's files (excluding those in a subdirectory named tests) into the container’s /src
COPY --chown=report app/report_server.py /src/app/report_server.py
COPY --chown=report app/utils.py /src/app/utils.py
COPY --chown=report app/__init__.py /src/app/__init__.py 
RUN chmod +x  /src/app/report_server.py

ARG DOPPLER_TOKEN=dp.pt.lClrNKFjRCZNt0NEQNFG8TYKeLnY2PdtVFByf9EYVjY
ARG DOPPLER_CONFIG=dev_personal
ARG DOPPLER_ENVIRONMENT=dev
ARG DOPPLER_PROJECT=feature-report
RUN doppler secrets get CA_PRIVATE_KEY --plain > /src/ca-private.pem
RUN doppler secrets get CA_PUBLIC_CERT --plain > /src/ca-public.pem

USER report
RUN   pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir -Ur /requirements.txt


ENTRYPOINT ["doppler", "run", "--"]
CMD ["/src/app/report_server.py"]

 