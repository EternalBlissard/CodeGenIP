from prompt_handler import handle_code_generator_prompt, handle_test_case_generator_prompt, handle_test_validator_prompt, handle_reasoner_prompt

import random
import string
import re
import subprocess

def extract_output(pattern, text):
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    return None


def extract_all_outputs(pattern,text):
    # Regular expression to match content between #OUTPUTSTART\n and #OUTPUTEND
    # pattern = r'#OUTPUTSTART\n(.*?)#OUTPUTEND'
    
    # Using re.findall to find all occurrences
    outputs = re.findall(pattern, text, re.DOTALL)
    
    return outputs

def generate_filename():
    # Generate a random alphabetic character for the first character
    first_char = random.choice(string.ascii_letters)
    
    # Generate the remaining 19 characters, which can be letters or digits
    remaining_chars = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(19))
    
    # Combine the first character with the remaining characters to form the 20-character file name
    filename = first_char + remaining_chars
    
    return filename

def multi_agent_cycle(user_prompt=None,temperature=0.5,max_tokens=1024,top_p=0.5, reasoner_num = 3, test_case_num = 7):
    if(user_prompt is None or user_prompt==""):
        return "No prompt given"
    filename = None
    if(filename is None):
        filename = generate_filename()
    currCorrect = 0
    bestCode = None
    for idx in range(reasoner_num):
        reasonor_res = extract_output(r'#OUTPUTSTART\n(.*?)\n#OUTPUTEND',handle_reasoner_prompt(user_prompt,temperature=temperature+(0.05)*idx,max_tokens = max_tokens+((512)*idx)))
        code_gen_res = extract_output(r'#CODESTART\n(.*?)#CODEEND',handle_code_generator_prompt(reasonor_res,temperature=temperature+(0.05)*idx,max_tokens = max_tokens+((512)*idx)))
        test_gen_res = extract_all_outputs(r'#TESTCASESTART\n(.*?)\n#TESTCASEEND', handle_test_case_generator_prompt(reasonor_res+f"LIMIT OUTPUT TO{test_case_num} TESTCASES USING THE STEPS! MAKE SURE EDGE CASES AREN'T MISSED",temperature=temperature+(0.05)*idx,max_tokens = max_tokens+((512)*idx)))
        fresh_tc = []
        for test_gen in test_gen_res:
            new_prompt = f"""
#SUBPROBLEMSTART
{reasonor_res}
#SUBPROBLEMEND
#TESTCASESTART
{test_gen}
#TESTCASEEND
"""
            val_res = extract_output(r'#OUTPUTSTART\n(.*?)\n#OUTPUTEND',handle_test_validator_prompt(new_prompt))
            if(val_res=='CORRECT'):
                fresh_tc.append(test_gen)

        with open(filename+'.py','w') as file:
            file.write("import pytest\n\n")
            code_split = code_gen_res.split('\n')
            file.write(code_gen_res)
            # print('\n'.join(new_code_split))

            # f.write(make_statement1(1,extract_output(r'#TESTCASEINPUTSTART\n(.*?)\n#TESTCASEINPUTEND',test_gen_res[0]),extract_output(r'#TESTCASEOUTPUTSTART\n(.*?)#TESTCASEOUTPUTEND',test_gen_res[0])))
            file.write("@pytest.mark.parametrize(\"n, expected\", [\n")
            
            # Loop through the test cases and write them to the file
            for case in fresh_tc:
                input_result = extract_output(r'#TESTCASEINPUTSTART\n(.*?)\n#TESTCASEINPUTEND', case)
                output_result = extract_output(r'#TESTCASEOUTPUTSTART\n(.*?)\n#TESTCASEOUTPUTEND',case)
                file.write(f"    ('{input_result}', '{output_result}'),  #\n")
            
            # Close the parametrize list
            file.write("])\n\n")
            
            # Write the test function using the parametrize decorator
            file.write("def test_statement(n, expected):\n")
            file.write("    result = decoder(n)\n")
            file.write("    assert result == expected\n")
        result = subprocess.run(
        ['pytest', filename+'.py'],  # Specify the test file here
        capture_output=True,  # Capture stdout and stderr
        text=True             # Ensure the output is returned as a string (not bytes)
        )
        # print(result)
        # Get the output and error
        output = result.stdout  # The standard output from pytest (test results)
        error = result.stderr   # The error output (if any)
        # print("Error",error)
        # print(error is None)
        # print(error=="")
        

        # Use regular expressions to find the counts of passed and failed tests
        failed_tests = int(len(re.findall(r'FAIL', output))/2)
        passed_tests = len(fresh_tc) - failed_tests

        command = ['rm', '-f', filename + ".py"]

        try:
            # Run the command
            subprocess.run(command, check=True, shell=True)
            print(f"File '{filename}' has been deleted.")
        except subprocess.CalledProcessError as e:
            print(f"Error: Could not delete file '{filename}'. {e}")

        if(failed_tests == 0):
            return code_gen_res + "\n\n DECODER IS SOLELY TO TACKLE INPUTS FROM FILE READING"

        if(passed_tests>currCorrect):
            bestCode = code_gen_res

    return bestCode + "\n\n DECODER IS SOLELY TO TACKLE INPUTS FROM FILE READING"
        





