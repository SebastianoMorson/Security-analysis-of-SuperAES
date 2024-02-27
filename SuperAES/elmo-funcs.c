#include "elmo-funcs.h"
#include <stdint.h>

void start_trigger() {asm volatile("SVC 1");}

void pause_trigger() {asm volatile("SVC 0");}

uint32_t get_rand() {
  char *address = (char *)0xfffff100;
  return *address | (uint32_t)((*address + 8) << 8) |
         (uint32_t)((*address + 16) << 16) | (uint32_t)((*address + 24) << 24);
}

void add_byte_to_trace(uint8_t p_data) {
  // Get the memory address and write p_data to it.
  int volatile *const address = (int *)0xfffff000;
  *address = p_data;
}

void add_to_trace(uint8_t p_data[], uint8_t p_length) {
  for (uint8_t i = 0; i < p_length; ++i) {
    add_byte_to_trace(p_data[i]);
  }
}