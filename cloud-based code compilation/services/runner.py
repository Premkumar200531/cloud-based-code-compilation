import subprocess
import os
import tempfile
import time
import uuid

class CodeRunner:
    @staticmethod
    def run_code(language, code, stdin_input="", timeout=5):
        """
        Executes code for a given language.
        :param language: Language object (DB model)
        :param code: Source code string
        :param stdin_input: Input for the program
        :param timeout: Execution timeout in seconds
        :return: Dict result
        """
        
        # Create a unique temporary directory for this run
        run_id = str(uuid.uuid4())
        temp_dir = tempfile.mkdtemp(prefix=f"run_{run_id}_")
        
        try:
            # Determine file extension
            filename = "main" # default name
            ext = ""
            if language.name.lower() == "python":
                ext = ".py"
            elif language.name.lower() == "c":
                ext = ".c"
            elif language.name.lower() == "c++":
                ext = ".cpp"
            elif language.name.lower() == "java":
                ext = ".java"
                filename = "Main" # Java often requires class name match
            elif language.name.lower() == "javascript":
                ext = ".js"
            
            filepath = os.path.join(temp_dir, filename + ext)
            
            # Write code to file
            with open(filepath, "w") as f:
                f.write(code)
            
            # Prepare compile command
            compile_cmd = language.compile_cmd
            run_cmd = language.run_cmd
            
            compile_output = ""
            if compile_cmd:
                # Format the command
                # e.g. "gcc {file} -o {out}"
                out_path = os.path.join(temp_dir, "run_executable")
                if os.name == 'nt':
                     out_path += ".exe"
                     
                formatted_compile = compile_cmd.replace("{file}", filepath).replace("{out}", out_path)
                
                start_time = time.time()
                try:
                    proc = subprocess.run(formatted_compile, shell=True, capture_output=True, text=True, timeout=10)
                    if proc.returncode != 0:
                        return {
                            "status": "compilation_error",
                            "stdout": "",
                            "stderr": proc.stderr,
                            "time_ms": int((time.time() - start_time) * 1000)
                        }
                    compile_output = proc.stdout
                except subprocess.TimeoutExpired:
                     return {"status": "timeout", "stdout": "", "stderr": "Compilation Timed Out", "time_ms": 10000}

            # Prepare run command
            # e.g. "./{out}" or "python {file}"
            if "{out}" in run_cmd:
                # Compiled executable
                # On Windows, simple execution of .exe might need full path
                exec_path = os.path.join(temp_dir, "run_executable.exe" if os.name == 'nt' else "run_executable")
                formatted_run = run_cmd.replace("{out}", exec_path)
            else:
                # Interpreted
                formatted_run = run_cmd.replace("{file}", filepath)
            
            # Run the code
            start_time = time.time()
            try:
                proc = subprocess.run(
                    formatted_run, 
                    input=stdin_input,
                    capture_output=True, 
                    text=True, 
                    timeout=timeout,
                    shell=True,
                    cwd=temp_dir # isolate somewhat by cwd
                )
                duration = int((time.time() - start_time) * 1000)
                
                return {
                    "status": "success" if proc.returncode == 0 else "runtime_error",
                    "stdout": proc.stdout,
                    "stderr": proc.stderr,
                    "time_ms": duration
                }

            except subprocess.TimeoutExpired:
                return {
                    "status": "timeout",
                    "stdout": "",
                    "stderr": "Execution Timed Out",
                    "time_ms": timeout * 1000
                }
            except Exception as e:
                return {
                    "status": "system_error",
                    "stdout": "",
                    "stderr": str(e),
                    "time_ms": 0
                }

        finally:
            # Cleanup
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except:
                pass
