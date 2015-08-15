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
}
