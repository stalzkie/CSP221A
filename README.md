# CSP221A Remedial — Submission Instructions

## 1. Fork this repository

Click **Fork** at the top of this repo's GitHub page. This creates your own copy of the repo under your GitHub account.

## 2. Clone your fork

```
git clone https://github.com/<your-username>/CSP221A.git
cd CSP221A
```

## 3. Find your folder

Go to your section, then the problem you were assigned:

```
BSCS4B/remedial/problem <N>/
BSCS4C/remedial/problem <N>/
```

Inside that problem folder, find the folder named with **your own student ID number**. That is your folder — read `instructions.md` in the problem folder for what to build, then put your work inside your ID folder.

If you don't see a folder with your ID number, contact your instructor before starting.

## 4. Add your work

Inside your ID folder, add your solution file(s) and write-up exactly as described in that problem's `instructions.md`.

## 5. Commit and push

Make **only one commit** on your forked repo — your final, finished work. Do not commit work-in-progress.

```
git add .
git commit -m "Add my solution"
git push origin main
```

## 6. Open a Pull Request

Only open a Pull Request when you are submitting your **final answer** — not a draft, not a work in progress.

1. Go to your fork on GitHub.
2. Click **Contribute**, then **Open pull request** (or go to the **Pull requests** tab and click **New pull request**).
3. Confirm the base repository is the original `CSP221A` repo (base: `main`) and the head is your fork (compare: `main`).
4. Give the PR a clear title (e.g., your student ID and problem number) and click **Create pull request**.

Your instructor reviews submissions through this Pull Request.

## Academic Integrity

- **Only one commit** is allowed on your forked repo. Multiple commits, force-pushes to rewrite history, or amending after you've opened your PR are not permitted.
- **Any AI-generated code that is caught will result in an automatic 0.**
- You will be asked **individually, in class**, to explain your code. Be prepared to defend every line you submit.
