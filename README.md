# Typica PWA

Site-aplicativo instalável desenvolvido com Flutter Web. Oferece pesquisa de
municípios, GPS, seleção de pixels, filtros de cultivares, fichas e relatório PDF.
As recomendações ficam disponíveis offline após preparar os dados. O ranking
usa os resultados originais de cada pixel.

Este repositório contém exclusivamente o projeto **web/PWA**. O código fica na
raiz, com `lib/`, `web/`, `tools/` e `deploy/`. Os dados científicos e os pacotes
compilados são mantidos fora do GitHub. Logotipos, ícones e fontes com licença
acompanham o projeto.

## Preparar e executar

São necessários Flutter com Dart compatível com o `pubspec.yaml` e Python 3.
Após clonar o repositório, entre na pasta do projeto e obtenha as dependências:

```bash
flutter pub get
```

Os dados privados são fornecidos separadamente. Organize-os em `private_assets/`
(pasta ignorada pelo Git):

```text
private_assets/
  cultivares.json
  colors_2026.json
  mg.geojson
  data/
    manifest.json
    <arquivo-original>.sqlite.gz
```

O nome e o caminho do SQLite compactado devem corresponder ao campo `asset` do
manifesto original. Os logotipos já estão incluídos no projeto; não é necessário
copiá-los para a pasta privada.

Com os dados disponíveis:

```bash
python3 tools/compilar.py
python3 tools/servir.py
```

Para usar os dados em outro local, sem copiá-los para o repositório:

```bash
python3 tools/compilar.py --assets-dir /caminho/privado/dos/assets
```

Também é possível definir a variável `TYPICA_ASSETS_DIR` ou salvar somente o
caminho em `.typica-assets-path`, arquivo local ignorado pelo Git. A prioridade
é `--assets-dir`, variável de ambiente, arquivo local e `private_assets/`.

Abra **http://localhost:8080/** no Chrome, em uma aba normal. A primeira abertura
mostra **Verificar atualização**, **Baixar banco de dados** e **Salvar como app**.
O primeiro acesso ao site não baixa o banco automaticamente. **Salvar como app**
inclui a preparação dos dados após confirmar a instalação; pelo ícone, o Typica
conclui a preparação e abre o mapa sozinho. **Baixar banco de dados** permite
preparar os dados separadamente e depois tocar em **Abrir Typica**.

Na versão **0.1.0+9**, o nome exibido no site, instalação e tela inicial é
**Typica**. A abertura mantém o logotipo e as instituições parceiras por no
mínimo três segundos. Os indicadores de abertura e download são círculos de
20 pixels, com traço de 2 pixels. O tutorial do mapa aguarda a transição de
entrada e tem um registro próprio para o aplicativo instalado: ver ou pular
o tutorial no site não dispensa a apresentação na primeira abertura após
instalar. Ao concluir ou pular, o tutorial não reaparece automaticamente;
**Rever tutorial**, no menu do mapa, permanece disponível.

O script reconhece `flutter` no PATH ou `~/App/flutter/bin/flutter`. As opções
`--flutter` e `--assets-dir /caminho/dos/assets` permitem outros caminhos. São
necessários os dados privados descritos acima. Nenhum arquivo original é
modificado. A compilação não exige o projeto Android nem um servidor MySQL.

Use `tools/compilar.py`: `flutter build web` sozinho não gera o service worker
próprio deste projeto.

## Dados por município — versão 0.1.0+6

O SQLite único de 198 MB exigia muitas cópias na memória durante a importação.
`tools/particionar_dados.py` deriva um catálogo de 450.560 bytes e **853 SQLite
municipais**, mantendo as geometrias WKB, índices dos pixels e referências dos
rankings. O maior banco municipal tem **1.716.224 bytes**. A exportação compara
todas as linhas derivadas contra a origem e valida os totais: 659.485 feições,
incluindo 658.632 pixels e 853 limites municipais.

Os 854 pacotes gzip são agrupados em **46 lotes de até 2 MB**, somando
**88.645.639 bytes**. O manifesto `data/manifest.json` descreve tamanho, SHA-256,
lote e posição de cada pacote. O formato é `cultivar-sqlite-regions-v2`.

A preparação verifica cada lote e grava seus pacotes como Blobs compactados no
IndexedDB, em uma transação. Só depois segue para o próximo lote. Ela não abre
os 198 MB do banco antigo. Uma interrupção retoma os lotes que faltam, inclusive
após fechar e reabrir o navegador. Um pacote corrompido é recuperado pelo lote
correspondente, sem baixar todos novamente.

Na consulta, somente o catálogo e um município são descompactados e abertos
como SQLite de leitura. A conexão regional e seu sistema de arquivos em memória
são fechados após a leitura. As consultas de regiões são serializadas. Todos os
municípios continuam disponíveis offline, sem baixar dados ao pesquisar.

A descompactação usa `archive` em Dart com limite de saída por pacote, sem exigir
`DecompressionStream`. As funções opcionais `StorageManager.estimate/persist`
são verificadas antes do uso. Isso remove incompatibilidades específicas; não
substitui testes em aparelhos físicos.

A atualização do formato v1 para v2 exige preparar os novos lotes uma vez.
O banco científico antigo, histórico e preferências são preservados. O pacote
monolítico continua na publicação para compatibilidade com clientes antigos,
mas a versão 6 não o baixa nem o abre.

## Offline e instalação — versão 0.1.0+8

A instalação e o download científico compõem um único fluxo. **Salvar como app**
usa o convite nativo quando disponível. Ao aceitar, os dados são preparados
automaticamente. Cancelar o convite não inicia o download. Sem convite nativo,
o botão mostra as instruções do navegador; abrir pelo ícone conclui a preparação
e entra no mapa. Uma visita inicial ao site continua mostrando os três botões,
sem iniciar o download dos dados.

A preparação não ocupa a sessão do histórico e das consultas. Se o ícone abrir
enquanto a aba ainda prepara os dados, as janelas usam uma fila via Web Locks
para reaproveitar os lotes salvos e evitar downloads duplicados. A verificação
do catálogo abre apenas um SQLite pequeno em memória. As consultas continuam
protegidas pela sessão existente. Em navegadores sem Web Locks, os Blobs são
gravados em transações, mas janelas simultâneas podem repetir algum download.

No aplicativo instalado, dados ausentes ou interrompidos são preparados ao
abrir, sem exigir outro botão. Uma falha mantém os pacotes já salvos e mostra
**Tentar novamente**. Com os dados completos, abre diretamente no mapa.

No iPhone/iPad, use Safari → Compartilhar → Adicionar à Tela de Início. O
armazenamento do aplicativo instalado pode ser separado do navegador; nesse
caso, a primeira abertura pelo ícone prepara os dados automaticamente com internet.
No Android, use o Chrome atualizado. Navegadores dentro de outros aplicativos
podem limitar instalação e armazenamento. Alguns navegadores criam um atalho,
sem uma entrada na lista de aplicativos.

O navegador decide se concede armazenamento persistente. Limpar os dados do
site remove os pacotes e exige nova preparação. O mapa de fundo OpenStreetMap
continua dependendo de internet; pesquisa, recomendações, filtros, fichas e PDF
usam os recursos locais. Para testar, prepare os dados, feche o app, retire a
conexão e abra pelo ícone novamente.

Se ocorrer um erro, **Copiar detalhes do erro** inclui versão, navegador,
quantidade de pacotes salvos e tamanhos máximos dos buffers e bancos abertos.
Esses números medem os dados processados, não toda a memória RAM do navegador.
Não há envio automático desses diagnósticos.

## Testar no telefone

O PWA exige HTTPS, com exceção de `localhost`. HTTP pelo IP do computador não
habilita todos os recursos. Para testar sem USB, com o servidor local ativo:

```bash
cloudflared tunnel --no-autoupdate --url http://127.0.0.1:8080 --protocol http2
```

Abra o HTTPS informado no Chrome/Safari do telefone. O computador e o túnel
precisam continuar ligados durante o acesso pela internet. Qualquer pessoa com
o link pode acessar os dados enquanto o túnel estiver ativo; esse acesso deve
estar autorizado. Uma nova execução gera outro endereço, com armazenamento
separado no navegador.

Alternativamente, no Android com depuração USB autorizada:

```bash
~/Android/Sdk/platform-tools/adb devices -l
~/Android/Sdk/platform-tools/adb -d reverse tcp:8080 tcp:8080
```

Abra `http://localhost:8080/` no telefone. O armazenamento é próprio do telefone,
independente do Chrome do computador.

## Publicar na UFV-DTI

Publique todo o conteúdo de `build/web/`, incluindo `.htaccess` e `data/`.
São arquivos estáticos para Apache; PHP/MySQL não são necessários em execução.
A publicação tem aproximadamente 230 MB, abaixo dos 500 MB informados pela DTI.
Confirme o HTTPS e os tipos `.wasm`, `.js`, `.bin`, `.gz` com a instituição.
O `.wasm` usa `application/wasm`; os lotes `.bin` são bytes binários entregues
sem transformações. O arquivo `.htaccess` fornece os tipos de conteúdo.

Quando o endereço for definido, ajuste apenas a base:

```bash
python3 tools/compilar.py --base-href /
# ou, para https://site.ufv.br/cultivar/
python3 tools/compilar.py --base-href /cultivar/
```

Não há domínio/IP fixo no código. Os pacotes e workers usam a base da aplicação.
Publique uma pasta completa de forma atômica. O service worker salva o cache da
interface antes de ativar a atualização e reabre as janelas existentes. Lotes
binários ficam fora desse cache e são persistidos pelo gerenciador de pacotes.
Uma primeira instalação não força recarregamento durante a preparação.

## Verificar

Use perfis descartáveis e execute os testes com dados reais um de cada vez:

```bash
npm install --prefix /tmp/cultivar-pwa-browser playwright-core
NODE_PATH=/tmp/cultivar-pwa-browser/node_modules node tools/testar_pwa.cjs
NODE_PATH=/tmp/cultivar-pwa-browser/node_modules node tools/testar_pacotes.cjs
NODE_PATH=/tmp/cultivar-pwa-browser/node_modules node tools/testar_preparacao.cjs
NODE_PATH=/tmp/cultivar-pwa-browser/node_modules node tools/testar_atualizacao.cjs
NODE_PATH=/tmp/cultivar-pwa-browser/node_modules node tools/testar_tela_inicial.cjs
```

O primeiro teste requer o servidor; `PWA_TEST_URL` permite outra porta. O teste
de pacotes usa `build/web` por padrão (`PWA_TEST_DIRECTORY` permite outra pasta).
`PWA_TEST_LOW_MEMORY=1` simula ausência de algumas APIs e limita o heap antigo do
V8 a 256 MB. Isso não simula toda a RAM de um telefone nem executa Safari.

Os testes cobrem ranking em dois pixels de Viçosa, maior município, filtros,
PDF, reabertura offline, SHA, retomada e preservação de dados anteriores.
Convite de instalação e modo standalone são simulados no Chrome do computador;
a instalação física e os aparelhos que falhavam precisam de validação local.

## Git

`private_assets/`, os dados em `assets/`, `web/data/`, builds, APKs e binários
gerados ficam fora do Git. Código, documentação, logotipos, fontes licenciadas e
ferramentas de preparação acompanham o projeto. O banco de dados não é obtido
ao clonar o repositório: deve ser fornecido separadamente para compilar e testar
com as recomendações reais.
