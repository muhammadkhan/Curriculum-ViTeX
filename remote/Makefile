CC=gcc
SERVER_SRC = remotecompile_server.c
CLIENT_SRC = remotecompile_client.c

all: server client

server: $(SERVER_SRC)
	$(CC) -o $@ $^

client: $(CLIENT_SRC)
	$(CC) -o $@ $^

.PHONY: all clean

clean:
	rm -f *.o
	rm -f server
	rm -f client
