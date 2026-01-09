from utils import add_numbers

def run_calculation():
    val1 = 10
    val2 = 5
    
    # ERROR 1: Calling a function that doesn't exist (should be add_numbers)
    # This forces the bot to check utils.py to see what functions are available.
    result = perform_addition(val1, val2) 
    
    print(f"The sum of {val1} and {val2} is: {result}")

if __name__ == "__main__":
    run_calculation()
