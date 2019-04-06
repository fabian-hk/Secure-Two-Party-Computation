/*  
*   Byte-oriented AES-256 implementation.
*   All lookup tables replaced with 'on the fly' calculations. 
*
*   Copyright (c) 2007-2009 Ilya O. Levin, http://www.literatecode.com
*   Other contributors: Hal Finney
*
*   Permission to use, copy, modify, and distribute this software for any
*   purpose with or without fee is hereby granted, provided that the above
*   copyright notice and this permission notice appear in all copies.
*
*   THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
*   WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
*   MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
*   ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
*   WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
*   ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
*   OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
*/

//#define F(x)   (((x)<<1) ^ ((((x)>>7) & 1) * 0x1b))
#define FD(x)  (((x) >> 1) ^ (((x) & 1) ? 0x8d : 0))

#define USE_S_BOX

//
//#include <stdio.h>
//
//#define DUMP(s, i, buf, sz)  {printf(s);                   \
//                              for (i = 0; i < (sz);i++)    \
//                                  printf("%02x ", buf[i]); \
//                              printf("\n");}

typedef unsigned char uint8_t;


const uint8_t sbox[256] = {
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
    0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
    0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc,
    0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a,
    0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
    0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
    0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85,
    0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
    0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17,
    0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88,
    0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c,
    0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9,
    0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6,
    0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e,
    0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94,
    0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68,
    0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
};



    typedef struct {
        // Key schedule
        uint8_t key[32]; 
        uint8_t enckey[16]; 
        //uint8_t deckey[16];
    } aes128_context; 

    
    
    
    // 11th entry not used
uint8_t rcon_table[11]={0x01, 0x02, 0x04,  0x08,  0x10,  0x20,  0x40,  0x80,  0x1b, 0x36, 0x6c};
    
/* -------------------------------------------------------------------------- */
uint8_t gf_alog(uint8_t x) // calculate anti-logarithm gen 3
{
    uint8_t atb = 1, z;

    while (x--) {z = atb; atb <<= 1; if (z & 0x80) atb^= 0x1b; atb ^= z;}

    return atb;
} /* gf_alog */

/* -------------------------------------------------------------------------- */
uint8_t gf_log(uint8_t x) // calculate logarithm gen 3
{
    uint8_t atb = 1, i = 0, z;

    do {
        if (atb == x) break;
        z = atb; atb <<= 1; if (z & 0x80) atb^= 0x1b; atb ^= z;
    } while (++i > 0);

    return i;
} /* gf_log */


/* -------------------------------------------------------------------------- */
uint8_t gf_mulinv(uint8_t x) // calculate multiplicative inverse
{
    return (x) ? gf_alog(255 - gf_log(x)) : 0;
} /* gf_mulinv */

/* -------------------------------------------------------------------------- */

#ifdef USE_S_BOX

#define rj_sbox(x)     sbox[(x)]

#else

uint8_t rj_sbox(uint8_t x)
{
    uint8_t y, sb;

    sb = y = gf_mulinv(x);
    y = (y<<1)|(y>>7); sb ^= y;  y = (y<<1)|(y>>7); sb ^= y; 
    y = (y<<1)|(y>>7); sb ^= y;  y = (y<<1)|(y>>7); sb ^= y;

    return (sb ^ 0x63);
}  /* rj_sbox */
#endif

/* -------------------------------------------------------------------------- */
//uint8_t rj_sbox_inv(uint8_t x)
//{
//    uint8_t y, sb;
//
//    y = x ^ 0x63;
//    sb = y = (y<<1)|(y>>7);
//    y = (y<<2)|(y>>6); sb ^= y; y = (y<<3)|(y>>5); sb ^= y;
//
//    return gf_mulinv(sb);
//} /* rj_sbox_inv */


/* -------------------------------------------------------------------------- */
//uint8_t rj_xtime(uint8_t x) 
//{
//    return (x & 0x80) ? ((x << 1) ^ 0x1b) : (x << 1);
//} /* rj_xtime */

/* -------------------------------------------------------------------------- */
void aes_subBytes(uint8_t *buf)
{
    //register 
	uint8_t i = 16;

    while (i--) buf[i] = rj_sbox(buf[i]);
} /* aes_subBytes */

/* -------------------------------------------------------------------------- */
//void aes_subBytes_inv(uint8_t *buf)
//{
//    register uint8_t i = 16;
//
//    while (i--) buf[i] = rj_sbox_inv(buf[i]);
//} /* aes_subBytes_inv */

/* -------------------------------------------------------------------------- */
void aes_addRoundKey(uint8_t *buf, uint8_t *key)
{
    //register 
    uint8_t i = 16;

    while (i--) buf[i] ^= key[i];
} /* aes_addRoundKey */

void aes_addRoundKey_cpy128(uint8_t *buf, uint8_t *key, uint8_t *cpk)
{
    //register 
    uint8_t i = 16;

    // Change, Lower bits in cpk are ignored!
    while (i--)  buf[i] ^= (cpk[16+i] = key[i]) ;
} /* aes_addRoundKey_cpy */


/* -------------------------------------------------------------------------- */
void aes_shiftRows(uint8_t *buf)
{
    //register 
    uint8_t i, j; /* to make it potentially parallelable :) */

    i = buf[1]; buf[1] = buf[5]; buf[5] = buf[9]; buf[9] = buf[13]; buf[13] = i;
    i = buf[10]; buf[10] = buf[2]; buf[2] = i;
    j = buf[3]; buf[3] = buf[15]; buf[15] = buf[11]; buf[11] = buf[7]; buf[7] = j;
    j = buf[14]; buf[14] = buf[6]; buf[6]  = j;
}
 /* aes_shiftRows */

/* -------------------------------------------------------------------------- */
//void aes_shiftRows_inv(uint8_t *buf)
//{
//    register uint8_t i, j; /* same as above :) */
//
//    i = buf[1]; buf[1] = buf[13]; buf[13] = buf[9]; buf[9] = buf[5]; buf[5] = i;
//    i = buf[2]; buf[2] = buf[10]; buf[10] = i;
//    j = buf[3]; buf[3] = buf[7]; buf[7] = buf[11]; buf[11] = buf[15]; buf[15] = j;
//    j = buf[6]; buf[6] = buf[14]; buf[14] = j;
//
//} /* aes_shiftRows_inv */

/* -------------------------------------------------------------------------- */
//void aes_mixColumns(uint8_t *buf)
//{
//    register uint8_t i, a, b, c, d, e;
//
//    for (i = 0; i < 16; i += 4)
//    {
//        a = buf[i]; b = buf[i + 1]; c = buf[i + 2]; d = buf[i + 3];
//        e = a ^ b ^ c ^ d;
//        buf[i] ^= e ^ rj_xtime(a^b);   buf[i+1] ^= e ^ rj_xtime(b^c);
//        buf[i+2] ^= e ^ rj_xtime(c^d); buf[i+3] ^= e ^ rj_xtime(d^a);
//    }
//} /* aes_mixColumns */

/* -------------------------------------------------------------------------- */
void aes_mixColumn_wiki(uint8_t *buf)
{
    // Code from wikipedia
        uint8_t a[4];
        uint8_t b[4];
        uint8_t c;
        uint8_t h;
        /* The array 'a' is simply a copy of the input array 'r'
         * The array 'b' is each element of the array 'a' multiplied by 2
         * in Rijndael's Galois field
         * a[n] ^ b[n] is element n multiplied by 3 in Rijndael's Galois field */ 
        for(c=0;c<4;c++) {
                a[c] = buf[c];
                /* h is 0xff if the high bit of r[c] is set, 0 otherwise */
                h = (unsigned char)((signed char)buf[c] >> 7); /* arithmetic right shift, thus shifting in either zeros or ones */
                b[c] = buf[c] << 1; /* implicitly removes high bit because b[c] is an 8-bit char, so we xor by 0x1b and not 0x11b in the next line */
                b[c] ^= 0x1B & h; /* Rijndael's Galois field */
        }
        buf[0] = b[0] ^ a[3] ^ a[2] ^ b[1] ^ a[1]; /* 2 * a0 + a3 + a2 + 3 * a1 */
        buf[1] = b[1] ^ a[0] ^ a[3] ^ b[2] ^ a[2]; /* 2 * a1 + a0 + a3 + 3 * a2 */
        buf[2] = b[2] ^ a[1] ^ a[0] ^ b[3] ^ a[3]; /* 2 * a2 + a1 + a0 + 3 * a3 */
        buf[3] = b[3] ^ a[2] ^ a[1] ^ b[0] ^ a[0]; /* 2 * a3 + a2 + a1 + 3 * a0 */
} /* aes_mixColumns */

/* -------------------------------------------------------------------------- */
void aes_mixColumns_wiki(uint8_t *buf)
{
    uint8_t i;
    for(i=0; i < 16; i+=4) {
        aes_mixColumn_wiki(&(buf[i]));
    }
} /* aes_mixColumns */



///* -------------------------------------------------------------------------- */
//void aes_mixColumns_inv(uint8_t *buf)
//{
//    register uint8_t i, a, b, c, d, e, x, y, z;
//
//    for (i = 0; i < 16; i += 4)
//    {
//        a = buf[i]; b = buf[i + 1]; c = buf[i + 2]; d = buf[i + 3];
//        e = a ^ b ^ c ^ d;
//        z = rj_xtime(e);
//        x = e ^ rj_xtime(rj_xtime(z^a^c));  y = e ^ rj_xtime(rj_xtime(z^b^d));
//        buf[i] ^= x ^ rj_xtime(a^b);   buf[i+1] ^= y ^ rj_xtime(b^c);
//        buf[i+2] ^= x ^ rj_xtime(c^d); buf[i+3] ^= y ^ rj_xtime(d^a);
//    }
//} /* aes_mixColumns_inv */

// Changed to 128bit version
/* -------------------------------------------------------------------------- */
void aes_expandEncKey128(uint8_t *k, uint8_t *rc) 
{
    
    //register 
	uint8_t i;
    //DUMP("before expand: ", i, k, 32);
    
    
    // does two key iteration at once
    k[0] = k[16] ^ rj_sbox(k[29]) ^ (rcon_table[*rc]);
    k[1] = k[17] ^ rj_sbox(k[30]);
    k[2] = k[18] ^ rj_sbox(k[31]);
    k[3] = k[19] ^ rj_sbox(k[28]);
    
    (*rc)++;

    for(i = 4; i < 16; i += 4) {
        k[i] = k[i+16] ^ k[i-4];
        k[i+1] = k[i+17] ^ k[i-3];
        k[i+2] = k[i + 18] ^ k[i-2];
        k[i+3] = k[i + 19] ^ k[i-1];
    }     
    
    // CHANGED added round_counter
    k[16] = k[0] ^ rj_sbox(k[13]) ^ (rcon_table[*rc]);
    k[17] = k[1] ^ rj_sbox(k[14]);
    k[18] = k[2] ^ rj_sbox(k[15]);
    k[19] = k[3] ^ rj_sbox(k[12]);
    
    (*rc)++;
    
    for(i = 20; i < 32; i += 4) {
        k[i] = k[i-4] ^ k[i-16];   
        k[i+1] = k[i-3] ^ k[i-15];
        k[i+2] = k[i-2] ^ k[i-14];
        k[i+3] = k[i-1] ^ k[i-13];
    }

} /* aes_expandEncKey */

///* -------------------------------------------------------------------------- */
//void aes_expandDecKey128(uint8_t *k, uint8_t *rc) 
//{
//    uint8_t i;
//
//    for(i = 28; i > 16; i -= 4) k[i+0] ^= k[i-4], k[i+1] ^= k[i-3], 
//        k[i+2] ^= k[i-2], k[i+3] ^= k[i-1];
//
//    k[16] ^= rj_sbox(k[12]);
//    k[17] ^= rj_sbox(k[13]);
//    k[18] ^= rj_sbox(k[14]);
//    k[19] ^= rj_sbox(k[15]);
//
//    for(i = 12; i > 0; i -= 4)  k[i+0] ^= k[i-4], k[i+1] ^= k[i-3],
//        k[i+2] ^= k[i-2], k[i+3] ^= k[i-1];
//
//    *rc = FD(*rc);
//    k[0] ^= rj_sbox(k[29]) ^ (*rc);
//    k[1] ^= rj_sbox(k[30]);
//    k[2] ^= rj_sbox(k[31]);
//    k[3] ^= rj_sbox(k[28]);
//} /* aes_expandDecKey */


/* -------------------------------------------------------------------------- */
void aes128_init_enc(aes128_context *ctx, uint8_t *k)
{
    //register uint8_t i;
    uint8_t i;

    // Copy enckey into key buffer
    for (i = 0; i < 16; i++) ctx->enckey[i] = k[i];
    // expand deckey 8 rounds? dunno why
    //for (i = 8;--i;) aes_expandEncKey128(ctx->deckey, &rcon);
    
    
} /* aes256_init */

/* -------------------------------------------------------------------------- */
//void aes256_done(aes128_context *ctx)
//{
//    register uint8_t i;
//
//    for (i = 0; i < sizeof(ctx->key); i++) 
//        ctx->key[i] = ctx->enckey[i] = ctx->deckey[i] = 0;
//} /* aes256_done */

/* -------------------------------------------------------------------------- */
void aes128_encrypt_ecb(aes128_context *ctx, uint8_t *buf)
{
    uint8_t i;//,j;
    uint8_t rcon = 0;

    // Copy enckey into key (TODO nesessary for 128?)
    aes_addRoundKey_cpy128(buf, ctx->enckey, ctx->key);
    
    //DUMP("Buf0: ",i,buf,16);
    
   // uint8_t *key2 = &(ctx->key[16]);
    
    //DUMP("Key0: ",i,key2,16);
    //aes_expandEncKey128(ctx->key, &rcon);
    //DUMP("Key1: ",i,ctx->key,16);
   // DUMP("Key2: ",i,key2,16);
     
    // change: 14 -> 10
    // only two rounds!
    for(i = 0; i < 1; ++i)
    {
        aes_subBytes(buf);
      //  DUMP("Sub: ",j , buf,16);
        aes_shiftRows(buf);
      //  DUMP("Shift: ",j ,buf ,16);
        aes_mixColumns_wiki(buf);
      //  DUMP("Mix: ",j ,buf ,16);
        // Alternating: ExpandEncKey generates two rounds at once to speed up.
        if( i & 1 ) {
            
            //aes_expandEncKey128(ctx->key, &rcon);
            aes_addRoundKey(buf, &ctx->key[16]);
            //uint8_t *key2 = &(ctx->key[16]);
            //uint8_t j;
            //DUMP("Key: ",j,ctx->key,16);
            //DUMP("Key: ",j,key2,16);
        } else {
//            aes_expandEncKey128(ctx->key, &rcon);
            aes_addRoundKey( buf, ctx->key);
        }
        //DUMP("Buf: ",j,buf,16);
    }
    aes_subBytes(buf);
    aes_shiftRows(buf);
    aes_addRoundKey(buf, &ctx->key[16]);
} /* aes256_encrypt */

///* -------------------------------------------------------------------------- */
//void aes256_decrypt_ecb(aes128_context *ctx, uint8_t *buf)
//{
//    uint8_t i, rcon;
//
//    aes_addRoundKey_cpy128(buf, ctx->deckey, ctx->key);
//    aes_shiftRows_inv(buf);
//    aes_subBytes_inv(buf);
//
//    for (i = 10, rcon = 0x80; --i;)
//    {
//        if( ( i & 1 ) )           
//        {
//            aes_expandDecKey128(ctx->key, &rcon);
//            aes_addRoundKey(buf, &ctx->key[16]);
//        }
//        else aes_addRoundKey(buf, ctx->key);
//        aes_mixColumns_inv(buf);
//        aes_shiftRows_inv(buf);
//        aes_subBytes_inv(buf);
//    }
//    aes_addRoundKey( buf, ctx->key); 
//} /* aes256_decrypt */



#ifdef SHIFTROWS_CBMC
uint8_t shiftrows_cbmc(int INPUT_A_x, int INPUT_B_x) {
    aes128_context ctx;
    //uint8_t key[16];
    uint8_t buf[16];
    uint8_t OUTPUT_z1, o1 = 0;
    uint8_t OUTPUT_z2, o2 = 0;
    uint8_t OUTPUT_z3, o3 = 0;
    uint8_t OUTPUT_z4, o4 = 0;
    //uint8_t key[32];
    //uint8_t buf[16], i;
    uint8_t i;

    /* put a test vector */
    for (i = 0; i < 16;i++) {
	buf[i] = INPUT_A_x + INPUT_B_x + i;
    }
    //aes_shiftRows(buf);
    aes_mixColumns_wiki(buf);
    for (i = 0; i < 16; i+=4) {
            o1 += buf[i];
            o2 += buf[i+1];
            o3 += buf[i+2];
            o4 += buf[i+3];
    }
        
    OUTPUT_z1 = o1;
    return OUTPUT_z1;
} /* main */
#endif

aes128_context ctx;
    
/* you can replace encrypt by decrypt */
uint8_t mpc_main(int INPUT_A_x, int INPUT_B_x) {
    uint8_t key[16];
    uint8_t buf[16];
	uint8_t OUTPUTz;
    //uint8_t key[32];
    //uint8_t buf[16], i;
    uint8_t i;

    /* put a test vector */
    for (i = 0; i < 16;i++) {
	buf[i] = i * 16 + i;
    }
    for (i = 0; i < 16;i++) {
	key[i] = INPUT_A_x+INPUT_B_x+i;
    }

    aes128_init_enc(&ctx, key);
    aes128_encrypt_ecb(&ctx, buf);

	
	//OUTPUTz = buf[0];
    OUTPUTz = buf[0]+buf[1];
 
    return OUTPUTz;
} /* main */


//int main() {
//    
//    // 'Correctness' comparison: http://openschemes.com/2010/03/03/fun-with-aes-128-example-encryption-with-aes-trainer/
//    
//    aes128_context ctx;
//    unsigned int i;
//    //unsigned char key[16] = "abcdabcdabcdabcd";
//    //unsigned char buf[16] = "0123456789ABCDEF";
//    
//    unsigned char key[16] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f};
//    unsigned char buf[16] = {0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff};
//    
//    
//    
// //   uint8_t rc = 0;
////    uint8_t double_key[32];
////    for(i =16; i<32;i++) {
////        double_key[i]=key[i-16];
////    }
////    aes_expandEncKey128(double_key, &rc) ;
////    DUMP("double key: ", i, double_key, 16);
////    return 0;
////    
//    
//    
//    DUMP("key: ", i, key, sizeof(key));
//    DUMP("buf: ", i, buf, sizeof(buf));
//
//    aes128_init_enc(&ctx, key);
//    aes128_encrypt_ecb(&ctx,buf);
//    
//    
//    DUMP("enc: ", i, buf, sizeof(buf));
//    
//    return 0;
//}
