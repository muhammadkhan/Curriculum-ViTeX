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
		     - a function that decides the appropriate amount
		       of expected bytes to send

 */

#ifndef _SERVERCLIENTCOMMON_H
#define _SERVERCLIENTCOMMON_H

#define BUFFER_SIZE 2048
#define PADDING_CHAR '#'

struct blob{
  char padded_fname[BUFFER_SIZE];
  char* file_data;
};

/**
 * Determines the appropriate number of bytes that should be sent
 *
 * @param total_bytes_sent an integer describing the number of bytes
 *                         that have already been sent prior to this
 *                         invocation of the function
 *
 * @param maximum_sendable an integer describing the maximum allowable
 *                         number of bytes that can be sent at one time
 *
 * @param total_bytes_to_send the number of bytes that are to be sent
                              in total
 */
unsigned int bytes_to_send(int total_bytes_sent,
			   int maximum_sendable,
			   int total_bytes_to_send);

#endif /* _SERVERCLIENTCOMMON_H */
