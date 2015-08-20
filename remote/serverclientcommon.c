/** serverclientcommon.c

   Curriculum ViTeX
   (C) 2015 Muhammad Khan

   This software is licensed under the MIT Public License

   This file contains implementations of the commonalities
   specified in 'serverclientcommon.h'.

 */
#include <math.h>
#include <string.h>

#include "serverclientcommon.h"
#include "utils.h"

unsigned int bytes_to_send(int tbs, int max, int tb2s){
  int diff = tb2s - tbs;
  return fmin(diff, max);
}

int blob_generate(struct blob* blob, const char* unpadded_fname){
  int i;
  FILE* f;
  char* unpadded_stripped;
  long f_size;
  unpadded_stripped = strip_extra_dirs(unpadded_fname);
  if(unpadded_stripped == NULL)
    return -1;
  memset(blob->padded_fname, '\0', BUFFER_SIZE);
  for(i = 0; i < BUFFER_SIZE; i++){
    if(i < strlen(unpadded_fname))
      blob->padded_fname[i] = unpadded_fname[i];
    else
      blob->padded_fname[i] = PADDING_CHAR;
  }
  f = fopen(unpadded_stripped, "r");
  fseek(f, 0, SEEK_END);
  f_size = ftell(f);
  rewind(f);
  fgets(blob->file_data, (int)f_size, f);
  return 0;
}

char* pad(char* unpadded){
  char* padded;
  int unpadded_len, i;
  unpadded_len = strlen(unpadded);
  if(unpadded_len > BUFFER_SIZE)
    error_and_quit("Filename is too long to pad");
  memset(padded, '\0', BUFFER_SIZE);
  for(i = 0; i < BUFFER_SIZE; i++){
    if(i < unpadded_len)
      padded[i] = unpadded[i];
    else
      padded[i] = PADDING_CHAR;
  }
  return padded;
}

char* unpad(char* padded){
  if(strlen(padded) != BUFFER_SIZE)
    error_and_quit("String to unpad is not of proper size");
  char* unpadded, *iter;
  unpadded = "";
  for(iter = padded; *iter != PADDING_CHAR; ++iter){
    strncat(unpadded, iter, 1);
  }
  return unpadded;
}
