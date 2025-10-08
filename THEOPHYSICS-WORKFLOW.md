# 🌟 THEOPHYSICS Gallery Workflow

## ✅ What's Been Set Up

Your THEOPHYSICS collection now has **full interactive features**:

### 📂 File Structure
```
collections/theophysics/
├── index.html          ← Beautiful gallery page
└── meta.json           ← Collection metadata

descriptions/
├── theophysics.txt                    ← Collection description
├── christ-observer-effect.txt         ← Image descriptions
├── entropy-grace-model.txt
└── consciousness-gravity-diagram.txt
```

---

## 🎨 Features

### 1. **Clickable Image Cards**
- Click any visualization → Opens full-screen modal
- Shows large high-quality image
- Displays title + description

### 2. **Download with Watermark**
- Automatically adds: `THEOPHYSICS • PhysicsOfFaith.org`
- Gold text on semi-transparent black background (bottom-right)
- Downloads as PNG: `the-master-equation-theophysics.png`
- Watermark scales with image size

### 3. **Share Link**
- Generates unique URL for each image
- Uses Web Share API (mobile)
- Copies link to clipboard (desktop)
- Example: `...theophysics/index.html?image=master-equation.svg`

### 4. **Keyboard Shortcuts**
- `ESC` key → Close modal

---

## 🚀 How to Use

### Adding New Images to Collection

1. **Drop image** into `/images/` folder
2. **Create description** (optional):
   ```
   descriptions/your-image-name.txt
   ```
3. **Add to collection page**:
   Edit `collections/theophysics/index.html` and add a new card:
   ```html
   <div class="card" onclick="openModal('your-image.svg', 'Title Here', 'Description here')">
     <img class="card-image" src="../../images/your-image.svg" alt="Your Image">
     <div class="card-content">
       <h3 class="card-title">Your Title</h3>
       <p class="card-description">Your description...</p>
       <div class="tags">
         <span class="tag">Tag1</span>
         <span class="tag">Tag2</span>
       </div>
     </div>
   </div>
   ```

4. **Deploy**:
   ```
   Double-click: auto-deploy.bat
   ```

---

## 🎯 Quick Deploy

```batch
# Just run this:
auto-deploy.bat

# It will:
✓ Build gallery
✓ Commit changes
✓ Push to GitHub
✓ Auto-deploy to Cloudflare (~1 min)
```

---

## 🎨 Watermark Details

- **Text**: `THEOPHYSICS • PhysicsOfFaith.org`
- **Position**: Bottom-right corner
- **Color**: Gold (#ffd166)
- **Background**: Semi-transparent black
- **Font**: System UI (clean, professional)
- **Size**: Scales to 2% of image width (minimum 16px)

---

## 🔗 Share Link Format

When someone clicks "Share Link", they get:
```
https://your-site.pages.dev/collections/theophysics/index.html?image=master-equation.svg
```

When they visit the link:
- Page loads automatically
- Image modal opens immediately
- Shows the exact visualization shared

---

## 🌈 Color Scheme

- **Background**: Dark cosmic gradient
- **Cards**: Translucent white overlay
- **Accent 1**: Gold (#ffd166) - Titles, watermark
- **Accent 2**: Teal (#06d6a0) - Links, share button
- **Accent 3**: Blue (#118ab2) - Download button
- **Text**: Light gray (#e0e6ed)

---

## 💡 Pro Tips

1. **Image Names**: Use descriptive filenames (no spaces)
   - ✓ `master-equation-visualization.svg`
   - ✗ `image 1.png`

2. **Descriptions**: Keep them concise but informative
   - 1-2 sentences for card preview
   - Full description shows in modal

3. **Tags**: Use consistent tags across visualizations
   - Makes browsing easier
   - Helps with SEO

4. **Cover Image**: Add `cover.png` to collection folder
   - Will appear in main gallery
   - 16:9 aspect ratio works best

---

## 🆘 Troubleshooting

**Modal won't open?**
- Check browser console (F12)
- Verify image path is correct

**Watermark not showing?**
- Canvas might not be loading image
- Check CORS (images must be same domain)

**Share not working?**
- Desktop: Falls back to clipboard copy
- Mobile: Uses native share sheet

---

## 📞 Need Help?

Your collection is at:
`collections/theophysics/index.html`

Open it in browser to test everything!

