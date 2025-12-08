# Alpha Testing: Login Cookie Fix (#454)

## IMPORTANT: Alpha Testing Uses Production Branch

**Alpha testers (including PM on alpha laptop) test on the `production` branch, NOT `main`.**

To deploy fixes for alpha testing:
1. Push to `main` first (done)
2. Merge `main` → `production` and push
3. On alpha laptop: `git pull origin production`

This ensures alpha testers get the same code that will be deployed.
