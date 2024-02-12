import subprocess
from concurrent.futures import ProcessPoolExecutor
import sys
import random

def run_agent(strategy):
    """
    Executes the script.py with a given argument.
    """
    # Construct the command to run the Python script with the specified argument
    command = ['python', 'run_agent.py', strategy]
    # Execute the command
    subprocess.run(command)

def main(agents_n):
    # Arguments to pass to the script
    strategies = [
        'Speak like a gen-z', 
        'Be very bold', 
        'Pretend you are a wizard',
        'Extract maximum value by moving fast and breaking things',
        'Be very sneaky. Try to hide your strategy',
        'First mover wins, second mover loses, you cannot hesitate',
    ]

    strategies = random.choices(strategies, k=agents_n)

    # Using ProcessPoolExecutor to run scripts in parallel
    with ProcessPoolExecutor() as executor:
        # Map the run_script function to the arguments
        executor.map(run_agent, strategies)

if __name__ == '__main__':
    agents_n = 3 if len(sys.argv) < 2 else int(sys.argv[1])

    main(agents_n)