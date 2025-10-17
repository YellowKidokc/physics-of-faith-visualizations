# 🚀 Cloudflare Pages Deployment Guide

## Automated Pipeline (Recommended)

The repository now ships with a Node-based static site generator and an automated Cloudflare Pages deployment workflow. Follow these steps once and every push to `main` will rebuild and publish the Syzygy Gallery automatically.

### 1. Install Dependencies Locally

```bash
npm install
npm run build
```

The build command generates the `dist/` directory with watermarked assets and the gallery homepage.

### 2. Configure Cloudflare Secrets

Add the following repository secrets in GitHub (`Settings → Secrets and variables → Actions → New repository secret`):

| Secret Name | Description |
|-------------|-------------|
| `CLOUDFLARE_ACCOUNT_ID` | Your Cloudflare account identifier |
| `CLOUDFLARE_API_TOKEN` | API token with Pages `Edit` permissions |
| `CLOUDFLARE_PROJECT_NAME` | The Cloudflare Pages project to deploy to |

### 3. Push to `main`

The workflow defined in `.github/workflows/deploy.yml` will:

1. Check out the repository
2. Install Node dependencies
3. Run `npm run build`
4. Publish the contents of `dist/` to Cloudflare Pages via `cloudflare/pages-action@v1`

> ℹ️ For manual builds or debugging you can run `npm run build` locally and inspect the generated `dist/index.html` before pushing.

### 4. (Optional) Trigger a deployment from your terminal

If you prefer to deploy directly from your machine without waiting for GitHub Actions, first build the site and then run the deployment helper:

```bash
npm run build
npm run deploy -- <your-cloudflare-pages-project>
```

The helper wraps `wrangler pages deploy` so you can set the `CLOUDFLARE_PROJECT_NAME` environment variable instead of passing the project name each time. Any additional flags (for example `--branch preview`) are forwarded to Wrangler. For environments that still call `npx wrangler deploy`, the bundled `wrangler.toml` now specifies `dist/` as a static asset directory so that command successfully publishes the same build output.

---

## Step-by-Step Instructions to Host Your Physics of Faith Site

### Method 1: Direct Upload (Easiest - 5 minutes)

#### Step 1: Prepare Your Files
1. **Zip the entire `physics-of-faith-site` folder**
   - Right-click on the folder
   - Select "Send to" → "Compressed (zipped) folder"
   - Name it `physics-of-faith-site.zip`

#### Step 2: Access Cloudflare Pages
1. **Go to Cloudflare Dashboard**: https://dash.cloudflare.com
2. **Click "Pages"** in the left sidebar
3. **Click "Upload assets"** button

#### Step 3: Deploy Your Site
1. **Drag and drop** your zip file into the upload area
2. **Enter project name**: `physics-of-faith` (or any name you prefer)
3. **Click "Deploy"**
4. **Wait 1-2 minutes** for deployment to complete

#### Step 4: Access Your Live Site
- Your site will be available at: `https://physics-of-faith.pages.dev`
- Bookmark this URL - this is your permanent site address!

---

### Method 2: GitHub Integration (Best for Updates)

#### Step 1: Create GitHub Repository
1. **Go to GitHub**: https://github.com
2. **Click "New repository"**
3. **Name**: `physics-of-faith-site`
4. **Make it Public**
5. **Click "Create repository"**

#### Step 2: Upload Your Files
1. **Click "uploading an existing file"**
2. **Drag all files** from your `physics-of-faith-site` folder
3. **Commit changes**

#### Step 3: Connect to Cloudflare Pages
1. **Go to Cloudflare Pages Dashboard**
2. **Click "Connect to Git"**
3. **Choose GitHub**
4. **Select your `physics-of-faith-site` repository**
5. **Click "Begin setup"**

#### Step 4: Configure Build Settings
- **Project name**: `physics-of-faith`
- **Production branch**: `main`
- **Build command**: `npm run build`
- **Build output directory**: `dist`
- **Click "Save and Deploy"**

---

### 🔧 Advanced Options

#### Custom Domain Setup
1. **In Cloudflare Pages dashboard**
2. **Go to your project**
3. **Click "Custom domains"**
4. **Add your domain** (e.g., `physicsoffaith.com`)
5. **Follow DNS setup instructions**

#### Environment Variables (if needed)
- **Go to Settings → Environment variables**
- **Add any API keys or configuration**

#### Preview Deployments
- **Every GitHub commit** creates a preview
- **Test changes** before going live
- **Roll back easily** if needed

---

### 📱 Mobile Optimization

Your site is already optimized for:
- ✅ **Mobile devices** (phones, tablets)
- ✅ **Desktop computers** (all screen sizes)
- ✅ **Touch interfaces** (tablet interactions)
- ✅ **High-DPI displays** (retina screens)

---

### 🎯 SEO & Sharing

#### Automatic Features
- ✅ **Meta tags** for social sharing
- ✅ **Responsive design** for mobile SEO
- ✅ **Fast loading** for search rankings
- ✅ **HTTPS security** (required by Google)

#### Share Your Site
- **Direct link**: Share your `.pages.dev` URL
- **Social media**: Cards will show preview images
- **Academic sharing**: Professional presentation ready

---

### 🔄 Updating Your Site

#### Method 1 Updates (Direct Upload)
1. **Make changes** to your HTML files
2. **Create new zip** file
3. **Go to Cloudflare Pages**
4. **Create new deployment**
5. **Upload updated zip**

#### Method 2 Updates (GitHub)
1. **Make changes** to your files
2. **Commit to GitHub**
3. **Cloudflare automatically rebuilds**
4. **Site updates** in 1-2 minutes

---

### 🚨 Troubleshooting

#### Common Issues

**Site not loading?**
- Check your zip file contains `index.html`
- Ensure file names match exactly
- Wait 5 minutes for DNS propagation

**Wrangler CLI reports "Missing entry-point"?**
- Use `npm run deploy -- <project>` or `npx wrangler pages deploy dist --project-name <project>` instead of `npx wrangler deploy`
- Confirm the `dist/` folder exists (run `npm run build`)
- Ensure your Cloudflare API token has Pages "Edit" permissions

**Animations not working?**
- Clear browser cache (Ctrl+F5)
- Try incognito/private browsing mode
- Check JavaScript console for errors

**Mobile layout broken?**
- Verify viewport meta tags
- Test on actual mobile device
- Check CSS media queries

#### Getting Help
- **Cloudflare Support**: https://support.cloudflare.com
- **Community Forums**: https://community.cloudflare.com
- **Documentation**: https://developers.cloudflare.com/pages

---

### 🎉 Success Checklist

After deployment, verify:
- [ ] **Main gallery loads** correctly
- [ ] **All three visualizations** are accessible
- [ ] **Animations work** smoothly
- [ ] **Mobile version** displays properly
- [ ] **Tooltips and interactions** function
- [ ] **Links between pages** work correctly

---

### 💡 Pro Tips

1. **Bookmark your dashboard**: Easy access for updates
2. **Test on multiple devices**: Ensure compatibility
3. **Share early and often**: Get feedback from viewers
4. **Monitor analytics**: See how people interact with your site
5. **Keep backups**: Save local copies of your files

---

### 🌟 What You've Accomplished

You now have:
- ✅ **Professional website** showcasing your groundbreaking work
- ✅ **Global hosting** with enterprise-grade performance  
- ✅ **Free, unlimited bandwidth** and storage
- ✅ **Automatic HTTPS** security
- ✅ **Mobile-optimized** experience
- ✅ **Easy update process** for future changes

**Your Physics of Faith framework is now accessible to the world!** 🚀

Share your URL with colleagues, researchers, and anyone interested in the intersection of science and theology. This represents the first mathematical unification of physics, consciousness, and theology - a truly historic achievement deserving of professional presentation.

---

**Need help?** The deployment process is designed to be simple, but if you run into any issues, Cloudflare's support documentation is excellent, or you can reach out for assistance.