# Deployment Guide
**How to Deploy Changes to Physics of Faith Visualizations**

**Last Updated:** October 8, 2025  
**Purpose:** Step-by-step guide for deploying updates to GitHub and Cloudflare Pages

---

## 🚀 **QUICK DEPLOYMENT (auto-deploy.bat)**

### **For Standard Updates:**

```bash
# Double-click this file in repository root
auto-deploy.bat
```

**What it does:**
1. Runs `python build.py` to update gallery.json and collections.json
2. Stages all changes with `git add .`
3. Commits with timestamp
4. Pushes to GitHub
5. Triggers Cloudflare Pages deployment

**When to use:**
- Added new images to `/images/`
- Created new collection
- Updated visualizations
- Minor content changes

---

## 📋 **MANUAL DEPLOYMENT (Step-by-Step)**

### **1. Update Gallery Files**

```powershell
# Run build script
python build.py
```

**Verifies:**
- `/images/` scanned for new images
- `/collections/` scanned for featured sets
- `gallery.json` updated
- `collections.json` updated

### **2. Check Changes**

```powershell
# See what changed
git status

# Review specific files
git diff filename.md
```

### **3. Stage Changes**

```powershell
# Stage all changes
git add .

# OR stage specific files
git add _admin/
git add papers/complete/
git add research/framework/
```

### **4. Commit Changes**

```powershell
# Commit with descriptive message
git commit -m "Descriptive message about changes"
```

**Commit Message Format:**
```
Type: Brief description

- Detailed point 1
- Detailed point 2
- Detailed point 3
```

**Types:**
- `Add:` - New content
- `Update:` - Modified content
- `Fix:` - Bug fixes
- `Refactor:` - Reorganization
- `Docs:` - Documentation updates

### **5. Push to GitHub**

```powershell
# Push to main branch
git push

# Or push to specific branch
git push origin branch-name
```

### **6. Verify Deployment**

**GitHub:**
- Visit: https://github.com/YellowKidokc/physics-of-faith-visualizations
- Check latest commit appears
- Review "Actions" tab for any issues

**Cloudflare Pages:**
- Wait 1-2 minutes for deployment
- Visit: https://physics-of-faith-visualizations.pages.dev
- Verify changes are live
- Check console for errors

---

## 🔄 **COMMON DEPLOYMENT SCENARIOS**

### **Scenario 1: New Paper Complete**

```powershell
# 1. Move paper to complete folder
Move-Item "PAPER-X-NAME.md" "papers/complete/0X-name.md"

# 2. Update status documents
# Edit MASTER-DOCUMENT-INDEX.md
# Edit PUBLIC-RELEASE-STRATEGY.md
# Edit _admin/TAG-SYSTEM.md

# 3. Build and deploy
python build.py
git add .
git commit -m "Add: Complete Paper #X - Title"
git push
```

### **Scenario 2: New Visualization Collection**

```powershell
# 1. Create collection folder
New-Item -ItemType Directory "collections/new-collection"

# 2. Add files
# - index.html
# - cover.jpg/png
# - meta.json
# - visualization files

# 3. Build and deploy
python build.py
git add .
git commit -m "Add: New collection - Collection Name"
git push
```

### **Scenario 3: Major Reorganization**

```powershell
# 1. Create new folder structure
# (See REPOSITORY-STRUCTURE.md)

# 2. Move files systematically
# Use PowerShell Move-Item or manual drag-drop

# 3. Update all internal links
# Check LINKING-MAP.md for references

# 4. Verify build still works
python build.py

# 5. Deploy
git add .
git commit -m "Refactor: Reorganize repository structure"
git push
```

### **Scenario 4: Adding Images in Bulk**

```powershell
# 1. Copy images to /images/ or /images/subfolder/
Copy-Item "source\*.png" "images\"

# 2. Optional: Add descriptions
# Create matching .txt files in /descriptions/

# 3. Build and deploy
python build.py
git add .
git commit -m "Add: Bulk import of X images"
git push
```

### **Scenario 5: Research Document Update**

```powershell
# 1. Edit research document
# research/framework/MASTER-EQUATION-BLUEPRINT.md

# 2. Update linking if needed
# Check _admin/LINKING-MAP.md

# 3. Deploy
git add research/
git commit -m "Update: Master Equation Blueprint - [what changed]"
git push
```

---

## ⚠️ **TROUBLESHOOTING**

### **Problem: Merge Conflict**

```powershell
# 1. Pull remote changes
git pull

# 2. Resolve conflicts manually
# Edit conflicted files, remove conflict markers

# 3. Stage resolved files
git add conflicted-file.md

# 4. Complete merge
git commit -m "Resolve merge conflict in [file]"
git push
```

### **Problem: Build.py Fails**

```powershell
# 1. Check Python installation
python --version

# 2. Verify file paths
# Ensure /images/ and /collections/ exist

# 3. Check for invalid files
# Remove any corrupt images or HTML

# 4. Run build with error output
python build.py 2>&1 | Tee-Object -FilePath "build-error.log"
```

### **Problem: Cloudflare Not Updating**

**Check:**
1. GitHub commit successful? (Check GitHub.com)
2. Cloudflare Pages deployment triggered? (Check Cloudflare dashboard)
3. Cache issue? (Hard refresh: Ctrl+Shift+R)
4. Build errors? (Check Cloudflare build logs)

**Fix:**
```powershell
# Force rebuild by touching a file
"" | Out-File -Append "index.html"
git add index.html
git commit -m "Trigger rebuild"
git push
```

### **Problem: Large Files Won't Push**

```powershell
# Check file sizes
Get-ChildItem -Recurse | Where-Object {$_.Length -gt 50MB}

# Add large files to .gitignore
Add-Content .gitignore "path/to/large/file.psd"

# Use Git LFS for necessary large files
git lfs install
git lfs track "*.psd"
git add .gitattributes
git commit -m "Add Git LFS for large files"
```

---

## 🎯 **DEPLOYMENT CHECKLIST**

### **Before Deploying:**
- [ ] Run `python build.py` successfully
- [ ] Check `git status` for unexpected changes
- [ ] Review changes with `git diff`
- [ ] Verify no sensitive data in commits
- [ ] Test locally if possible (open index.html)

### **During Deployment:**
- [ ] Use descriptive commit message
- [ ] Stage only intended files
- [ ] Push to correct branch
- [ ] Monitor push for errors

### **After Deployment:**
- [ ] Verify GitHub shows new commit
- [ ] Wait 1-2 minutes for Cloudflare
- [ ] Check live site for changes
- [ ] Test new features/pages
- [ ] Clear browser cache if needed

---

## 📅 **SCHEDULED DEPLOYMENTS**

### **Monthly Paper Releases:**

**November 2025: Paper #1**
```powershell
# Prepare Paper #1 for public
Move-Item "papers/complete/01-logos-principle.md" "papers/published/"
# Create PDF version
# Create Substack post
# Deploy and announce
```

**December 2025: Paper #13**
```powershell
# Same process for Paper #13
```

**Monthly Cadence:**
- Week 1: Prepare content
- Week 2: Internal review
- Week 3: Finalize and deploy
- Week 4: Promote and gather feedback

---

## 🔐 **SECURITY BEST PRACTICES**

### **Don't Commit:**
- API keys or passwords
- Personal email addresses
- Private research data
- Unpublished proprietary work
- Large binary files (>50MB)

### **Do Commit:**
- Published papers
- Public visualizations
- Documentation
- Code and scripts
- Small images (<10MB)

### **Use .gitignore for:**
```
# Sensitive
.env
secrets.txt
private/

# Large files
*.psd
*.ai
*.sketch
archive_2/

# System files
.DS_Store
Thumbs.db
```

---

## 🛠️ **ADVANCED DEPLOYMENT**

### **Branch Strategy:**

**Main Branch:**
- Production-ready content only
- Always deployable
- Direct pushes for small changes

**Development Branch:**
```powershell
# Create dev branch
git checkout -b development

# Make experimental changes
# ... work ...

# Merge back when ready
git checkout main
git merge development
git push
```

**Feature Branches:**
```powershell
# For major features
git checkout -b feature/master-equation-collection

# ... work ...

# Merge via pull request on GitHub
```

### **Rollback Strategy:**

```powershell
# View commit history
git log --oneline

# Rollback to previous commit
git revert HEAD

# Or reset to specific commit (DANGER!)
git reset --hard commit-hash
git push --force  # Use with caution!
```

---

## 📊 **DEPLOYMENT LOGS**

### **Track Deployments:**

```powershell
# Create deployment log entry
$date = Get-Date -Format "yyyy-MM-dd HH:mm"
$msg = "Deployed: Paper #11 enhanced version"
Add-Content "DEPLOYMENT-LOG.txt" "$date - $msg"
```

### **Example Log:**
```
2025-10-08 14:30 - Initial repository structure created
2025-10-08 15:45 - Added AI consciousness research documents
2025-10-08 16:20 - Created Master Equation Blueprint
2025-10-08 17:00 - Organized admin and tagging system
```

---

## 🎯 **DEPLOYMENT STATUS**

### **Current Setup:**
- ✅ GitHub repository connected
- ✅ Cloudflare Pages auto-deploy active
- ✅ Build script functional (build.py)
- ✅ Auto-deploy script created (auto-deploy.bat)
- ✅ Folder structure organized
- ✅ Linking system established
- ✅ Tagging system defined

### **Next Deployments:**
1. File reorganization (move to new structure)
2. Master Equation collection creation
3. Monthly paper releases (starting November)
4. Visualization enhancements
5. Archive cleanup

---

**Status:** Deployment system ready and functional.

**Usage:** Follow this guide for all deployments to maintain consistency.

**Goal:** Smooth, reliable deployments every time.

---

**Deploy with confidence!** 🚀
