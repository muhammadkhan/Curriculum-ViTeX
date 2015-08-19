CC=gcc
COMMON_SRC = utils.c serverclientcommon.c
SERVER_SRC = remotecompile_server.c
CLIENT_SRC = remotecompile_client.c

all: server client

server: $(COMMON_SRC) $(SERVER_SRC)
	$(CC) -o $@ $^

client: $(COMMON_SRC) $(CLIENT_SRC)
	$(CC) -o $@ $^

.PHONY: all clean

clean:
	rm -f *.o
	rm -f server
	rm -f client
