package main

import (
	"time"

	"github.com/izveigor/tasks/notifications/pkg/config"
	"github.com/izveigor/tasks/notifications/pkg/notifications"
)

func main() {
	notifications.ConnectToMongo()
	go notifications.InitNotificationsServiceServer(config.Config.NotificationSvcUrl)
	time.Sleep(time.Millisecond * 2000)
	go notifications.AddRoutes(config.Config.Host)
	for {
	}
}
