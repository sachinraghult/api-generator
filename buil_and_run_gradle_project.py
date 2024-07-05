import subprocess

def run_gradle_tasks(project_path):
    # Run Gradle tasks
    try:
        subprocess.check_call(['gradle', 'clean', 'build'], cwd=project_path)
        subprocess.check_call(['gradle', 'bootRun'], cwd=project_path)
        print("Gradle project is up and running")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Gradle tasks: {e}")

# Define project path and name
project_path = '/path/to/project'
project_name = 'com.example.demo'

# start the Gradle project
run_gradle_tasks(os.path.join(project_path, project_name))