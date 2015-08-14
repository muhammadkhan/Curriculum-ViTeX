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
#include "utils.h"

#define SERVER_QUEUE_LIMIT 5
#define DUMP_BASE_DIR "tmp/cvitex/"
#define PDF_EXTENSION ".pdf"

void socket_init(struct sockaddr_in* sock, unsigned short port){
  memset(sock, 0, sizeof(*sock));
  sock->sin_family = AF_INET;
  sock->sin_addr_s_addr = htonl(INADDR_ANY);
  sock->sin_port = htons(port);
}

FILE* write_and_compile_dump(const char* data_dump, int* err_code){
  struct blob* tex_blob;
  char* unpadded_fname, *iter, *full_fname, *pdflatex;
  FILE* f;
  if(data_dump == NULL){
    perror("dat null dump");
    *err_code = -1;
    return NULL;
  }
  unpadded_fname = "";
  tex_blob = (struct blob*)data_dump;
  for(iter = tex_blob->padded_fname; *iter != PADDING_CHAR; ++iter)
    strncat(unpadded_fname, iter, 1); //write byte-by-byte
  full_fname = DUMP_BASE_DIR;
  strcat(full_fname, unpadded_fname);
  f = fopen(full_fname, "w");
  if(f == NULL){
    perror("Could not save incoming file to server space");
    *err_code = -1;
    return NULL;
  }
  fprintf(f, tex_blob->file_data);
  sprintf(pdflatex, "pdflatex %s", full_fname);
  *err_code = system(pdflatex);
  str_replace_last(full_fname, PDF_EXTENSION);
  return fopen(full_fname,"r");
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
    int child_socket_fd, client_length, compile_exit_status;
    struct sockaddr_in clientaddress;
    struct hostent* client_host_info;
    char* client_host_address;
    char client_msg_buf[BUFFER_SIZE], pdf_file_buf[BUFFER_SIZE];
    int bytes_read, total_bytes_sent;
    char* data_dump;
    FILE* pdf_file;
    long pdf_file_size;
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
    memset(client_msg_buf, sizeof(client_msg_buf));

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
      pdf_file = write_and_compile_dump(data_dump, &compile_exit_status);
      if(pdf_file == NULL){
	char* err_msg;
	sprintf(err_msg, "Unable to successfully compile into PDF. Exit status: %d\n", compile_exit_status);
	error_and_quit(err_msg);
      }
      /* now just send the PDF file back to the client */
      fseek(pdf_file, 0, SEEK_END);
      pdf_file_size = ftell(pdf_file);
      rewind(pdf_file);
      memset(pdf_file_buf, pdf_file_size);
      bytes_read = fread((void*)pdf_file_buf, pdf_file_size, 1, pdf_file);
      if(bytes_read != pdf_file_size)
	error_and_quit("Error reading PDF file bytestream\n");
      total_bytes_sent = 0;
      memset(client_msg_buf, sizeof(client_msg_buf));
      while(total_bytes_sent < pdf_file_size){
	int bytes_sent;
	bytes_sent = write(child_socket_fd, client_msg_buf,
			   bytes_to_send(total_bytes_sent,
					 BUFFER_SIZE,
					 pdf_file_size));
	total_bytes_sent += bytes_sent;
      }
    }
    printf("Finished entire transaction with client @ %d\n", client_socket_fd);
    close(child_socket_fd);
  }
  return 0;
}
