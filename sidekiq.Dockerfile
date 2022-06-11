FROM ruby:2.7

ENV DEBIAN_FRONTEND noninteractive

# For firefox dependencies
RUN apt update && apt install -y firefox-esr xvfb

WORKDIR /opt
RUN curl -L "https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=en-US" | tar -jx
RUN ln -s /opt/firefox/firefox /bin/firefox

WORKDIR /beatnik
COPY . /beatnik
RUN bundle install

CMD ["bundle", "exec", "sidekiq"]
