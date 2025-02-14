import requests
import json
import os
import git

# Your Codeforces handle
CODEFORCES_HANDLE = "your_handle"  # Change to your Codeforces username
GITHUB_REPO_PATH = r"C:\Users\Lychee\Codeforces"  # Change this to your local GitHub repo path

# Fetch submissions
url = f"https://codeforces.com/api/user.status?handle=archi_998&from=1&count=1000"
response = requests.get(url)
data = response.json()

# Ensure successful API response
if data.get("status") != "OK":
    print("Error fetching Codeforces data")
    exit()

submissions = data["result"]

# Directory to store submissions
save_dir = os.path.join(GITHUB_REPO_PATH, "submissions")
os.makedirs(save_dir, exist_ok=True)

# Process and save only accepted solutions
for submission in submissions:
    if submission.get("verdict") == "OK":
        problem = submission.get("problem", {})
        
        # Handle missing contestId
        contest_id = problem.get("contestId", "GYM")  # Default "GYM" for non-contest problems
        index = problem.get("index", "UNKNOWN")
        
        problem_name = f"{contest_id}_{index}.cpp"
        file_path = os.path.join(save_dir, problem_name)

        # Fetch real solution code (requires authentication & web scraping)
        # Here, we assume a placeholder function `fetch_solution_code(submission_id)`
        submission_id = submission.get("id")
        code = f"// Accepted solution for {problem_name}\nint main() {{ return 0; }}"  # Dummy content
        
        with open(file_path, "w") as file:
            file.write(code)

print("Saved accepted submissions successfully!")

# Push changes to GitHub
def push_to_github():
    try:
        repo = git.Repo(GITHUB_REPO_PATH)
        repo.git.add(all=True)
        repo.index.commit("Updated accepted Codeforces solutions")
        origin = repo.remote(name="origin")
        origin.push()
        print("Pushed to GitHub successfully!")
    except Exception as e:
        print(f"Error pushing to GitHub: {e}")

push_to_github()
