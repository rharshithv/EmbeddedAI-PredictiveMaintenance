
#include <stdbool.h>

bool classify_motor(float peak_amplitude)
{
    return peak_amplitude > 1.442362666130066f;
}
