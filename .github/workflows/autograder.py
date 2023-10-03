"""
Github Actions Autograder
"""
import os
import sys
import json
import pathlib
from subprocess import Popen, PIPE

PATH = pathlib.Path(__file__).parent.parent.parent.absolute()

def main():
    test_file = json.load(open(os.path.join(PATH,".github", "workflows","testcases.json"), "r"))
    file = test_file.get("file_name")
    # Run the lab with the autograder test cases
    print(f"Running {test_file.get('file_name')}")
    # Compile and run the lab and capture the output
    for test in test_file.get("test_cases"):
        stdout, stderr = Popen(
                f"javac {os.path.join(PATH,file)} && java {os.path.join(PATH,file)} " + test.get("input"),
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            shell=True).communicate()
        # Check if the output matches the expected output
        decoded_stdout: str = stdout.decode("utf-8").strip()
        expected_output: str = test.get("expected_output").strip()
        print(f"Running test case: {test.get('input')}")
        if decoded_stdout == expected_output:
            print(f"Expected: {expected_output}")
            print(f"Received: {decoded_stdout}")
        else:
            print(f"Expected: {expected_output}")
            print(f"Received: {decoded_stdout}")
            raise RuntimeError("❌ Test case failed")
    print("✅ All tests passed")
        
if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(e)
        sys.exit(1)