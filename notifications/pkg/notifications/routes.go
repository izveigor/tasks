package notifications

import (
	"encoding/json"
	"log"
	"net/http"
	"strings"

	"github.com/gorilla/websocket"
)

func getTokenByAuthorizationFunction(authorization string) string {
	var token string = ""
	var args []string = strings.Split(authorization, " ")
	if args[0] == "Token" {
		token = args[1]
	}
	return token
}

var getTokenByAuthorization = getTokenByAuthorizationFunction

func WSNotify(responseWriter http.ResponseWriter, request *http.Request) {
	var upgrader = websocket.Upgrader{
		ReadBufferSize:  1024,
		WriteBufferSize: 1024,
	}

	connection, err := upgrader.Upgrade(responseWriter, request, nil)
	if err != nil {
		log.Println(err)
		return
	}

	var token string = getTokenByAuthorization(request.Header.Get("Authorization"))
	if token == "" {
		return
	}
	client := &Client{Token: token, Conn: connection, hub: hub}
	client.hub.register <- client
}

func GetNotificationsView(responseWriter http.ResponseWriter, request *http.Request) {
	responseWriter.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
	responseWriter.Header().Set("Access-Control-Allow-Origin", "*")
	var token string = getTokenByAuthorization(request.Header.Get("Authorization"))
	notifications := GetLastNotifications(token)
	sentNotifications := []SentNotification{}
	for _, notification := range notifications {
		sentNotifications = append(sentNotifications, SentNotification{
			Image: notification.Image,
			Text:  notification.Text,
			Time:  notification.Time,
		})
	}

	responseWriter.Header().Set("Content-Type", "application/json")
	responseWriter.WriteHeader(http.StatusOK)
	json.NewEncoder(responseWriter).Encode(sentNotifications)
}

func GetNumberUnreadNotificationsView(responseWriter http.ResponseWriter, request *http.Request) {
	responseWriter.Header().Set("Access-Control-Allow-Origin", "*")
	responseWriter.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
	var token string = getTokenByAuthorization(request.Header.Get("Authorization"))
	number := GetNumberUnreadNotifications(token)

	responseWriter.Header().Set("Content-Type", "application/json")
	responseWriter.WriteHeader(http.StatusOK)
	json.NewEncoder(responseWriter).Encode(number)
}

func ClearUnreadNotificationsView(responseWriter http.ResponseWriter, request *http.Request) {
	responseWriter.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
	responseWriter.Header().Set("Access-Control-Allow-Origin", "*")
	var token string = getTokenByAuthorization(request.Header.Get("Authorization"))
	ClearUnreadNotifications(token)

	responseWriter.WriteHeader(http.StatusOK)
}

func AddRoutes(address string) {
	http.HandleFunc("/notifications/", GetNotificationsView)
	http.HandleFunc("/get_number_unread_notifications/", GetNumberUnreadNotificationsView)
	http.HandleFunc("/clear_unread_notifications/", ClearUnreadNotificationsView)
	http.HandleFunc("/ws/notify/", WSNotify)

	http.ListenAndServe(address, nil)
	log.Println("Маршруты успешно загрузились.")
}
