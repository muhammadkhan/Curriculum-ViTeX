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
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#include "serverclientcommon.h"
#include "utils.h"

int main(int argc, char** argv){
  int socket_fd, port;
  char* hostname, *texfile_name;
  FILE* texfile, *pdffile;
  struct sockaddr_in serveraddress;
  struct hostent* server_info;
  struct blob texblob, *pdfblob;
  char* bytewise_blob, *pdf_dump;
  char pdf_buffer[BUFFER_SIZE];
  int total_bytes_tex_sent, pdf_bytes_read;
  if(argc != 4){
    char* msg;
    sprintf(msg, "ERROR - usage: %s <hostname> <port-number> <path/to/tex/file>", argv[0]);
    error_and_quit(msg);
  }
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
  if(connect(socket_fd, (struct sockaddr*)&serveraddress, sizeof(serveraddress)) < 0)
    error_and_quit("Error establishing connection");
  /* make initial blob */
  blob_generate(&texblob, texfile_name);
  bytewise_blob = (char*)&texblob;
  total_bytes_tex_sent = 0;
  while(total_bytes_tex_sent < sizeof(texblob.file_data)){
    int bytes_sent, to_send;
    to_send = bytes_to_send(total_bytes_tex_sent,
			    BUFFER_SIZE,
			    sizeof(texblob.file_data));
    bytes_sent = write(socket_fd, bytewise_blob, to_send);
    total_bytes_tex_sent += bytes_sent;
    bytewise_blob += bytes_sent;
  }
  /* now we're gonna get a pdf back */
  pdf_dump = "";
  pdf_bytes_read = 0;
  memset(pdf_buffer, '\0', BUFFER_SIZE);
  do{
    pdf_bytes_read = read(socket_fd, pdf_buffer, BUFFER_SIZE);
    if(pdf_bytes_read < 0)
      error_and_quit("Client unable to read message from socket");
    printf("CLIENT HAS RECEIVED %d bytes\n", pdf_bytes_read);
    if(pdf_bytes_read > 0)
      strcat(pdf_dump, pdf_buffer);
  } while(pdf_bytes_read == BUFFER_SIZE);
  if(strlen(pdf_dump) <= 0)
    error_and_quit("CLIENT: There was an error reading back the PDF\n");
  pdfblob = (struct blob*)pdf_dump;
  pdffile = fopen(unpad(pdfblob->padded_fname), "w");
  if(pdffile == NULL)
    error_and_quit("CLIENT: Couldn't create appropriate PDF filename from server");
  fwrite(pdf_dump, sizeof(char), pdf_bytes_read, pdffile);
  printf("Successful receipt of PDF from server to client!\n");
  fclose(pdffile);
  close(socket_fd);
  return 0;
}
