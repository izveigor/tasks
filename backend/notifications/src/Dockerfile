FROM golang:1.19
WORKDIR /home/app/tasks/notifications

ENV GO111MODULE=on

COPY go.mod go.sum ./
RUN go mod download && go mod verify

COPY . .
RUN go build -o notifications cmd/main.go