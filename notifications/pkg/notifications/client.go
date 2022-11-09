package notifications

import (
	"log"
	"time"

	"github.com/gorilla/websocket"
)

type Client struct {
	Token string
	Conn  *websocket.Conn
	hub   *Hub
}

type SentNotification struct {
	Text  string    `json:"text"`
	Image string    `json:"image"`
	Time  time.Time `json:"time"`
}

func (c *Client) SendNotification(notification *SentNotification) {
	defer func() {
		c.hub.unregister <- c
		c.Conn.Close()
	}()
	connectionErr := c.Conn.WriteJSON(notification)
	if connectionErr != nil {
		log.Println("write:", connectionErr)
	}
}
