/** serverclientcommon.h

   Curriculum ViTeX
   (C) 2015 Muhammad Khan

   This software is licensed under the MIT Public License

   This file contains some commonalities shared by both the server
   and client code. 

   Current content includes:
                     - message buffer size
		     - file name padding character
		     - a struct describing the packet protocol

 */

#ifndef _SERVERCLIENTCOMMON_H
#define _SERVERCLIENTCOMMON_H

#define BUFFER_SIZE 2048
#define PADDING_CHAR '#'

struct blob{
  char padded_fname[BUFFER_SIZE];
  char* file_data;
};

#endif /* _SERVERCLIENTCOMMON_H */
