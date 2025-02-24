//+------------------------------------------------------------------+
//|  MQL5 Implementation of IB Low-Level Messaging                   |
//+------------------------------------------------------------------+

// Function to encode a message with a length prefix
uchar[] MakeMessage(string text)
{
    uchar encoded[];
    int length = StringLen(text);
    ArrayResize(encoded, 4 + length);
    IntToByteArray(length, encoded, 0);
    StringToCharArray(text, encoded, 4);
    return encoded;
}

// Helper function to convert an integer to a 4-byte array
void IntToByteArray(int value, uchar &arr[], int pos)
{
    arr[pos] = (uchar)(value >> 24);
    arr[pos + 1] = (uchar)(value >> 16);
    arr[pos + 2] = (uchar)(value >> 8);
    arr[pos + 3] = (uchar)value;
}

// Function to add a NULL-terminated field
string MakeField(string val)
{
    return val + "\0";
}

// Function to handle empty values
string MakeFieldHandleEmpty(string val)
{
    if (StringLen(val) == 0)
        return "\0";
    return MakeField(val);
}

// Function to decode a message
string ReadMessage(uchar &buffer[])
{
    if (ArraySize(buffer) < 4)
        return "";
    int size = (buffer[0] << 24) | (buffer[1] << 16) | (buffer[2] << 8) | buffer[3];
    if (ArraySize(buffer) - 4 < size)
        return "";
    return CharArrayToString(buffer, 4, size);
}

// Function to split a message into fields
string[] ReadFields(string msg)
{
    string fields[];
    StringSplit(msg, '\0', fields);
    return fields;
}

// 
// comm2.mqh
// 

// This script contains tools for implementing low-level messaging similar to the IB API.

// Function to create a message with a length prefix
uchar[] MakeMsg(string text) {
    int length = StringLen(text);
    uchar msg[];
    ArrayResize(msg, 4 + length);
    // Pack the length as a 4-byte integer in network byte order (big-endian)
    msg[0] = (length >> 24) & 0xFF;
    msg[1] = (length >> 16) & 0xFF;
    msg[2] = (length >> 8) & 0xFF;
    msg[3] = length & 0xFF;
    // Append the text as bytes
    for (int i = 0; i < length; i++) {
        msg[4 + i] = text[i];
    }
    return msg;
}

// Function to create a field with a NULL terminator
string MakeField(const string &val) {
    if (val == NULL) {
        Print("Cannot send NULL to TWS");
        return "";
    }
    // Check if the string contains non-ASCII characters
    for (int i = 0; i < StringLen(val); i++) {
        if (val[i] < 32 || val[i] > 126) {
            Print("Invalid symbol in string: ", val);
            return "";
        }
    }
    // Append NULL terminator
    return val + "\0";
}

// Function to handle empty fields
string MakeFieldHandleEmpty(const string &val) {
    if (val == NULL) {
        Print("Cannot send NULL to TWS");
        return "";
    }
    // Handle unset values
    if (val == "UNSET_INTEGER" || val == "UNSET_DOUBLE") {
        return MakeField("");
    }
    if (val == "DOUBLE_INFINITY") {
        return MakeField("INF");
    }
    return MakeField(val);
}

// Function to read a message (size prefix and payload)
bool ReadMsg(const uchar &buf[], int &size, string &text, uchar &remainingBuf[]) {
    if (ArraySize(buf) < 4) {
        size = 0;
        text = "";
        ArrayCopy(remainingBuf, buf);
        return false;
    }
    // Unpack the size prefix (big-endian)
    size = (buf[0] << 24) | (buf[1] << 16) | (buf[2] << 8) | buf[3];
    if (ArraySize(buf) - 4 >= size) {
        text = "";
        for (int i = 0; i < size; i++) {
            text += CharToString(buf[4 + i]);
        }
        ArrayResize(remainingBuf, ArraySize(buf) - (4 + size));
        ArrayCopy(remainingBuf, buf, 0, 4 + size);
        return true;
    } else {
        size = 0;
        text = "";
        ArrayCopy(remainingBuf, buf);
        return false;
    }
}

// Function to read fields separated by NULL characters
string[] ReadFields(const uchar &buf[]) {
    string fields[];
    string buffer = CharArrayToString(buf);
    int start = 0;
    int pos = StringFind(buffer, "\0", start);
    while (pos != -1) {
        string field = StringSubstr(buffer, start, pos - start);
        ArrayResize(fields, ArraySize(fields) + 1);
        fields[ArraySize(fields) - 1] = field;
        start = pos + 1;
        pos = StringFind(buffer, "\0", start);
    }
    return fields;
}
