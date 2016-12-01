#include <gmp.h>
#include <stdio.h>

int main(int argc, char **argv) {
  mpz_t res, h1, h2, s1, s2;
  mpz_init(res);

  mpz_init_set_str (s1, argv[1], 10); // signature value
  mpz_init_set_str (h1, argv[2], 10); // pkcs1 padded message hash

  mpz_init_set_str (s2, argv[3], 10); // signature value
  mpz_init_set_str (h2, argv[4], 10); // pkcs1 padded message hash

  mpz_pow_ui(res, s1, 65537);
  mpz_sub(s1, res, h1);

  mpz_pow_ui(res, s2, 65537);
  mpz_sub(s2, res, h2);

  mpz_gcd(res, s1, s2);
  char* ptr=mpz_get_str(0,10,res);
  printf("%s\n", ptr);  // the public key that signed both messages
  return 0;
}
