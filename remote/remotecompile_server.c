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

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/socket.h>

#define BUFFER_SIZE 2048
#define SERVER_QUEUE_LIMIT 7

void error_and_quit(const char* err){
  perror(err);
  exit(1);
}

void socket_init(struct sockaddr_in* sock, unsigned short port){
  memset(sock, 0, sizeof(*sock));
  sock->sin_family = AF_INET;
  sock->sin_addr_s_addr = htonl(INADDR_ANY);
  sock->sin_port = htons(port;
}

int main(int argc, char** argv){
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
    int child_socket_fd;
    struct sockaddr_in clientaddress;
    
  }
}
