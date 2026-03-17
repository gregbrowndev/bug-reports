# Bug report for mise monorepo tasks, pnpm, prepare, idiomatic version file

I seem to be going in circles with this issue. I'm trying to manage a monorepo with a NodeJS project using `pnpm`.
I use idiomatic version files, e.g. `.node-version`, to specify the node version and a postinstall hook to enable `pnpm`.

## Issue 1: pnpm not found when task run from monorepo root

I seem to be having two issues now, but the first I wanted to report:

- I can run `mise format` from the `packages/app1` directory all fine. It runs `pnpm format` which runs prettier in the `package.json`.
- However, when I run `mise format` from the root `mise.toml`, I get a `command not found: pnpm` error.

It seems this issue is related to the idiomatic version file, since if I specify `node = "25"` in the tools explicitly the problem goes away.

I also tried other approaches too, such as setting the `node.corepack = true` setting, which I thought would make the `postinstall` hook unnecessary.

## Issue 2: postinstall hook not run with `mise install --force node`

The second issue I came across while trying to diagnose the above issue, is that even when switching from the idiomatic version file to explicit tool, once node has been installed (without `pnpm`) its difficult to force the `postinstall` hook to run again. Even with

```shell
mise install --force node`
```

I would expect both node/pnpm to be installed, but instead I had to uninstall node, prune versions, and reinstall.

| `node` installed...  | `pnpm` installed...    | `mise :format` (in app1 dir) | `mise //packages/app1:format` |
|----------------------|------------------------|------------------------------|-------------------------------|
| ✅ via idiomatic file | ✅ via postinstall hook | ✅ runs task                  | ❌ "pnpm: command not found"   |
| ✅ via idiomatic file | ❌ via `node.corepack`  | ❌ "pnpm: command not found"  | ❌ "pnpm: command not found"   |
| ✅ via explicit tool  | ⚠️ via postinstall hook | ✅ runs task                  | ✅ runs task                   |
| ✅ via explicit tool  | ⚠️ via `node.corepack`  | ✅ runs task                  | ✅ runs task                   |

⚠️ - because I found sometimes the postinstall hook wouldn't run without running `mise uninstall node --all` first, and even after doing `mise use node`, `pnpm` would not be installed...
