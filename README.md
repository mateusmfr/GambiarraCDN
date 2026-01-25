# hash_renamer

Script para renomear arquivos adicionando um hash do conteúdo ao final do nome (cache-busting).

Exemplos:

- Dry-run recursivo (mostra alterações):

```powershell
python hash_renamer.py --dir "C:\Users\Mateus\Pictures\GambiarraCDN\images" --recursive --dry-run
```

- Aplicar alterações (aplica renomeações):

```powershell
python hash_renamer.py --dir "C:\Users\Mateus\Pictures\GambiarraCDN\images" --recursive
```

Opções principais:

- `--dir` / `-d`: diretório alvo (padrão `.`)
- `--recursive` / `-r`: processa subpastas
- `--algorithm`: algoritmo de hash (p.ex. `sha256`, `sha1`, `md5`)
- `--length` / `-l`: número de caracteres do hash a adicionar (padrão `8`)
- `--sep`: separador entre nome e hash (padrão `-`)
- `--dry-run`: apenas mostrar, não alterar arquivos

Observações:

- O script tenta evitar sobrescritas: se o arquivo destino já existir e for idêntico, o original será removido; se for diferente, será buscado um nome livre adicionando `-1`, `-2`, etc.
- Faça sempre um `--dry-run` antes de executar para confirmar os resultados.
