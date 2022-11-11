package notifications

import (
	"context"
	"encoding/json"
	"github.com/stretchr/testify/assert"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

func TestGetTokenByAuthorization(t *testing.T) {
	var authorization string = "Token 11111"
	var token string = getTokenByAuthorization(authorization)
	assert.Equal(t, token, "11111")
}

func TestGetNotifications(t *testing.T) {
	notifications := []*Notification{
		&Notification{
			Image:  "image1",
			Text:   "Внимание! Сообщение 1.",
			Time:   time.Date(2009, time.November, 10, 23, 0, 10, 0, time.UTC),
			Tokens: []string{"a", "b"},
		},
		&Notification{
			Image:  "image2",
			Text:   "Внимание! Сообщение 2.",
			Time:   time.Date(2009, time.November, 10, 23, 0, 20, 0, time.UTC),
			Tokens: []string{"a", "c"},
		},
		&Notification{
			Image:  "image3",
			Text:   "Внимание! Сообщение 3.",
			Time:   time.Date(2009, time.November, 10, 23, 0, 30, 0, time.UTC),
			Tokens: []string{"a", "b", "d"},
		},
	}
	GetLastNotifications = func(token string) []*Notification {
		return notifications
	}
	defer func() {
		GetLastNotifications = GetLastNotificationsFunction
	}()
	wr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	req.Header.Set("Authorization", "Token 111")

	GetNotificationsView(wr, req)
	assert.Equal(t, wr.Code, http.StatusOK)
	var result []*Notification
	if err := json.Unmarshal([]byte(wr.Body.String()), &result); err != nil {
		t.Fatal(err)
	}
	for i := 0; i < len(notifications); i++ {
		assert.Equal(t, result[i].Image, notifications[i].Image)
		assert.Equal(t, result[i].Text, notifications[i].Text)
		assert.Equal(t, result[i].Time, notifications[i].Time)
	}
}

func TestGetAndClearUnreadNotificationsView(t *testing.T) {
	defer func() {
		notificationsCollection.Drop(context.TODO())
		tokensCollection.Drop(context.TODO())
	}()

	notifications := []*Notification{
		&Notification{
			Image:  "image1",
			Text:   "Внимание! Сообщение 1.",
			Time:   time.Date(2009, time.November, 10, 23, 0, 10, 0, time.UTC),
			Tokens: []string{"a", "b"},
		},
		&Notification{
			Image:  "image2",
			Text:   "Внимание! Сообщение 2.",
			Time:   time.Date(2009, time.November, 10, 23, 0, 20, 0, time.UTC),
			Tokens: []string{"a", "c"},
		},
		&Notification{
			Image:  "image3",
			Text:   "Внимание! Сообщение 3.",
			Time:   time.Date(2009, time.November, 10, 23, 0, 30, 0, time.UTC),
			Tokens: []string{"a", "b", "d"},
		},
	}
	for _, notification := range notifications {
		AddNotification(*notification)
	}

	wr := httptest.NewRecorder()
	req := httptest.NewRequest(http.MethodGet, "/", nil)
	req.Header.Set("Authorization", "Token a")

	GetNumberUnreadNotificationsView(wr, req)

	assert.Equal(t, wr.Code, http.StatusOK)
	var number int
	if err := json.Unmarshal([]byte(wr.Body.String()), &number); err != nil {
		t.Fatal(err)
	}
	assert.Equal(t, number, 3)

	clearWr := httptest.NewRecorder()
	clearReq := httptest.NewRequest(http.MethodGet, "/", nil)
	clearReq.Header.Set("Authorization", "Token a")

	ClearUnreadNotificationsView(clearWr, clearReq)
	assert.Equal(t, clearWr.Code, http.StatusOK)

	getWr := httptest.NewRecorder()
	getReq := httptest.NewRequest(http.MethodGet, "/", nil)
	getReq.Header.Set("Authorization", "Token a")

	var clearerNumber int
	GetNumberUnreadNotificationsView(getWr, getReq)
	assert.Equal(t, getWr.Code, http.StatusOK)
	if err := json.Unmarshal([]byte(getWr.Body.String()), &clearerNumber); err != nil {
		t.Fatal(err)
	}
	assert.Equal(t, clearerNumber, 0)
}
