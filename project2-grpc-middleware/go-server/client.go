// protoc --proto_path=./../ --go_out=paths=source_relative --go_opt=paths=source_relative --go-grpc_out=. --go-grpc_opt=paths=source_relative hashtable.proto

package main

import (
	"context"
	"log"
	"time"

	"math/rand"

	pb "main/hashtable_pb"

	"google.golang.org/grpc"
)

const (
	address     = "localhost:50051"
	defaultName = "hashtable"
)

func run(keys []string, values []int) {
	conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()

	c := pb.NewHashtableClient(conn)

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

}

func main2() {
	rand.Seed(time.Now().UTC().UnixNano())

	n := 1000

	var keys [n]string

	// Set up a connection to the server.
	conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	c := pb.NewHashtableClient(conn)

	// Contact the server and print out its response.
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	var key string = "jesus"
	var value int32 = 6667
	r, _ := c.Put(ctx, &pb.PutRequest{Key: &key, Value: &value})
	log.Printf("Put: %t", r.GetOk())

	rr, _ := c.Get(ctx, &pb.GetRequest{Key: &key})
	log.Printf("Get: %d", rr.GetValue())
}
