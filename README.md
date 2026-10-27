# homebrew-omega

![Platform](https://img.shields.io/badge/platform-macOS-000000?logo=apple&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-brightgreen)
![Go](https://img.shields.io/badge/built%20with-Go-00ADD8?logo=go&logoColor=white)

Homebrew tap for [**omega**](https://github.com/lcajigasm/omega): AI-driven
macOS maintenance that combines what [topgrade](https://github.com/topgrade-rs/topgrade)
does (update everything) and what [Mole](https://github.com/tw93/Mole) does
(clean and optimise), with a model from Anthropic, OpenAI, OpenRouter or OpenCode
that runs each step, diagnoses errors and fixes the configuration. The interface
is available in English, Spanish, French, German and Portuguese.

## Requirements

- macOS (Apple Silicon or Intel)
- [Homebrew](https://brew.sh)
- An API key for at least one of these providers:

| Provider | Where to get a key |
|---|---|
| Anthropic | <https://console.anthropic.com/settings/keys> |
| OpenAI | <https://platform.openai.com/api-keys> |
| OpenRouter | <https://openrouter.ai/settings/keys> |
| OpenCode Zen | <https://opencode.ai/auth> |

Go is installed automatically as a build dependency.

## Install

```bash
brew tap lcajigasm/omega
brew install omega
```

or in one step:

```bash
brew install lcajigasm/omega/omega
```

> homebrew-core already has a formula called `omega` (a Xapian search engine).
> If `brew install omega` picks that one, use the full name
> `lcajigasm/omega/omega`.

Optional, to use topgrade and Mole as backends:

```bash
brew install topgrade mole
```

## Getting started

```bash
omega setup        # pick a provider, store the API key in the Keychain and choose a model
omega analyze      # report on the state of your Mac without changing anything
omega              # complete maintenance: update + clean + summary
```

Other tasks:

| Command | What it does |
|---|---|
| `omega update` | updates only (like topgrade) |
| `omega clean` | cleanup only (like `mo clean`) |
| `omega fix` | diagnoses and fixes the topgrade and Mole configuration |
| `omega -p "…"` | free-form task in natural language |
| `omega steps` | maintenance steps detected on your Mac |
| `omega steps run brew npm` | run steps without AI |

Dangerous actions (deleting files, `sudo`, editing configuration) ask for
confirmation. Destructive commands (`rm -rf ~`, `diskutil erase…`, `curl | sh`…)
are always blocked.

The interface language follows your system locale; override it with
`omega config set language es` or `OMEGA_LANG=fr`.

Full documentation is in the
[omega README](https://github.com/lcajigasm/omega#readme).

## What gets installed

- The `omega` binary in `$(brew --prefix)/bin`.
- Shell completion for zsh, bash and fish.

It is built from the source of the published release (`go build`, with the
version embedded in `omega --version`).

## Upgrade

```bash
brew update
brew upgrade omega
```

## Uninstall

```bash
brew uninstall omega
brew untap lcajigasm/omega
```

omega keeps data outside Homebrew. To remove it as well:

```bash
rm -rf ~/.config/omega ~/.local/state/omega
security delete-generic-password -s omega-cli -a anthropic   # repeat per provider
```

## Install the development version

```bash
brew install --HEAD lcajigasm/omega/omega
```

## Troubleshooting

**`Error: No available formula with the name "omega"`**: run
`brew tap lcajigasm/omega` or use the full name `lcajigasm/omega/omega`.

**The Xapian `omega` gets installed**: uninstall it (`brew uninstall omega`) and
install with the full name.

**The build fails**: run `brew update` and try again. If it still fails, open an
issue at <https://github.com/lcajigasm/omega/issues> with the output of
`brew install --verbose --debug lcajigasm/omega/omega`.

## For maintainers

When releasing a new omega version:

```bash
# in the omega repository
git tag v0.2.0 && git push origin v0.2.0
make formula VERSION=0.2.0               # updates url and sha256 in Formula/omega.rb
cp Formula/omega.rb ../homebrew-omega/Formula/omega.rb

# in this repository
brew audit --strict --online lcajigasm/omega/omega
brew install --build-from-source lcajigasm/omega/omega && brew test omega
git commit -am "omega 0.2.0" && git push
```

## License

[MIT](LICENSE) © Luis Cajigas
