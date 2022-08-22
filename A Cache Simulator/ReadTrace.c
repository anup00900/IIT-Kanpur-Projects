#include<stdio.h>
#include<assert.h>
#include<stdlib.h>
#include<string.h>


int main(int argc, char *argv[] ){
    
    int k;
    char input_name[strlen(argv[1])+2];    
    FILE *fp, *fw;
    unsigned long long *addr;
    char *type,*iord;
    unsigned* pc;
    int numtraces = atoi(argv[2]);

    type = (char*)malloc(sizeof(char));
    addr = (unsigned long long*)malloc(sizeof(unsigned long long));
    iord = (char*)malloc(sizeof(char));
    pc   = (unsigned*)malloc(sizeof(unsigned));

    for (k=0; k<numtraces; k++) {
        sprintf(input_name, "%s_%d", argv[1], k);
        fp = fopen(input_name, "rb");
        assert(fp != NULL);
        
        char str[strlen(argv[1])] ;
        sprintf(str, "%s", argv[1]);
        char *pch;
        pch = strrchr(str, '/');
        if (pch != NULL) {
            pch++; /* step over the slash */
        }

        char o_name[1000];       
        sprintf(o_name, "L1Miss_%s_%d", pch, k);
        
        fw=fopen(o_name, "w");
        while (!feof(fp)) {
            fread(iord, sizeof(char), 1, fp);
            fread(type, sizeof(char), 1, fp);
            fread(addr, sizeof(unsigned long long), 1, fp);         
            fread(pc, sizeof(unsigned), 1, fp);
            
            fprintf(fw,"%d %llu\n",(int)*type,*addr);
        }

        fclose(fp);
        fclose(fw);
        
        printf("Done reading %s %d!\n", argv[1], k);
    }
    return 0;
}

