#!/usr/bin/env node
import { access } from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const distDir = path.resolve(__dirname, '../dist');
const rawArgs = process.argv.slice(2);
let projectName = process.env.CLOUDFLARE_PROJECT_NAME;
let passthroughArgs = [];

if (projectName) {
  passthroughArgs = rawArgs;
} else if (rawArgs.length > 0) {
  [projectName, ...passthroughArgs] = rawArgs;
}

if (!projectName) {
  console.error('Missing Cloudflare project name. Set CLOUDFLARE_PROJECT_NAME or pass it as the first argument.');
  process.exit(1);
}

try {
  await access(distDir);
} catch (error) {
  console.error('Build output not found. Run "npm run build" before deploying.');
  process.exit(1);
}

const npxCommand = process.platform === 'win32' ? 'npx.cmd' : 'npx';
const commandArgs = ['wrangler', 'pages', 'deploy', distDir, '--project-name', projectName, ...passthroughArgs];

const child = spawn(npxCommand, commandArgs, {
  stdio: 'inherit',
  env: process.env
});

child.on('close', code => {
  process.exit(code ?? 0);
});
