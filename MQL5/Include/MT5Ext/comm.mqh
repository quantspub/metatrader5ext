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
