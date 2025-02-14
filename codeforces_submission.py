import requests
from bs4 import BeautifulSoup
import os
import git

# Your Codeforces handle
CODEFORCES_HANDLE = "your_handle"
GITHUB_REPO_PATH = r"C:\Users\Lychee\Codeforces"  # Update this to your local GitHub repo path

# Fetch submissions
url = f"https://codeforces.com/api/user.status?handle=archi_998&from=1&count=1000"
response = requests.get(url)
data = response.json()

# Ensure successful API response
if data["status"] != "OK":
    print("Error fetching Codeforces data")
    exit()

submissions = data["result"]

# Directory to store submissions
save_dir = os.path.join(GITHUB_REPO_PATH, "submissions")
os.makedirs(save_dir, exist_ok=True)

# Process and save only accepted solutions
for submission in submissions:
    if submission["verdict"] == "OK":
        # Handle missing contestId
        contest_id = submission['problem'].get('contestId', None)
        problem_index = submission['problem']['index']
        
        if contest_id is None:
            print(f"Skipping submission with problem {problem_index}: Missing contestId")
            continue
        
        problem_name = f"{contest_id}_{problem_index}.cpp"
        file_path = os.path.join(save_dir, problem_name)

        # Get the URL for the submission's code
        submission_url = f"https://codeforces.com/contest/{contest_id}/submission/{submission['id']}"

        # Fetch the submission page
        submission_response = requests.get(submission_url)
        soup = BeautifulSoup(submission_response.text, 'html.parser')

        # Find the code in the submission page (adjust based on the HTML structure)
        code_block = soup.find('div', class_='program-source')

        if code_block:
            code = code_block.get_text(strip=True)
        else:
            code = f"// No code found for {problem_name}\n"

        # Write the real code to the file
        with open(file_path, "w") as file:
            file.write(code)

print("Saved accepted submissions successfully!")

def push_to_github():
    try:
        repo = git.Repo(GITHUB_REPO_PATH)
        repo.git.add(A=True)
        repo.index.commit("Updated accepted Codeforces solutions")
        origin = repo.remote(name="origin")
        origin.push()
        print("✅ Pushed to GitHub successfully!")
    except git.exc.GitCommandError as e:
        print(f"❌ Git Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

push_to_github()
