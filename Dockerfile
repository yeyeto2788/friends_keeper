# Base image to use
FROM python:3.9-buster
# Copy applciation files
COPY ./ /friends_keeper/
WORKDIR /friends_keeper

# Install dependecies and package
RUN pip3 install poetry && \
    poetry install --no-dev

ENTRYPOINT [ "poetry", "run", "friends_keeper" ]