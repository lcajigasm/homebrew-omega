# homebrew-omega

![Platform](https://img.shields.io/badge/platform-macOS-000000?logo=apple&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-brightgreen)
![Go](https://img.shields.io/badge/built%20with-Go-00ADD8?logo=go&logoColor=white)

Tap de Homebrew para [**omega**](https://github.com/lcajigasm/omega): mantenimiento
de macOS guiado por IA que junta lo que hacen
[topgrade](https://github.com/topgrade-rs/topgrade) (actualizar todo) y
[Mole](https://github.com/tw93/Mole) (limpiar y optimizar), con un modelo de
Anthropic, OpenAI, OpenRouter u OpenCode que ejecuta cada paso, diagnostica los
errores y corrige la configuración.

## Requisitos

- macOS (Apple Silicon o Intel)
- [Homebrew](https://brew.sh)
- Una API key de al menos uno de estos proveedores:

| Proveedor | Dónde conseguir la key |
|---|---|
| Anthropic | <https://console.anthropic.com/settings/keys> |
| OpenAI | <https://platform.openai.com/api-keys> |
| OpenRouter | <https://openrouter.ai/settings/keys> |
| OpenCode Zen | <https://opencode.ai/auth> |

Go se instala automáticamente como dependencia de compilación.

## Instalación

```bash
brew tap lcajigasm/omega
brew install omega
```

o en un solo paso:

```bash
brew install lcajigasm/omega/omega
```

> homebrew-core ya tiene una fórmula llamada `omega` (un motor de búsqueda de
> Xapian). Si `brew install omega` intenta instalar esa, usa el nombre completo
> `lcajigasm/omega/omega`.

Opcional, para usar topgrade y Mole como backends:

```bash
brew install topgrade mole
```

## Primeros pasos

```bash
omega setup        # elige proveedor, guarda la API key en el llavero y escoge modelo
omega analyze      # informe del estado del Mac sin cambiar nada
omega              # mantenimiento completo: actualizar + limpiar + resumen
```

Otras tareas:

| Comando | Qué hace |
|---|---|
| `omega update` | solo actualizaciones (equivalente a topgrade) |
| `omega clean` | solo limpieza (equivalente a `mo clean`) |
| `omega fix` | diagnostica y arregla la configuración de topgrade y Mole |
| `omega -p "…"` | tarea libre en lenguaje natural |
| `omega steps` | pasos de mantenimiento detectados en tu Mac |
| `omega steps run brew npm` | ejecutar pasos sin IA |

Las acciones peligrosas (borrar archivos, `sudo`, editar configuraciones) piden
confirmación. Los comandos destructivos (`rm -rf ~`, `diskutil erase…`,
`curl | sh`…) están bloqueados siempre.

La documentación completa está en el
[README de omega](https://github.com/lcajigasm/omega#readme).

## Qué instala

- El binario `omega` en `$(brew --prefix)/bin`.
- Autocompletado para zsh, bash y fish.

Se compila desde el código fuente de la versión publicada
(`go build`, con la versión incrustada en `omega --version`).

## Actualizar

```bash
brew update
brew upgrade omega
```

## Desinstalar

```bash
brew uninstall omega
brew untap lcajigasm/omega
```

omega guarda datos fuera de Homebrew. Para borrarlos también:

```bash
rm -rf ~/.config/omega ~/.local/state/omega
security delete-generic-password -s omega-cli -a anthropic   # repetir por proveedor
```

## Instalar la versión en desarrollo

```bash
brew install --HEAD lcajigasm/omega/omega
```

## Solución de problemas

**`Error: No available formula with the name "omega"`**: ejecuta
`brew tap lcajigasm/omega` o usa el nombre completo `lcajigasm/omega/omega`.

**Se instala el `omega` de Xapian**: desinstálalo (`brew uninstall omega`) e
instala con el nombre completo.

**Falla la compilación**: ejecuta `brew update` y vuelve a intentarlo. Si sigue
fallando, abre un issue en <https://github.com/lcajigasm/omega/issues> con la
salida de `brew install --verbose --debug lcajigasm/omega/omega`.

## Para mantenedores

Al publicar una nueva versión de omega:

```bash
# en el repositorio omega
git tag v0.2.0 && git push origin v0.2.0
make formula VERSION=0.2.0               # actualiza url y sha256 en Formula/omega.rb
cp Formula/omega.rb ../homebrew-omega/Formula/omega.rb

# en este repositorio
brew audit --strict --online lcajigasm/omega/omega
brew install --build-from-source lcajigasm/omega/omega && brew test omega
git commit -am "omega 0.2.0" && git push
```

## Licencia

[MIT](LICENSE) © Luis Cajigas
