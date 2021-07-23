// protoc --proto_path=./../ --go_out=paths=source_relative --go_opt=paths=source_relative --go-grpc_out=. --go-grpc_opt=paths=source_relative hashtable.proto

package main

import (
	"context"
	"log"
	"os"
	"time"

	"google.golang.org/grpc"
	pb "./client_go"
)

const (
	address     = "localhost:50051"
	defaultName = "hashtable"
)

func main() {
	// Set up a connection to the server.
	conn, err := grpc.Dial(address, grpc.WithInsecure(), grpc.WithBlock())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	c := pb.NewHashtableClient(conn)

	// Contact the server and print out its response.
	name := defaultName
	if len(os.Args) > 1 {
		name = os.Args[1]
	}
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	r, err := c.Put(ctx, &pb.Put{key: "5", value: 5})
	log.Printf("Put: %t", r.Ok)

	r, err := c.Get(ctx, &pb.Put{key: "5"})
	log.Printf("Get: %d", r.Value)
}