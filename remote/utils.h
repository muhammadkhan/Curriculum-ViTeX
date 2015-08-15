/** utils.h

   Curriculum ViTeX
   (C) 2015 Muhammad Khan

   This software is licensed under the MIT Public License

   This file contains some functions that are helpful for both
   client and server code, but in general irrelevant to any of the
   processes.

   TL;DR: Just some code to make life easier

 */

#ifndef _UTILS_H
#define _UTILS_H

/**
 * Causes the program to terminate and print
 * the message passed
 * 
 * @param err the message that is to be printed upon
 *            termination of the program
 */
void error_and_quit(const char* err);


/**
 * Replaces the latter portion of 'destination' with
 * the string 'source'. Returns 'source' itself if the
 * length of 'source' is greater than the length of
 * 'destination'.
 *
 * @param destination the string to be modified by replacing
 *                    the last portion with the contents of
 *                    the 'source' string
 *
 * @param source the string which will be used to modify the
 *               'destination' string
 *
 *
 * @return if length of 'source' is greater than that of
 *         'destination', then 'source' is simply returned.
 *         Otherwise, 'destination' is returned, and the input
 *         parameter 'destination' is modified as described above
 */
char* str_replace_last(char* destination, const char* source);

/**
 * Takes a (full) file path and returns only that portion
 * which corresponds to the actual file name, i.e. removes
 * all the prepending directory names.
 *
 * @param fp the full file path to be stripped
 *
 * @return simply the file name portion from the supplied path
 */
char* strip_extra_dirs(const char* fp);

#endif /* _UTILS_H */
