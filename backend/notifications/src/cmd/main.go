package main

import (
	"fmt"
	"time"

	"github.com/izveigor/tasks/notifications/pkg/config"
	"github.com/izveigor/tasks/notifications/pkg/notifications"
)

func main() {
	fmt.Println("Сервер был запущен.")
	notifications.ConnectToMongo()
	go notifications.InitNotificationsServiceServer(config.Config.NotificationSvcUrl)
	time.Sleep(time.Millisecond * 2000)
	go notifications.AddRoutes(":8002")
	for {
	}
}
