#include <stdio.h>
#include <stdlib.h>

#define BAUDOT_ERROR 0xFF;

#define LIMITATION_CHI_2_BACK 1
#define LIMITATION_NONE 0

char ascii2baudot(char a);
char baudot2ascii(char b, int LTRS);
char get_bit(char b, int pos);
char set_bit(char b, int pos, int bit);
void advance_kpos(int kpos[5]);
void advance_spos(int spos[5]);
void advance_m1pos(int *m1pos);
void advance_m2pos(int *m2pos);

// BREAM SETTINGS for LORENZ CIPHER                
//              . . . x x x x . . . . x x . . . . x . x x . . x . . x x . x . x x . x . x x x x .
char bk1[41] = {0,0,0,1,1,1,1,0,0,0,0,1,1,0,0,0,0,1,0,1,1,0,0,1,0,0,1,1,0,1,0,1,1,0,1,0,1,1,1,1,0};
//              x x . . x x x . x x . . . x . x . x x . . . x . . . . x x x .
char bk2[31] = {1,1,0,0,1,1,1,0,1,1,0,0,0,1,0,1,0,1,1,0,0,0,1,0,0,0,0,1,1,1,0};
//              . . x x x . x x . . x . . . . x x x . . x x . x x . . x x
char bk3[29] = {0,0,1,1,1,0,1,1,0,0,1,0,0,0,0,1,1,1,0,0,1,1,0,1,1,0,0,1,1}; 
//              . . x x . . x . x x . . x . . x x . . x . . x x x x
char bk4[26] = {0,0,1,1,0,0,1,0,1,1,0,0,1,0,0,1,1,0,0,1,0,0,1,1,1,1}; 
//              . x . . . x . x x . . x . . . x x x . x x x .
char bk5[23] = {0,1,0,0,0,1,0,1,1,0,0,1,0,0,0,1,1,1,0,1,1,1,0};
//              x x x . x . x x . . x x . . x x . . . x x x x . x . x x . x x . . . x x . . . . x x x x . x x . . x x . . . x x . . . . x
char bm1[61] = {1,1,1,0,1,0,1,1,0,0,1,1,0,0,1,1,0,0,0,1,1,1,1,0,1,0,1,1,0,1,1,0,0,0,1,1,0,0,0,0,1,1,1,1,0,1,1,0,0,1,1,0,0,0,1,1,0,0,0,0,1};
//              x . x x x . x . x . x . x . . x . x . x x x . x . x . x . x . x . x . x .
char bm2[37] = {1,0,1,1,1,0,1,0,1,0,1,0,1,0,0,1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0}; 
//              . . x . x . x . x . x . . x . . x . x x . x x . x . x . . x x . x x x . . x x x . . . 
char bs1[43] = {0,0,1,0,1,0,1,0,1,0,1,0,0,1,0,0,1,0,1,1,0,1,1,0,1,0,1,0,0,1,1,0,1,1,1,0,0,1,1,1,0,0,0};
//              . . x . x x . x . x . x . x . x . x x . . x x . x . . x . x x x x . . . . . x x x . . x . x x 
char bs2[47] = {0,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,0,1,1,0,1,0,0,1,0,1,1,1,1,0,0,0,0,0,1,1,1,0,0,1,0,1,1};
//              x . x . x . x . x . x . x . . x . . x x . x . x . x x x x . . . . x x x . . . x x x . x x . . x . . x 
char bs3[51] = {1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1,0,0,1,1,0,1,0,1,0,1,1,1,1,0,0,0,0,1,1,1,0,0,0,1,1,1,0,1,1,0,0,1,0,0,1};
//              x . x . . x x . x . x . x . x . x . x x . x . . . . x x . . x x . . x x . x x x x x . x . . x . . . . x .
char bs4[53] = {1,0,1,0,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0,0,0,0,1,1,0,0,1,1,0,0,1,1,0,1,1,1,1,1,0,1,0,0,1,0,0,0,0,1,0};
//              . x . x . x . x . x x . . . x . x . . x x x . x x x x . x x . x . . . . x . . . x . . x x . x x . . x x . . x . x . x 
char bs5[59] = {0,1,0,1,0,1,0,1,0,1,1,0,0,0,1,0,1,0,0,1,1,1,0,1,1,1,1,0,1,1,0,1,0,0,0,0,1,0,0,0,1,0,0,1,1,0,1,1,0,0,1,1,0,0,1,0,1,0,1};


int main(int argc, char *argv[])
{
    // the following are the start positions for each of the wheels
    int kpos[5]={0,6,7,3,4};
    int m1pos=20;
    int m2pos=10;
    int spos[5]={8,26,16,21,24};

    int TOTAL_MOTOR, BASIC_MOTOR;
    int LIMITATION;

    char message[] = "qzahlen<<n>>";
    char ch,bp,bc; // bp = plaintext baudot code, bc = ciphertext
    char bit;
    
    int i,j;
    // for each letter in message
    for(i=0; i<strlen(message); i++){
        bc = 0;
        ch = toupper(message[i]);
        bp = ascii2baudot(ch);
        // encrypt each bit separately
        bit = get_bit(bp,0);
        bit ^= bk1[kpos[0]] ^ bs1[spos[0]];
        bc = set_bit(bc,0,bit);
              
        bit = get_bit(bp,1);
        bit ^= bk2[kpos[1]] ^ bs2[spos[1]];
        bc = set_bit(bc,1,bit);       
        
        bit = get_bit(bp,2);
        bit ^= bk3[kpos[2]] ^ bs3[spos[2]];
        bc = set_bit(bc,2,bit);       
        
        bit = get_bit(bp,3);
        bit ^= bk4[kpos[3]] ^ bs4[spos[3]];
        bc = set_bit(bc,3,bit);  
        
        bit = get_bit(bp,4);
        bit ^= bk5[kpos[4]] ^ bs5[spos[4]];
        bc = set_bit(bc,4,bit);    

        ch = baudot2ascii(bc,1);
        printf("%c",ch);                          
         
        if(LIMITATION_CHI_2_BACK) LIMITATION = bk2[(kpos[1]+30)%31];
        else LIMITATION = 1;
        
        BASIC_MOTOR = bm2[m2pos];      
        TOTAL_MOTOR = !(!BASIC_MOTOR && LIMITATION);
 
        advance_kpos(kpos); 
        if(TOTAL_MOTOR != 0) advance_spos(spos);
        if(bm1[m1pos] != 0) advance_m2pos(&m2pos);
        advance_m1pos(&m1pos);
    }
    printf("\n");
    system("PAUSE");	
    return 0;
}

char get_bit(char b, int pos){
    b >>= pos;
    b &= 0x01;
    return b;     
}

// sets position 'pos' of byte 'b' to value 'bit'
char set_bit(char b, int pos, int bit){
    int mask = ~(1 << pos);
    int ret = 0;
    bit = bit ? 1 : 0; // ensure b is either 0 or 1
    ret = b & mask;
    ret |= bit << pos;
    return ret;     
}

/* advance the k-wheels 1 position */
void advance_kpos(int kpos[5]){
     kpos[0] = (kpos[0] + 1)%41;
     kpos[1] = (kpos[1] + 1)%31;
     kpos[2] = (kpos[2] + 1)%29;  
     kpos[3] = (kpos[3] + 1)%26;  
     kpos[4] = (kpos[4] + 1)%23;  
}

void advance_m1pos(int *m1pos){
     *m1pos = (*m1pos + 1)%61;
}

void advance_m2pos(int *m2pos){
     *m2pos = (*m2pos + 1)%37;
}

/* advance the k-wheels 1 position */
void advance_spos(int spos[5]){
     spos[0] = (spos[0] + 1)%43;
     spos[1] = (spos[1] + 1)%47;
     spos[2] = (spos[2] + 1)%51;  
     spos[3] = (spos[3] + 1)%53;  
     spos[4] = (spos[4] + 1)%59;  
}


/*************************************************************************
converts a baudot code to ascii. if LTRS is 1, returns letters, else assumes FIGS
**************************************************************************/
char baudot2ascii(char b, int LTRS){
    switch(b){
      case 0x03: return  LTRS ? 'A' : '-';
      case 0x19: return  LTRS ? 'B' : '?';
      case 0x0E: return  LTRS ? 'C' : ':';
      case 0x09: return  LTRS ? 'D' : '$';
      case 0x01: return  LTRS ? 'E' : '3';
      case 0x0D: return  LTRS ? 'F' : '!';
      case 0x1A: return  LTRS ? 'G' : '&';
      case 0x14: return  LTRS ? 'H' : '#';
      case 0x06: return  LTRS ? 'I' : '8';
      case 0x0B: return  LTRS ? 'J' : 'b';
      case 0x0F: return  LTRS ? 'K' : '(';
      case 0x12: return  LTRS ? 'L' : ')';
      case 0x1C: return  LTRS ? 'M' : '.';
      case 0x0C: return  LTRS ? 'N' : ',';
      case 0x18: return  LTRS ? 'O' : '9';
      case 0x16: return  LTRS ? 'P' : '0';
      case 0x17: return  LTRS ? 'Q' : '1';
      case 0x0A: return  LTRS ? 'R' : '4';
      case 0x05: return  LTRS ? 'S' : '\'';
      case 0x10: return  LTRS ? 'T' : '5';
      case 0x07: return  LTRS ? 'U' : '7';
      case 0x1E: return  LTRS ? 'V' : ';';
      case 0x13: return  LTRS ? 'W' : '2';
      case 0x1D: return  LTRS ? 'X' : '/';
      case 0x15: return  LTRS ? 'Y' : '6';
      case 0x11: return  LTRS ? 'Z' : '"';
      case 0x08: return 'n';              // '3'  in comments are the characters as used by british
      case 0x02: return 'r';              // '4'
      case 0x04: return '_';              // ' '
      case 0x1F: return '>'; // LTRS      // '+'
      case 0x1B: return '<'; // FIGS      // '-'
      case 0x00: return 'i';              // '/'
      default: return BAUDOT_ERROR;
    }             
}

/* this table only deals with encoded ascii, and doesnt worry about FIGS */
char ascii2baudot(char a){
    switch(a){   
      case 'A': return 0x03;
      case 'B': return 0x19;
      case 'C': return 0x0E;
      case 'D': return 0x09;
      case 'E': return 0x01;
      case 'F': return 0x0D;
      case 'G': return 0x1A;
      case 'H': return 0x14;
      case 'I': return 0x06;
      case 'J': return 0x0B;
      case 'K': return 0x0F;
      case 'L': return 0x12;
      case 'M': return 0x1C;
      case 'N': return 0x0C;
      case 'O': return 0x18;
      case 'P': return 0x16;
      case 'Q': return 0x17;
      case 'R': return 0x0A;
      case 'S': return 0x05;
      case 'T': return 0x10;
      case 'U': return 0x07;
      case 'V': return 0x1E;
      case 'W': return 0x13;
      case 'X': return 0x1D;
      case 'Y': return 0x15;
      case 'Z': return 0x11;
      case 'n': return 0x08;  // represents \n
      case 'r': return 0x02; // represents \r
      case '_': return 0x04;
      case '>': return 0x1F; // LTRS
      case '<': return 0x1B; // FIGS
      case 'i': return 0;    // NULL
      default: return 0x04; // just a placeholder
    }
}
