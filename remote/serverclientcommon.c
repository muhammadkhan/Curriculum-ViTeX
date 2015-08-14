/** serverclientcommon.c

   Curriculum ViTeX
   (C) 2015 Muhammad Khan

   This software is licensed under the MIT Public License

   This file contains implementations of the commonalities
   specified in 'serverclientcommon.h'.

 */
#include <math.h>

#include "serverclientcommon.h"

unsigned int bytes_to_send(int tbs, int max, int tb2s){
  int diff = tb2s - tbs;
  return fmin(diff, max);
}
