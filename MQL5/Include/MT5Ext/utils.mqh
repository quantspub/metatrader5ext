// Collection of misc tools for MQL5

// Utility functions for formatting values
string floatMaxString(double val) {
    return (val != DBL_MAX) ? DoubleToString(val, 8) : "";
}

string longMaxString(long val) {
    return (val != LONG_MAX) ? IntegerToString(val) : "";
}

string intMaxString(int val) {
    return (val != INT_MAX) ? IntegerToString(val) : "";
}

bool isAsciiPrintable(string val) {
    for (int i = 0; i < StringLen(val); i++) {
        if (StringGetCharacter(val, i) < 32 || StringGetCharacter(val, i) >= 128) {
            return false;
        }
    }
    return true;
}

string decimalMaxString(double val) {
    return (val != DBL_MAX) ? DoubleToString(val, 8) : "";
}

// 
// 
// Helper functions for encoding and compressing strings
// 
// 

// Function to compress a string using a basic run-length encoding (RLE) algorithm
// uchar[] CompressString(string input)
// {
//     uchar compressed[];
//     int len = StringLen(input);
//     int count = 1;
    
//     for (int i = 0; i < len; i++)
//     {
//         uchar ch = (uchar)StringGetCharacter(input, i);
//         ArrayResize(compressed, ArraySize(compressed) + 1);
//         compressed[ArraySize(compressed) - 1] = ch;
        
//         if (i + 1 < len && StringGetCharacter(input, i) == StringGetCharacter(input, i + 1))
//         {
//             count++;
//         }
//         else
//         {
//             ArrayResize(compressed, ArraySize(compressed) + 1);
//             compressed[ArraySize(compressed) - 1] = (uchar)count;
//             count = 1;
//         }
//     }
//     return compressed;
// }

// // Function to encode and compress strings
// uchar[] EncodeStringWithRLECompression(string input)
// {
//     uchar encoded[];
//     uchar compressed[] = CompressString(input);
    
//     for (int i = 0; i < ArraySize(compressed); i++)
//     {
//         uchar ch = compressed[i] + 42;  // Simple shift encoding
//         ArrayResize(encoded, ArraySize(encoded) + 1);
//         encoded[ArraySize(encoded) - 1] = ch;
//     }
//     return encoded;
// }