package notifications

import (
	"context"
	"log"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	"github.com/izveigor/tasks/notifications/pkg/config"
)

const MAX_NOTIFICATIONS = 3

type Notification struct {
	Text   string    `bson:"text"`
	Time   time.Time `bson:"time"`
	Image  string    `bson:"image"`
	Tokens []string  `bson:"tokens"`
}

type TokenUnread struct {
	Token  string `bson:"token"`
	Number int    `bson:"number"`
}

var notificationsCollection *mongo.Collection
var tokensCollection *mongo.Collection

func ConnectToMongo() {
	client, err := mongo.NewClient(options.Client().ApplyURI(config.Config.MongoUrl))
	if err != nil {
		log.Fatal(err)
	}

	err = client.Connect(context.TODO())
	if err != nil {
		log.Fatal(err)
	}

	notificationsCollection = client.Database("notify").Collection("notifications")
	tokensCollection = client.Database("notify").Collection("tokens")
}

func AddNotificationFunction(notification Notification) {
	insertResult, err := notificationsCollection.InsertOne(context.TODO(), notification)
	if err != nil {
		log.Fatal(err)
	}

	for _, token := range notification.Tokens {
		findFilter := bson.D{{"token", token}}

		var found TokenUnread
		findErr := tokensCollection.FindOne(context.TODO(), findFilter).Decode(&found)

		if findErr != nil {
			if findErr == mongo.ErrNoDocuments {
				createdToken := TokenUnread{
					Token:  token,
					Number: 1,
				}
				_, insertErr := tokensCollection.InsertOne(context.TODO(), createdToken)
				if insertErr != nil {
					log.Fatal(insertErr)
				}
			} else {
				log.Fatal(findErr)
			}
		} else {
			if found.Number != 9 {
				updateFilter := bson.D{{"token", token}}

				update := bson.D{
					{"$inc", bson.D{
						{"number", 1},
					}},
				}

				_, updateErr := tokensCollection.UpdateOne(context.TODO(), updateFilter, update)
				if updateErr != nil {
					log.Fatal(updateErr)
				}
			}
		}
	}
}

func GetNumberUnreadNotificationsFunction(token string) int {
	findFilter := bson.D{{"token", token}}

	var found TokenUnread
	findErr := tokensCollection.FindOne(context.TODO(), findFilter).Decode(&found)

	if findErr != nil {
		return 0
	}

	return found.Number
}

func ClearUnreadNotificationsFunction(token string) {
	tokenFilter := bson.D{{"token", token}}

	update := bson.D{
		{"$set", bson.D{
			{"number", 0},
		}},
	}

	_, err := tokensCollection.UpdateOne(context.TODO(), tokenFilter, update)
	if err != nil {
		log.Fatal(err)
	}
}

func GetLastNotificationsFunction(token string) []*Notification {
	var notifications []*Notification
	filter := bson.D{{"tokens", token}}

	optionsFind := options.Find()
	optionsFind.SetLimit(MAX_NOTIFICATIONS)
	optionsFind.SetSort(bson.D{{"time", -1}})

	cursor, err := notificationsCollection.Find(context.TODO(), filter, optionsFind)
	if err != nil {
		return []*Notification{}
	}

	for cursor.Next(context.TODO()) {
		var element Notification
		err := cursor.Decode(&element)
		if err != nil {
			log.Fatal(err)
		}

		notifications = append(notifications, &element)
	}

	if err := cursor.Err(); err != nil {
		log.Fatal(err)
	}

	cursor.Close(context.TODO())
	return notifications
}

var ClearUnreadNotifications = ClearUnreadNotificationsFunction
var GetNumberUnreadNotifications = GetNumberUnreadNotificationsFunction
var AddNotification = AddNotificationFunction
var GetLastNotifications = GetLastNotificationsFunction
