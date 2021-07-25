// Package main implements a server for Greeter service.
package main

import (
	"context"
	"log"
	"net"

	pb "main/hashtable_pb"

	"google.golang.org/grpc"
)

const (
	port = ":50051"
)

// Hashtable
var hashtable map[string]int32

// server is used to implement HashtableServer
type server struct {
	pb.UnimplementedHashtableServer
}

// Put implements HashtableServer
func (s *server) Put(ctx context.Context, in *pb.PutRequest) (*pb.PutResponse, error) {
	log.Printf("Received: %v: %v", in.GetKey(), in.GetValue())
	hashtable[in.GetKey()] = in.GetValue()
	ok := true
	return &pb.PutResponse{Ok: &ok}, nil
}

// Put implements HashtableServer
func (s *server) Get(ctx context.Context, in *pb.GetRequest) (*pb.GetResponse, error) {
	log.Printf("Received: %v", in.GetKey())
	value := hashtable[in.GetKey()]
	return &pb.GetResponse{Value: &value}, nil
}

func main() {
	hashtable = make(map[string]int32)

	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterHashtableServer(s, &server{})
	log.Printf("server listening at %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
