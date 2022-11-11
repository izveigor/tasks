proto:
	protoc -I ./pkg/notifications/pb/ --go_out=. --go-grpc_out=. ./pkg/notifications/pb/*.proto

start:
	go run cmd/main.go

test:
	go test -v -cover github.com/izveigor/tasks/notifications/pkg/notifications