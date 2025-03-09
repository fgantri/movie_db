def get_binary_input(question):
    """Gets a yes or no answer from input.
    
    Args:
        question: The question to ask the user.
        
    Returns:
        bool: True if the user answered yes, False if no.
    """
    while True:
        answer = input(f"{question.replace('?', '')}? [Y]es or [N]o: ").strip().lower()
        if answer in ["y", "yes"]:
            return True
        elif answer in ["n", "no"]:
            return False
        else:
            print('Please enter "Y" or "N"')
            continue


def get_input(prompt, empty_msg):
    """Gets a non-empty input value (simulates a required input).
    
    Args:
        prompt: The prompt to show the user.
        empty_msg: Error message to show if input is empty.
        
    Returns:
        str: The non-empty user input.
    """
    while True:
        value = input(prompt).strip()
        if value == "":
            print(empty_msg)
        else:
            return value


def get_number_input(prompt, error_msg, min_value=None, max_value=None):
    """Gets a valid number as input.
    
    Args:
        prompt: The prompt to show the user.
        error_msg: Error message to show if input is not a valid number.
        min_value: Optional minimum allowed value.
        max_value: Optional maximum allowed value.
        
    Returns:
        float: The valid numeric input.
    """
    while True:
        try:
            value = float(input(prompt))
            
            # Validate range if provided
            if min_value is not None and value < min_value:
                print(f"Value must be at least {min_value}")
                continue
                
            if max_value is not None and value > max_value:
                print(f"Value must be at most {max_value}")
                continue
                
            return value
        except ValueError:
            print(error_msg)


def get_optional_input(prompt, cast_func, error_msg):
    """Gets an optional input of type returned by cast_func or None.
    
    Args:
        prompt: The prompt to show the user.
        cast_func: The function to cast the input to the desired type.
        error_msg: Error message to show if casting fails.
        
    Returns:
        The casted value or None if input was empty.
    """
    while True:
        value = input(f"{prompt} (leave blank for no value): ")
        if value == "":
            return None
        try:
            return cast_func(value)
        except ValueError:
            print(error_msg)
            continue