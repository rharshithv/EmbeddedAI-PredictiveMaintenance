
#include <stdio.h>

int main(void)
{
    float peak_amplitude;

    while (scanf("%f", &peak_amplitude) == 1)
    {
        if (peak_amplitude <= 1.442362666130066f)
        {
            printf("normal\n");
        }
        else
        {
            printf("abnormal\n");
        }
    }

    return 0;
}
