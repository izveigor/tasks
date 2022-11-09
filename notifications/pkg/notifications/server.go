package notifications

import (
	"context"
	"net"
	"sync"
	"time"

	"github.com/izveigor/tasks/notifications/pkg/notifications/pb"
	"google.golang.org/grpc"
)

type server struct {
	pb.UnimplementedNotificationsServer
}

func containToken(token string, tokens []string) bool {
	for _, tokenInArray := range tokens {
		if token == tokenInArray {
			return true
		}
	}
	return false
}

func (s *server) Notify(ctx context.Context, in *pb.NotificationRequest) (*pb.NotificationResponse, error) {
	var text string = in.GetText()
	var time time.Time = in.GetTime().AsTime()
	var image string = in.GetImage()

	notification := Notification{
		Image:  image,
		Text:   text,
		Time:   time,
		Tokens: in.GetTokens(),
	}
	sentNotification := SentNotification{
		Image: image,
		Text:  text,
		Time:  time,
	}

	AddNotification(notification)
	var wg sync.WaitGroup
	for client, _ := range hub.Clients {
		if containToken(client.Token, notification.Tokens) {
			wg.Add(1)
			go client.SendNotification(&sentNotification)
		}
	}
	wg.Wait()

	return &pb.NotificationResponse{}, nil
}

func InitNotificationsServiceServer(address string) {
	lis, err := net.Listen("tcp", address)
	if err != nil {
		panic(err)
	}

	s := grpc.NewServer()
	pb.RegisterNotificationsServer(s, &server{})
	if err := s.Serve(lis); err != nil {
		panic(err)
	}
}
