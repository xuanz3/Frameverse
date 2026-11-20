#!/bin/bash
# FRAMEVERSE — publish the existing, authentic local Git history to GitHub.
# This script does not rewrite timestamps or force-push.
cd "$(dirname "$0")" || exit 1
printf '\nFRAMEVERSE — GitHub publisher\n\n'
if ! command -v git >/dev/null 2>&1; then
  echo 'Git is not installed. Install GitHub Desktop: https://desktop.github.com/'
  echo 'Then add this FRAMEVERSE folder as an existing local repository.'
  read -r -p 'Press Enter to exit... '
  exit 1
fi
if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo 'The .git folder is missing. Use the special GitHub upload ZIP, not the website-only ZIP.'
  read -r -p 'Press Enter to exit... '
  exit 1
fi
if [ "$(git branch --show-current)" != 'main' ]; then
  echo 'Please select main before publishing.'
  read -r -p 'Press Enter to exit... '
  exit 1
fi
if ! git remote get-url origin >/dev/null 2>&1; then
  git remote add origin https://github.com/xuanz3/FRAMEVERSE.git
fi
printf 'Destination: %s\n' "$(git remote get-url origin)"
printf 'Branch: main\n\n'
printf 'Your browser may open for GitHub authentication.\n\n'
if git push -u origin main; then
  printf '\nPublished successfully: https://github.com/xuanz3/FRAMEVERSE\n'
else
  printf '\nPublish did not complete.\n'
  printf 'If GitHub sign-in was blocked, open GitHub Desktop, add this FRAMEVERSE folder as a local repository and select Push origin.\n'
  printf 'Get GitHub Desktop: https://desktop.github.com/\n'
fi
printf '\n'
read -r -p 'Press Enter to close... '
