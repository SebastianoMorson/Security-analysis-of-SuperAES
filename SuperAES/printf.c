#include <stdarg.h>
int vprintf_(const char* format, va_list va);
int printf(const char *str, ...) {
     va_list va;
     va_start(va, str);
     int ret = vprintf_(str, va);
     va_end(va);
     return ret;
}