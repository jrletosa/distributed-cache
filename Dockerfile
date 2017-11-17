FROM pypy:2-5.6-slim

# Save image size and build time
RUN set -ex \
	&& apt-get update \
	&& buildDeps='build-essential libffi-dev python-dev' \
	&& apt-get install -y --no-install-recommends git $buildDeps \
	&& rm -rf /var/lib/apt/lists/* \
	&& apt-get purge -y --auto-remove $buildDeps

ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1
CMD ["distributed-cache"]
