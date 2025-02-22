// Collection of misc tools for MQL5

// Logging setup
int loggerLevel = LOG_LEVEL_DEBUG; // Custom log level, adjust as needed

// Custom exception classes
class BadMessage {
public:
    string text;
    BadMessage(string _text) : text(_text) {}
};

class ClientException {
public:
    int code;
    string msg;
    string text;
    ClientException(int _code, string _msg, string _text) : code(_code), msg(_msg), text(_text) {}
};

// LogFunction decorator equivalent
class LogFunction {
private:
    string text;
    int logLevel;

public:
    LogFunction(string _text, int _logLevel) : text(_text), logLevel(_logLevel) {}

    template<typename T>
    void operator()(T& fn, string fnName, void* origSelf, void* args[], int argsCount, void* kwargs[]) {
        if (loggerLevel >= logLevel) {
            string logMsg = text + " " + fnName + " args:[";
            for (int i = 0; i < argsCount; i++) {
                logMsg += StringFormat("%p, ", args[i]);
            }
            logMsg += "] kwargs:[";
            // Assuming kwargs is an array of key-value pairs
            for (int i = 0; i < ArraySize(kwargs); i += 2) {
                logMsg += StringFormat("%s=%p, ", kwargs[i], kwargs[i + 1]);
            }
            logMsg += "]";
            Print(logMsg);
        }
        fn(origSelf, args, kwargs); // Call the original function
    }
};

// Function to get the current function name
string current_fn_name(int parent_idx = 0) {
    return __FUNCTION__; // MQL5 built-in macro for current function name
}

// Function to log attribute setting
void setattr_log(void* self, string var_name, void* var_value) {
    PrintFormat("%s %p %s=|%p|", typename(self), self, var_name, var_value);
    // Call the original __setattr__ equivalent (not directly available in MQL5)
}

// Global flag for showing unset values
bool SHOW_UNSET = true;

// Function to decode fields into specific types
template<typename T>
T decode(string s, bool show_unset = false, bool use_unicode = false) {
    if (s == NULL || StringLen(s) == 0) {
        if (show_unset) {
            if (typename(T) == "double") {
                return DBL_MAX; // Equivalent to UNSET_DOUBLE
            } else if (typename(T) == "int") {
                return INT_MAX; // Equivalent to UNSET_INTEGER
            } else {
                BadMessage("Unsupported type for empty value: " + typename(T));
            }
        } else {
            return T(0);
        }
    }

    if (typename(T) == "double") {
        if (s == "INF") {
            return DBL_MAX; // Equivalent to DOUBLE_INFINITY
        }
        return StringToDouble(s);
    } else if (typename(T) == "int") {
        return StringToInteger(s);
    } else if (typename(T) == "bool") {
        return StringToInteger(s) != 0;
    } else if (typename(T) == "string") {
        return s; // No decoding needed for strings in MQL5
    } else {
        BadMessage("Unsupported type: " + typename(T));
    }
    return T(0);
}

// Function to exercise static methods of a class
void ExerciseStaticMethods(void* klass) {
    // MQL5 does not support reflection, so this is not directly translatable
    Print("ExerciseStaticMethods is not fully supported in MQL5");
}

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
        if (val[i] < 32 || val[i] >= 128) {
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


// // Function to encode strings using a predefined alphabet-number mapping
// uchar[] EncodeString(string input)
// {
//     uchar encoded[];
//     for (int i = 0; i < StringLen(input); i++)
//     {
//         uchar ch = (uchar)StringGetCharacter(input, i);
//         ArrayResize(encoded, ArraySize(encoded) + 1);
//         encoded[ArraySize(encoded) - 1] = ch + 42;  // Simple shift encoding
//     }
//     return encoded;
// }