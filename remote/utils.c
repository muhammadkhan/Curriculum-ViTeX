/** utils.c

   Curriculum ViTeX
   (C) 2015 Muhammad Khan

   This software is licensed under the MIT Public License

   This file contains implementations of the utility functions
   specified and documented in 'utils.h'

 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "utils.h"

const char path_sep =
  #ifdef _WIN32
  '\\';
  #else
  '/';
  #endif

void error_and_quit(const char* err){
  perror(err);
  exit(1);
}

char* str_replace_last(char* destination, const char* source){
  int src_len, dest_len, i;
  char* dest_copy;
  strcpy(dest_copy, destination);
  src_len = strlen(source);
  dest_len = strlen(destination);
  if(src_len > dest_len)
    return source;
  for(i = 0; i < dest_len; i++){
    if(i >= dest_len - src_len)
      destination[i] = source[i]; //replace
  }
  return dest_copy;
}

char* strip_extra_dirs(const char* fp){
  char* stripped;
  const char* iter;
  stripped = "";
  for(iter = fp; *iter != '\0'; ++iter){
    if(*iter == path_sep)
      stripped = "";
    else
      strncat(stripped, iter, 1);
  }
  return stripped;
}
