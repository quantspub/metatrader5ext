def make_message(command, sub_command, parameters):
    """
    Constructs a message in the format FXXX^Y^<parameters>.

    :param command: The command identifier (e.g., "F123").
    :param sub_command: The sub-command or parameter (e.g., "Y").
    :param parameters: A list of additional parameters (e.g., ["param1", "param2"]).
    :return: A formatted message string.
    """
    try:
        # Join the parameters with the '^' delimiter
        params_str = '^'.join(parameters)
        
        # Construct the message in the required format
        message = f"{command}^{sub_command}^{params_str}"
        
        return message
    
    except Exception as e:
        # Handle any errors that occur during message construction
        return f"Error: {str(e)}"

# Example usage:
command = "F123"
sub_command = "Y"
parameters = ["param1", "param2", "param3"]

message = make_message(command, sub_command, parameters)
print(message)


def parse_response_message(response_message):
    """
    Parses response message in the format FXXX^Y^<parameters>.
    The <parameters> part contains the server's response data.
    Handles hidden '^' delimiters and ensures data is properly extracted.

    :param response_message: The response or message string to parse.
    :return: A dictionary containing the command, sub-command, and data.
    """
    try:
        # Split the response or message by the '^' delimiter
        parts = response_message.split('^')
        
        # Ensure the response or message has at least three parts
        if len(parts) < 3:
            raise ValueError("Invalid format. Expected at least three parts separated by '^'.")
        
        # Extract the command and sub-command
        command = parts[0]
        sub_command = parts[1]
        
        # Extract the data (all remaining parts)
        data = parts[2:]
        
        # Find the index of the last non-empty data element
        last_non_empty_index = len(data) - 1
        while last_non_empty_index >= 0 and data[last_non_empty_index] == '':
            last_non_empty_index -= 1
        
        # Slice the data list up to the last non-empty index
        data = data[:last_non_empty_index + 1]
        
        # Check for hidden '^' delimiters in data (empty strings in the middle)
        if '' in data:
            raise ValueError("Invalid format. Hidden '^' delimiters detected in data.")
        
        # Return the parsed components as a dictionary
        return {
            'command': command,
            'sub_command': sub_command,
            'data': data
        }
    
    except Exception as e:
        # Handle any errors that occur during parsing
        return {
            'error': str(e)
        }

# Example usage:
response_message = "F123^Y^param1^param2^param3^^"
parsed_data = parse_response_message(response_message)
print(parsed_data)



