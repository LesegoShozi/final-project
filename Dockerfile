FROM alpine:latest
WORKDIR /app
COPY hello.txt .
CMD ["cat", "hello.txt"]
