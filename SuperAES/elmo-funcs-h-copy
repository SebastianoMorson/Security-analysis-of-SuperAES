#ifndef ELMO_FUNCS_H_
#define ELMO_FUNCS_H_

#include <stdint.h>

// ELMO specific functions

//! @brief Start recording execution from this point onwards, until a
//! pause_trigger()
//! occurs.
void start_trigger() { asm volatile("SVC 1"); }

//! @brief Pause recording execution from this point onwards, until a
//! start_trigger() occurs.
void pause_trigger() { asm volatile("SVC 0"); }

//! @brief Gets a random value.
//! @todo: FixMe: Unverified: This probably currently takes the first byte of 16
//! random 16 byte numbers instead of 1 16 byte number. See line ~300 in
//! thumb-sim memory.cpp
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

#endif // ELMO_FUNCS_H_
