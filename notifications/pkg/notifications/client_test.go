package notifications

import (
	"encoding/json"
	"github.com/gorilla/websocket"
	"github.com/stretchr/testify/assert"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

func TestSendNotification(t *testing.T) {
	go hub.run()
	getTokenByAuthorization = func(authorization string) string {
		return "1111"
	}

	s := httptest.NewServer(http.HandlerFunc(WSNotify))

	url := "ws" + strings.TrimPrefix(s.URL, "http") + "/ws/notify"
	var notification = &SentNotification{
		Text:  "Важно! Это уведомление 1.",
		Image: "image1",
		Time:  time.Date(2009, time.November, 10, 23, 0, 10, 0, time.UTC),
	}

	ws, _, err := websocket.DefaultDialer.Dial(url, nil)
	time.Sleep(time.Millisecond * 1000)
	if err != nil {
		t.Fatal(err)
	}
	defer func() {
		getTokenByAuthorization = getTokenByAuthorizationFunction
		hub.Clients = map[*Client]bool{}
		s.Close()
		ws.Close()
	}()

	for client, _ := range hub.Clients {
		client.SendNotification(notification)
	}

	_, p, err := ws.ReadMessage()
	if err != nil {
		t.Fatal(err)
	}

	result := SentNotification{}
	err = json.Unmarshal(p, &result)
	if err != nil {
		t.Fatal(err)
	}
	assert.Equal(t, notification, &result)
}
