## 1. Team Workflow: Branches and Pull Requests
We follow a simplified "GitHub Flow" to manage our code changes.

**1.1. The `main` Branch**
The `main` branch represents the stable, production-ready code.

Direct pushes to main are strictly forbidden. All changes must go through a Pull Request.

Always keep your local main branch updated.

**1.2. Feature Branching**
For every new task (feature, bug fix, improvement), you must create a new branch.

- **Start from `main`:**
Always ensure your local `main` is up-to-date before creating a new branch.

```
git checkout main
git pull origin main
```

- **Create your Feature Branch:**
Choose a descriptive name.

```
git checkout -b feature/your-task-name
# Examples:
# git checkout -b feature/implement-virtual-card-creation
# git checkout -b bugfix/fix-card-status-display
# git checkout -b chore/update-bitnob-sdk
```

- **1.3. Developing and Committing**
As you work on your task:

i. Make your code changes.

ii. Stage your changes:

```
git add . # Or git add <specific_file>
```

iii. Commit your changes:
Write clear and concise commit messages.

```
git commit -m "feat: Implement Bitnob virtual card creation endpoint"
# Example: "fix: Correct virtual card status mapping"
# Example: "chore: Update Django to latest patch version"
```

**Commit Message Best Practices:**
- Start with a type (feat, fix, chore, docs, style, refactor, test, build, ci).

- Followed by a colon and a space.

- Concise, imperative mood summary (e.g., "Add...", "Fix...", "Update...").

- (Optional) Leave a blank line, then add a more detailed explanation.

iv. Push your branch to GitHub:
The first time you push a new branch:

```
git push -u origin feature/your-task-name
```

For subsequent pushes on the same branch:

```
git push
```

Push frequently! This serves as a backup and allows teammates to see your progress.

- **1.4. Keeping Your Branch Updated with `main`**
While you're working, others might merge their changes into `main`. To avoid large conflicts later, regularly pull `main` into your feature branch:

Ensure you are on your feature branch:

```
git checkout feature/your-task-name
```

Pull and merge `main` into your branch:

```
git pull origin main
```

- Resolve any merge conflicts: Git will guide you through this. After resolving, `git add` the conflicted files and `git commit` the merge.

- `git push` your updated feature branch.

- **1.5. Creating a Pull Request (PR)**
When your feature/bug fix is complete, tested, and ready for review:

i. Ensure your branch is pushed and up-to-date.

git push

ii. Go to GitHub: Navigate to our repository. GitHub will usually prompt you to create a Pull Request for your recently pushed branch.

iii. Configure the PR:

- Base branch: main (this is where your changes will eventually go).

- Compare branch (head): Your feature branch (e.g., feature/implement-virtual-card-creation).

iv. Write a Clear PR Description:

Title: A concise summary of the PR's purpose.

Description:

What problem does this PR solve?

What changes were made?

How can reviewers test this functionality?

Any known limitations or future considerations.

Reference any related issues (e.g., "Closes #123", "Resolves #456").

Assign Reviewers: Request reviews from your teammates.


- **1.6. Code Review and Iteration**
i. Reviewers provide feedback: Your teammates will review your code on GitHub, leaving comments and suggestions.

ii. Address feedback: Make necessary changes in your local feature branch, commit them, and git push them. These new commits will automatically appear in the open PR.

iii. Discuss: Use the PR comments for discussion and clarification.


- **1.7. Merging and Cleaning Up**
Once the PR is approved and all discussions are resolved:

i. Merge the Pull Request: The designated team lead or an approved reviewer will merge the PR into the main branch on GitHub.

ii. Delete the Feature Branch: After merging, GitHub usually offers a button to delete the feature branch. Do this to keep the repository clean.

iii. Update your Local main and Delete Local Branch:

```
git checkout main
git pull origin main # Get the newly merged changes
git branch -d feature/your-task-name # Delete your local feature branch
```

(Use `git branch -D` if Git complains about unmerged changes, but try to avoid this by always merging main into your feature branch before the final PR merge).
