# Publicação do Typica PWA

Destino: hospedagem Apache da UFV-DTI. Aplicação estática compilada com Flutter
Web e SQLite no navegador. Não exige processos Node, Python ou R no servidor.

Arquivos de publicação: conteúdo completo de `build/web`, incluindo `.htaccess`.
O banco distribuído é somente o pacote compactado em `data/`; o banco MySQL e
os GeoJSONs de origem permanecem no ambiente de preparação dos dados.

Informações a confirmar com a equipe:

- URL definitiva e caminho da aplicação: raiz do domínio ou uma subpasta.
- HTTPS com certificado válido.
- Publicação de arquivos estáticos `.js`, `.wasm`, fontes e `.gz`.
- `Content-Type: application/wasm` para o SQLite e os módulos do renderizador.
- Entrega do pacote `.sqlite.gz` sem descompactação automática pelo Apache.
- Permissão de uso do `.htaccess`, ou aplicação equivalente pela equipe.
- Disponibilidade do espaço anunciado e procedimento de envio/atualização.

O projeto usa cache próprio de aplicação e banco persistente no navegador.
`index.html`, `sw.js`, `manifest.json` e `flutter_bootstrap.js` devem poder ser
revalidados, conforme o arquivo `apache.htaccess`. Os pacotes de dados têm
nomes por versão. Os arquivos não precisam de permissões de escrita pelo PHP.

COOP/COEP não são obrigatórios nesta configuração: o Drift pode usar IndexedDB
sem esses cabeçalhos, e a aplicação impede o uso simultâneo em duas abas. A
configuração entregue não habilita isolamento de origem, preservando o acesso
normal ao mapa de fundo externo.

O teste local usa `python3 tools/servir.py` e `http://localhost:8080/`. Python é
somente uma ferramenta de teste no computador do desenvolvedor.

Fonte do ambiente anunciado: [Hospedagem de sites — DTI-UFV](https://www1.dti.ufv.br/hospedagem-de-sites/).
