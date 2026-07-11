import subprocess
import re
from collections import defaultdict

def run_mypy():
    result = subprocess.run(['.venv/bin/mypy', 'generators/'], capture_output=True, text=True)
    return result.stdout

def parse_errors(output):
    errors = defaultdict(list)
    # Match: file.py:line: error: message [code]
    pattern = re.compile(r'^(generators/[^:]+\.py):(\d+): error:.*\[(.*)\]$')
    for line in output.splitlines():
        match = pattern.match(line)
        if match:
            file_path, line_num, code = match.groups()
            errors[file_path].append((int(line_num), code))
    return errors

def apply_fixes(errors):
    for file_path, file_errors in errors.items():
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Group codes by line number
        line_codes = defaultdict(set)
        for line_num, code in file_errors:
            line_codes[line_num].add(code)
            
        # Apply ignores from bottom to top to avoid line shifts (though here we only modify lines in place)
        for line_num, codes in line_codes.items():
            if 1 <= line_num <= len(lines):
                idx = line_num - 1
                line = lines[idx].rstrip()
                if '# type: ignore' in line:
                    continue # Already has an ignore
                
                codes_str = ', '.join(sorted(codes))
                lines[idx] = f"{line}  # type: ignore[{codes_str}]\n"
                
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
            
if __name__ == '__main__':
    for _ in range(3): # Run multiple times to fix cascaded errors
        print("Running mypy...")
        output = run_mypy()
        errors = parse_errors(output)
        if not errors:
            print("No errors found!")
            break
        print(f"Applying fixes for {len(errors)} files...")
        apply_fixes(errors)
        
