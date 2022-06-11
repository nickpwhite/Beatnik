FROM ruby:2.7.6

ENV DEBIAN_FRONTEND noninteractive

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg -o /root/yarn-pubkey.gpg && apt-key add /root/yarn-pubkey.gpg
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list

RUN apt update && apt install -y firefox-esr xvfb
RUN apt install -y --no-install-recommends nodejs yarn

WORKDIR /opt
RUN curl -L "https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=en-US" | tar -jx
RUN ln -s /opt/firefox/firefox /bin/firefox

WORKDIR /beatnik
COPY . /beatnik
RUN bundle install
RUN yarn install
RUN bin/webpack

ENTRYPOINT ["bundle", "exec", "rails", "server", "-b", "0.0.0.0"]
