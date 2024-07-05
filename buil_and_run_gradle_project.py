import os
import subprocess

def build_and_run_gradle_project(project_path, gradle_path):
    # Check if the given path is a valid directory
    if not os.path.isdir(project_path):
        print(f"The provided path {project_path} is not a valid directory.")
        return

    # Check if the project has a build.gradle file
    build_gradle_path = os.path.join(project_path, 'build.gradle')
    if not os.path.isfile(build_gradle_path):
        print(f"No build.gradle file found in the directory {project_path}.")
        return

    # Run Gradle tasks
    try:
        # Navigate to the project directory
        os.chdir(project_path)

        # Execute Gradle clean and build
        subprocess.check_call([gradle_path, 'clean', 'build'])
        print("Gradle project built successfully.")

        # Execute Gradle bootRun
        subprocess.check_call([gradle_path, 'bootRun'])
        print("Gradle project is up and running.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Gradle tasks: {e}")
    except FileNotFoundError:
        print("Gradle is not installed or not found in your PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Define the path to your existing Gradle project and Gradle executable
project_path = '/path/to/your/gradle/project'
gradle_path = '/path/to/gradle/bin/gradle'  # Update this to your Gradle executable path

# Build and run the Gradle project
build_and_run_gradle_project(project_path, gradle_path)
