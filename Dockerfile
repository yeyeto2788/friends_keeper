# Base image to use
FROM python:3.9-buster
# Copy applciation files
COPY ./ /friends_keeper/
WORKDIR /friends_keeper

# Install dependecies and package
# TODO: delete files shown on build
RUN ls -la && \ 
    pip install poetry && \
    poetry install --no-dev

ENTRYPOINT [ "poetry", "run", "friends_keeper" ]