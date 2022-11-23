package notifications

import (
	"context"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"go.mongodb.org/mongo-driver/bson"
)

func TestAddNotification(t *testing.T) {
	defer func() {
		notificationsCollection.Drop(context.TODO())
		tokensCollection.Drop(context.TODO())
	}()
	ConnectToMongo()

	notification := Notification{
		Image:  "image",
		Text:   "Внимание!",
		Time:   time.Date(2009, time.November, 10, 23, 0, 10, 0, time.UTC),
		Tokens: []string{"a", "b"},
	}

	AddNotification(notification)

	notificationsFilter := bson.D{{"text", "Внимание!"}}
	var notificationsResult Notification
	notificationsErr := notificationsCollection.FindOne(context.TODO(), notificationsFilter).Decode(&notificationsResult)
	if notificationsErr != nil {
		t.Fatal(notificationsErr)
	}

	tokensFilter := bson.D{{"token", "a"}}
	var tokensResult TokenUnread
	tokensErr := tokensCollection.FindOne(context.TODO(), tokensFilter).Decode(&tokensResult)
	if tokensErr != nil {
		t.Fatal(tokensErr)
	}

	assert.Equal(t, tokensResult.Number, 1)
	assert.Equal(t, notification, notificationsResult)
}

func TestGetLastNotifications(t *testing.T) {
	defer func() {
		notificationsCollection.Drop(context.TODO())
		tokensCollection.Drop(context.TODO())
	}()

	ConnectToMongo()
	first_notification := Notification{
		Image:  "image1",
		Text:   "Внимание! Сообщение 1.",
		Time:   time.Date(2009, time.November, 10, 23, 0, 10, 0, time.UTC),
		Tokens: []string{"a", "b"},
	}
	second_notification := Notification{
		Image:  "image2",
		Text:   "Внимание! Сообщение 2.",
		Time:   time.Date(2009, time.November, 10, 23, 0, 20, 0, time.UTC),
		Tokens: []string{"a", "c"},
	}
	third_notification := Notification{
		Image:  "image3",
		Text:   "Внимание! Сообщение 3.",
		Time:   time.Date(2009, time.November, 10, 23, 0, 30, 0, time.UTC),
		Tokens: []string{"a", "b", "d"},
	}
	fourth_notification := Notification{
		Image:  "image4",
		Text:   "Внимание! Сообщение 4.",
		Time:   time.Date(2009, time.November, 10, 23, 0, 40, 0, time.UTC),
		Tokens: []string{"c", "b"},
	}
	fifth_notification := Notification{
		Image:  "image5",
		Text:   "Внимание! Сообщение 5.",
		Time:   time.Date(2009, time.November, 10, 23, 0, 50, 0, time.UTC),
		Tokens: []string{"a", "b"},
	}

	notifications := []interface{}{
		first_notification,
		second_notification,
		third_notification,
		fourth_notification,
		fifth_notification,
	}

	if _, err := notificationsCollection.InsertMany(context.TODO(), notifications); err != nil {
		t.Fatal(err)
	}

	right_notifications := []Notification{
		fifth_notification,
		third_notification,
		second_notification,
	}

	last_notifications := GetLastNotifications("a")

	for i := 0; i < len(last_notifications); i++ {
		assert.Equal(t, last_notifications[i], &right_notifications[i])
	}
}

func TestGetAndClearNumberUnreadNotifications(t *testing.T) {
	defer func() {
		notificationsCollection.Drop(context.TODO())
		tokensCollection.Drop(context.TODO())
	}()

	ConnectToMongo()

	first_notification := Notification{
		Image:  "image1",
		Text:   "Внимание! Сообщение 1.",
		Time:   time.Date(2009, time.November, 10, 23, 0, 10, 0, time.UTC),
		Tokens: []string{"a", "b"},
	}
	second_notification := Notification{
		Image:  "image2",
		Text:   "Внимание! Сообщение 2.",
		Time:   time.Date(2009, time.November, 10, 23, 0, 20, 0, time.UTC),
		Tokens: []string{"a", "c"},
	}
	third_notification := Notification{
		Image:  "image3",
		Text:   "Внимание! Сообщение 3.",
		Time:   time.Date(2009, time.November, 10, 23, 0, 30, 0, time.UTC),
		Tokens: []string{"a", "b", "d"},
	}

	AddNotification(first_notification)
	AddNotification(second_notification)
	AddNotification(third_notification)

	assert.Equal(t, GetNumberUnreadNotifications("a"), 3)
	assert.Equal(t, GetNumberUnreadNotifications("b"), 2)
	assert.Equal(t, GetNumberUnreadNotifications("c"), 1)
	assert.Equal(t, GetNumberUnreadNotifications("d"), 1)

	ClearUnreadNotifications("a")
	assert.Equal(t, GetNumberUnreadNotifications("a"), 0)

	ClearUnreadNotifications("b")
	assert.Equal(t, GetNumberUnreadNotifications("b"), 0)

	ClearUnreadNotifications("c")
	assert.Equal(t, GetNumberUnreadNotifications("c"), 0)

	ClearUnreadNotifications("d")
	assert.Equal(t, GetNumberUnreadNotifications("d"), 0)
}
