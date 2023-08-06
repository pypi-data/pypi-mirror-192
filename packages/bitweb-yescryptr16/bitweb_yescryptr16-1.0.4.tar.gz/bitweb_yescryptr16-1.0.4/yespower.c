#include "yespower.h"
/* 
 * yespower for bitweb coin
 */
int yespower_hash(const char *input, char *output)
{
	yespower_params_t params = {YESPOWER_0_5, 4096, 16, "Client Key", 10};
	return yespower_tls(input, 80, &params, (yespower_binary_t *) output);
}
