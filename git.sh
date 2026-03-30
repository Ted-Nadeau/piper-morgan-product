# Pull latest changes to both branches
git checkout main
git pull origin main

git checkout demo-stable-pm-008  
git pull origin demo-stable-pm-008

# Verify they're synchronized
git log --oneline -5
