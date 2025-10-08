# MCP Setup Guide for Cursor

## 🎯 What is MCP?

**Model Context Protocol (MCP)** lets you connect other AIs to Cursor's Composer as custom tools. This is perfect for delegating paper development to specialized AI agents.

---

## 📥 HOW TO INSTALL MCP IN CURSOR:

### Step 1: Open Cursor Settings
1. Open Cursor
2. Go to **Settings** (Ctrl+,)
3. Navigate to **Features > MCP**

### Step 2: Add MCP Server
1. Click **"+ Add New MCP Server"**
2. Fill in the details:

#### For stdio Server (local):
- **Name:** `paper-writer` (or any nickname)
- **Type:** Select `stdio`
- **Command:** `node ~/path-to-your-mcp-server/build/index.js`

#### For SSE Server (remote):
- **Name:** `paper-writer`
- **Type:** Select `sse`
- **URL:** `http://your-server-url.com:8000/sse`

3. Click **Save**

### Step 3: Verify Installation
1. Check that server appears in MCP servers list
2. Click **refresh button** to populate tool list
3. Server should show as "Connected"

---

## 🛠️ USING MCP TOOLS IN COMPOSER:

### Automatic Tool Usage:
Composer Agent will automatically use MCP tools when relevant to your prompt.

### Explicit Tool Usage:
Mention the tool by name or describe its function:
```
"Use the paper-writer tool to develop Paper #8 according 
to the brief in PAPER-8-GRACE-FUNCTION-BRIEF.md"
```

### Tool Execution:
1. Composer displays approval request
2. Shows tool call arguments
3. You approve execution
4. Tool runs and returns response
5. Response appears in chat

---

## 📋 BRIEFS READY FOR DELEGATION:

### Available Briefs:
1. **`PAPER-8-GRACE-FUNCTION-BRIEF.md`** ✅ READY
   - Cosmological model with Grace Function
   - Includes Grok's Eternity Equation
   - ~10-15 pages target

### To Create More Briefs:
Just tell me which paper you want to delegate, and I'll create a similar detailed brief with:
- Objective
- Foundation
- Sections to write
- Mathematical requirements
- Citations needed
- Success criteria

---

## 🎯 WORKFLOW:

### 1. Setup MCP (you do this once)
- Follow steps above in Cursor Settings

### 2. Open Composer
- Start new chat with Composer Agent

### 3. Provide Brief
```
I need you to write Paper #8: The Grace Function.

Please read the complete brief in:
D:\CloudFlare GitHUB\physics-of-faith-visualizations\PAPER-8-GRACE-FUNCTION-BRIEF.md

Follow all requirements and produce a complete academic paper.
```

### 4. Review Output
- Check mathematical rigor
- Verify theological balance
- Ensure testability
- Compare to completed papers (1, 12, 13)

### 5. Iterate if Needed
- Request specific revisions
- Add missing sections
- Adjust tone/balance

---

## 💡 TIPS:

### Environment Variables:
If your MCP server needs environment variables, create a wrapper script:

**wrapper.sh:**
```bash
#!/bin/bash
export API_KEY="your-key-here"
node ~/mcp-server/build/index.js
```

Then use `./wrapper.sh` as your Command in MCP settings.

### Multiple Papers:
You can set up multiple MCP servers for different tasks:
- `paper-writer` - for drafting papers
- `math-checker` - for verifying equations
- `citation-finder` - for locating references

### Model Compatibility:
Note: MCP tools may not work with all models. Test with:
- Claude Sonnet (best compatibility)
- GPT-4 (good compatibility)

---

## 🚨 TROUBLESHOOTING:

### Server Won't Connect:
- Check command path is correct
- Verify server is actually running
- Look at Cursor logs for errors

### Tools Not Appearing:
- Click refresh button in MCP settings
- Restart Cursor
- Check server logs

### Tool Execution Fails:
- Check tool arguments
- Verify file paths are absolute
- Review error message in Composer

---

## 📂 FILE STRUCTURE FOR DELEGATION:

Keep all briefs organized:
```
D:\CloudFlare GitHUB\physics-of-faith-visualizations\
├── PAPER-8-GRACE-FUNCTION-BRIEF.md ✅
├── PAPER-3-ALGORITHM-BRIEF.md (to create)
├── PAPER-4-TIME-BRIEF.md (to create)
├── PAPER-5-CONSCIOUSNESS-BRIEF.md (to create)
└── ... etc
```

---

## 🎯 NEXT STEPS:

1. **Install MCP** in Cursor Settings (follow steps above)
2. **Test with Paper #8 brief** (already created)
3. **Let me know which other papers** you want briefs for
4. **Review outputs** and iterate as needed

---

**Status:** MCP setup guide ready. Paper #8 brief ready. Awaiting your MCP installation and first delegation test. 🚀

