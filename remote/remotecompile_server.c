/** remotecompile_server.c
    usage: 'server <port-number>'

   Curriculum ViTeX
   (C) 2015 Muhammad Khan

   This software is licensed under the MIT Public License

   PROTOCOL: TCP/IP

   This file contains the code that should run on a server machine
   that is able to compile using 'pdflatex'. The client shall establish
   a connection if the client machine does not have pdflatex, and will send
   the .tex file. Server should send back the pdf file once and destroy
   local copy of the tex file.

 */

#include <errno.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#include "serverclientcommon.h"

#define SERVER_QUEUE_LIMIT 5

void error_and_quit(const char* err){
  perror(err);
  exit(1);
}

void socket_init(struct sockaddr_in* sock, unsigned short port){
  memset(sock, 0, sizeof(*sock));
  sock->sin_family = AF_INET;
  sock->sin_addr_s_addr = htonl(INADDR_ANY);
  sock->sin_port = htons(port);
}

struct tex_blob {
  char padded_fname[BUFFER_SIZE];
  char* file_data;
};

int write_dump(const char* data_dump){
  
}

int main(int argc, char** argv) {
  int parent_socket_fd;
  int optval;
  struct sockaddr_in serveraddress;
  //check if port number was supplied
  if(argc != 2)
    error_and_quit("Need to supply port number");
  port = atoi(argv[1]);
  parent_socket_fd = socket(AF_INET, SOCK_STREAM, 0);
  if(parent_socket_fd < 0){
    char* socket_error_msg;
    if(sprintf(socket_error_msg, "Could not open socket on port %d\n", port) < 0)
      socket_error_msg = "Problem opening socket on specified port";
    error_and_quit(socket_error_msg);
  }
  optval = 1;
  setsockopt(parent_socket_fd, SQL_SOCKET,
	     SO_REUSEADDR, (const void*)&optval, sizeof(int));
  socket_init(&structaddress, (unsigned short)port);
  if(bind(parent_socket_fd, ()&serveraddress, sizeof(serveraddress)) < 0)
    error_and_quit("Couldn't bind socket");
  if(listen(parent_socket_fd, SERVER_QUEUE_LIMIT) < 0)
    error_and_quit("Socket unable to begin listening");

  /*now we can actually start the main loop */
  while(1){
    int child_socket_fd, client_length;
    struct sockaddr_in clientaddress;
    struct hostent* client_host_info;
    char* client_host_address;
    char client_msg_buf[BUFFER_SIZE];
    int bytes_read;
    char* data_dump;
    client_length = sizeof(clientaddress);
    child_socket_fd = accept(parent_socket_fd,
			     (struct sockaddr_in*)&clientaddr,
			     &client_length);
    if(child_socket_fd < 0)
      error_and_quit("Server unable to accept connection from client");
    client_host_info = gethostbyaddr((const char*)&clientaddress.sin_addr.s_addr,
				     sizeof(clientaddress.sin_addr.s_addr),
				     AF_INET);
    if(client_host_info == NULL)
      error_and_quit("Server unable to obtain client host");
    client_host_address = inet_ntoa(clientaddress.sin_addr);
    if(client_host_address == NULL)
      error_and_quit("Couldn't convert to dotted-decimal string");
    printf("SERVER HAS ESTABLISHED CONNECTION WITH %s (%s)\n",
	   client_host_info->h_name,
	   client_host_address);
    memset(client_msg_buf, BUFFER_SIZE);

    /*
     * One major assumption of this connection is that
     * if the client sends a full buffer, then there is actually
     * more data coming, so we loop the reads. When the buffer
     * is not full, then the client has finished.
     *
     * TODO: try to do this without blocking
     */
    data_dump = "";
    do{
      bytes_read = read(child_socket_fd, client_msg_buf, BUFFER_SIZE);
      if(bytes_read < 0)
	error_and_quit("Server unable to read message from socket");
      printf("SERVER HAS RECEIVED %d bytes\n", bytes_read);

      if(bytes_read > 0)
	strcat(data_dump, client_msg_buf);
    } while(bytes_read == BUFFER_SIZE);
    if(strlen(data_dump) > 0){
      /* now let's actually do something with all this */
      if(write_dump(data_dump) < 0)
	error_and_quit("Unable to successfully compile into PDF - aborting");
    }
    close(child_socket_fd);
  }
  return 0;
}
