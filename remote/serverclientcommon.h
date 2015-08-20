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
		     - routines to pad/unpad

 */

#ifndef _SERVERCLIENTCOMMON_H
#define _SERVERCLIENTCOMMON_H

#define BUFFER_SIZE 2048
#define PADDING_CHAR '#'
#define PDF_EXTENSION ".pdf"

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
 *                            in total
 *
 * @return the number of bytes actually sent during this particular
 *         invocation
 */
unsigned int bytes_to_send(int total_bytes_sent,
			   int maximum_sendable,
			   int total_bytes_to_send);

/**
 * Creates a 'blob' by passing in the raw file name. Adds padding
 * and loads the file's data also. Modifies the first argument by
 * loading it with this information. Returns a negative number in
 * the case of failure.
 *
 * @param blob A pointer to the blob struct to be filled
 *
 * @param unpadded_fname the raw (unpadded) file name for which
 *                       to generate a blob
 *
 * @return a negative number in the case of failure, or a non-zero
 *         number otherwise
 */
int blob_generate(struct blob* blob, const char* unpadded_fname);

/**
 * Returns a new padded version of the input string of
 * length 'BUFFER_SIZE', with
 * 'PADDING_CHAR' used for the padding
 *
 * @param unpadded the original string to be padded
 *
 * @return a separate string of length 'BUFFER_SIZE' with
 *         a padded tail of 'PADDING_CHAR' characters
 */
char* pad(char* unpadded);

/**
 * Returns a new string that has been stripped of all padding.
 * Throws an error if the input string is not of length
 * 'BUFFER_SIZE'.
 *
 * @param padded a string of length 'BUFFER_SIZE' expected to
 *               have a trail of 'PADDING_CHAR' characters at its
 *               tail
 *
 * @return a string stripped of the padding, or throws an error if
 *         the inut was not of appropriate size
 */
char* unpad(char* padded);

#endif /* _SERVERCLIENTCOMMON_H */
