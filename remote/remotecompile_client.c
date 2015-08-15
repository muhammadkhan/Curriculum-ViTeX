/** remotecompile_client.c
    usage: 'client <hostname> <port-number> <path/to/tex/file>'

   Curriculum ViTeX
   (C) 2015 Muhammad Khan

   This software is licensed under the MIT Public License

   PROTOCOL: TCP/IP

   This file contains the code that a client should run in order
   to transfer over a .tex file to a server so that it can run
   'pdflatex' and receive a compiled PDF file.

 */

#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#include "serverclientcommon.h"
#include "utils.h"

int main(int argc, char** argv){
  int socket_fd, port;
  char* hostname, texfile_name;
  FILE* texfile;
  struct sockaddr_in serveraddress;
  struct hostent* server_info;
  if(argc != 4)
    error_and_quit("ERROR - usage: %s <hostname> <port-number> <path/to/tex/file>", argv[0]);
  port = atoi(argv[2]);
  hostname = argv[1];
  texfile_name = argv[3];
  socket_fd = socket(AF_INET, SOCK_STREAM, 0);
  if(socket_fd < 0){
    char* err_msg;
    if(sprintf(err_msg, "Failure opening socket on port %d\n", port) < 0)
      err_msg = "Couldn't open socket on specified port";
    error_and_quit(err_msg);
  }
  server_info = gethostbyname(hostname);
  if(server_info == NULL){
    char* err_msg;
    if(sprintf(err_msg, "Error connecting to host '%s'\n", hostname) < 0)
      err_msg = "Couldn't connect to specified host";
    error_and_quit(err_msg);
  }
  memset((char*)&serveraddress, '\0', sizeof(serveraddress));
  serveraddress.sin_family = AF_INET;
  memmove((char*)&serveraddress.sin_addr.s_addr,
	  server_info->h_addr, server_info->h_length);
  serveraddress.sin_port = htons(port);
  if(connect(socket_fd, &serveraddress, sizeof(serveraddress)) < 0)
    error_and_quit("Error establishing connection");
  /* make initial blob */
  struct blob texblob;
  memset(texblob.padded_fname, '\0', BUFFER_SIZE);
}
