# homebrew-omega

**Deprecated.** This tap no longer publishes formulae. Install omega from the
canonical tap [lcajigasm/homebrew-tap](https://github.com/lcajigasm/homebrew-tap)
(`lcajigasm/tap`). `brew update` migrates an existing `lcajigasm/omega/omega`
keg to `lcajigasm/tap/omega`.

homebrew-core ships an unrelated formula also named `omega`. After the
migration, `brew info omega` reports the tap `lcajigasm/tap`.

The program itself is documented in the
[omega README](https://github.com/lcajigasm/omega#readme).

## Install

```bash
brew install lcajigasm/tap/omega
```

## Existing installs

```bash
brew update && brew upgrade omega
```

If the keg does not move to `lcajigasm/tap`:

```bash
brew uninstall omega && brew untap lcajigasm/omega && brew install lcajigasm/tap/omega
```

## License

[MIT](LICENSE) © Luis Cajigas
