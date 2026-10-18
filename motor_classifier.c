
#include <stdio.h>

const char *classify_motor(float peak_amplitude)
{
    if (peak_amplitude <= 1.44236267f)
    {
        return "normal";
    }

    return "abnormal";
}

int main(void)
{
    float peak_amplitude;

    while (scanf("%f", &peak_amplitude) == 1)
    {
        printf("%s\n", classify_motor(peak_amplitude));
    }

    return 0;
}
