@echo off
echo Building gallery...
python build.py

echo Committing changes...
git add .
git commit -m "Auto-update: %date% %time%"

echo Pushing to GitHub...
git push

echo ✅ Done! Your site will update on Cloudflare in ~1 minute.
pause

