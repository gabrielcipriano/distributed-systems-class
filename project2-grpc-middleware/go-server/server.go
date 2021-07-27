package main

import (
	"context"
	"log"
	"net"

	pb "main/hashtable_pb"

	ht "main/safe_hashtable"

	"google.golang.org/grpc"
)

const (
	port = ":50051"
)

// Hashtable
var hashtable ht.SafeHashtable

// server is used to implement HashtableServer
type server struct {
	pb.UnimplementedHashtableServer
}

// Put implements HashtableServer
func (s *server) Put(ctx context.Context, in *pb.PutRequest) (*pb.PutResponse, error) {
	// log.Printf("Received: %v: %v", in.GetKey(), in.GetValue())
	hashtable.Put(in.GetKey(), in.GetValue())
	ok := true
	return &pb.PutResponse{Ok: &ok}, nil
}

// Put implements HashtableServer
func (s *server) Get(ctx context.Context, in *pb.GetRequest) (*pb.GetResponse, error) {
	// log.Printf("Received: %v", in.GetKey())

	value := hashtable.Get(in.GetKey())
	return &pb.GetResponse{Value: &value}, nil
}

func main() {
	hashtable = ht.SafeHashtable{}
	hashtable.Create()

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
