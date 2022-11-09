package notifications

import (
	"context"
	"github.com/izveigor/tasks/notifications/pkg/notifications/pb"
	"github.com/stretchr/testify/assert"
	"google.golang.org/grpc"
	"google.golang.org/protobuf/types/known/timestamppb"
	"testing"
	"time"
)

func TestNotify(t *testing.T) {
	var address string = "localhost:50054"
	go InitNotificationsServiceServer(address)
	time.Sleep(1250)

	conn, err := grpc.Dial(address, grpc.WithInsecure())
	var sentNotification = &Notification{
		Text:   "Важно! Это первое уведомление!",
		Image:  "image1",
		Time:   time.Date(2009, time.November, 10, 23, 0, 10, 0, time.UTC),
		Tokens: []string{"a", "b"},
	}

	if err != nil {
		t.Fatal(err)
	}

	defer func() {
		AddNotification = AddNotificationFunction
		conn.Close()
	}()

	AddNotification = func(notification Notification) {
		assert.Equal(t, sentNotification, &notification)
	}

	client := pb.NewNotificationsClient(conn)
	_, err = client.Notify(context.Background(), &pb.NotificationRequest{
		Image:  sentNotification.Image,
		Text:   sentNotification.Text,
		Time:   timestamppb.New(sentNotification.Time),
		Tokens: sentNotification.Tokens,
	})

	if err != nil {
		t.Fatal(err)
	}
}
