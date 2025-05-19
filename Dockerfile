FROM python:3.13-alpine
WORKDIR /app
COPY . .
RUN make mig