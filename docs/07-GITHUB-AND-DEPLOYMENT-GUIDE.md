# FlowFoundry GitHub and Deployment Guide

**Version:** 4.00  
**Audience:** Repository owner, developer, or deployment engineer

---

## 1. GitHub-Ready Package

The delivered source archive is designed to be extracted into a new directory and uploaded to GitHub. It excludes generated dependencies, local build output, temporary files, and Git history.

After extraction, verify that the project root contains `package.json`, `app/`, `public/`, `docs/`, and `.gitignore`.

---

## 2. Create a New GitHub Repository

Create an empty repository without automatically adding another README, `.gitignore`, or licence. Then run from the extracted project directory:

```bash
git init
git add .
git commit -m "Initial FlowFoundry prototype handover"
git branch -M main
git remote add origin https://github.com/YOUR-ACCOUNT/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the example remote with the repository URL created in GitHub.

---

## 3. Existing Repository Alternative

If adding the project to an existing repository:

1. create a dedicated branch;
2. inspect existing files and licences;
3. copy the FlowFoundry source without overwriting unrelated work;
4. install dependencies;
5. run the validation commands;
6. commit and open a pull request.

Do not use destructive Git commands to force the upload.

---

## 4. Install and Run

```bash
pnpm install --frozen-lockfile
pnpm dev
```

Open `http://localhost:3000`.

---

## 5. Validate Before Push

```bash
pnpm run build
pnpm test
pnpm run lint
git status
```

Review the staged files before committing:

```bash
git diff --staged
```

---

## 6. Repository Hygiene

Never commit:

- access tokens or credentials;
- `.env` files containing secrets;
- `node_modules`;
- local build directories;
- temporary archives;
- editor caches;
- deployment credentials;
- user files or private attachments.

The supplied `.gitignore` covers the current local output directories.

---

## 7. Hosting Providers

The application produces Cloudflare-compatible output through vinext. Adapting it to another provider may require changes to the build and runtime configuration. Treat that as a deployment project, not a simple static-file upload.

Before changing providers, confirm support for:

- React server rendering;
- Vite/vinext output;
- Worker-compatible runtime APIs;
- dynamic request headers used by metadata generation;
- future server-side orchestration and secrets.

---

## 9. Versioning Recommendation

Suggested initial tags:

- `v0.1.0-prototype` for the current first-page code;
- `handover-v4.0` for the documentation baseline.

Future releases should separate product versions from document versions.

---

## 10. Licence Decision

No new open-source licence is imposed by this handover. Before making the GitHub repository public, the owner should choose and add an appropriate licence or keep the repository private. Absence of a licence does not automatically grant reuse rights to others.

---

## 11. First GitHub Review Checklist

- Repository name and description identify FlowFoundry.
- README renders correctly.
- No secrets appear in commit history.
- The source archive and GitHub tree match.
- Build and tests pass from a clean checkout.
- Social artwork displays correctly.
- Documentation links work.
- `CLAUDE.md` is present at the repository root.
- The final logo remains `2095 × 677` with transparency and its aspect ratio preserved.
- Repository visibility is intentionally selected.
