#include <socket-library-mt4-mt5.mqh>

// Function to compress a string using a basic run-length encoding (RLE) algorithm
uchar[] CompressString(string input)
{
    uchar compressed[];
    int len = StringLen(input);
    int count = 1;
    
    for (int i = 0; i < len; i++)
    {
        uchar ch = (uchar)StringGetCharacter(input, i);
        ArrayResize(compressed, ArraySize(compressed) + 1);
        compressed[ArraySize(compressed) - 1] = ch;
        
        if (i + 1 < len && input[i] == input[i + 1])
        {
            count++;
        }
        else
        {
            ArrayResize(compressed, ArraySize(compressed) + 1);
            compressed[ArraySize(compressed) - 1] = (uchar)count;
            count = 1;
        }
    }
    return compressed;
}

// Function to encode and compress strings
uchar[] EncodeString(string input)
{
    uchar encoded[];
    uchar compressed[] = CompressString(input);
    
    for (int i = 0; i < ArraySize(compressed); i++)
    {
        uchar ch = compressed[i] + 42;  // Simple shift encoding
        ArrayResize(encoded, ArraySize(encoded) + 1);
        encoded[ArraySize(encoded) - 1] = ch;
    }
    return encoded;
}
