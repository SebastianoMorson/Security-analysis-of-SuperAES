#ifndef ELMO_FUNCS_H
#define ELMO_FUNCS_H
// ELMO specific functions
#include <stdint.h>
//! @brief Start recording execution from this point onwards, until a
//! pause_trigger()
//! occurs.
void start_trigger();

//! @brief Pause recording execution from this point onwards, until a
//! start_trigger() occurs.
void pause_trigger();

//! @brief Gets a random value.
//! @todo: FixMe: Unverified: This probably currently takes the first byte of 16
//! random 16 byte numbers instead of 1 16 byte number. See line ~300 in
//! thumb-sim memory.cpp
uint32_t get_rand();

void add_byte_to_trace(uint8_t p_data);

void add_to_trace(uint8_t p_data[], uint8_t p_length);

#endif // ELMO_FUNCS_H
