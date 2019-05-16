## Deploy contínuo com Gitlab Runner

A utilização do novo deploy funciona a partir de uma nova funcionalidade do Gitlab, chamada de Gitlab Runner, que ao invés de utilizar um dos runners padrões do Gitlab, utiliza um proprietário, no caso, uma droplet do DigitalOcean. O roteiro para deploy contínuo em uma droplet no DigitalOcean pode ser realizado desta forma:

- Criar uma droplet nova no DigitalOcean (DO)
- Acessar a droplet por ssh (ou terminal interativo dentro do DO)
- Instalar o Gitlab Runner, cada sistema possui um binário próprio
    - Linux x86-64
    `
    sudo wget -O /usr/local/bin/gitlab-runner https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-amd64
    `
    - Linux x86
    `
    sudo wget -O /usr/local/bin/gitlab-runner https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-386
    `
    - Linux arm
    `
    sudo wget -O /usr/local/bin/gitlab-runner https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-linux-arm
    `

- Permitir execução do Gitlab Runner
`sudo chmod +x /usr/local/bin/gitlab-runner`

- Instalar o Docker (caso você já não tenha instalado)
`curl -sSL https://get.docker.com/ | sh`

- Criar um usuário do Gitlab CI
`sudo useradd --comment 'GitLab Runner' --create-home gitlab-runner --shell /bin/bash`

- Instalar e rodar o serviço
`sudo gitlab-runner install --user=gitlab-runner --working-directory=/home/gitlab-runner`
`sudo gitlab-runner start`

- Agora você deve registrar o Gitlab Runner com seu repositório
`sudo gitlab-runner register`
    - No coordenador de URI, digite "https://gitlab.com/"
    - No token, adicione o token presente no seu repositório do gitlab (Settings > CI/CD > Runners > Set up a specific Runner manually)
    - Na descrição, adicione um apelido pro seu runner
    - Em tags, crie uma tag para identificação (importante)
    - No executor, digite "shell"

- Acesse a droplet e adicione o usuário gitlab-runner ao grupo 'docker'
`sudo usermod -aG docker gitlab-runner`

- Permita que o usuário tenha acesso a todo o sistema
`sudo visudo`
    - Na ultima linha do arquivo adicione a seguinte configuração
    `gitlab-runner ALL=(ALL) NOPASSWD= ALL`

- Reinicie o serviço do gitlab
`sudo gitlab-runner restart`

- Em seu arquivo de configuração 'gitlab-ci.yml' crie os passos necessários para o deploy, neste determinado stage, adicione:
```
tags: 
  - <nome_da_tag_criada>
```

Com isso, sempre o runner escolhido para rodar seu pipeline de deploy será o runner criado em sua droplet no DigitalOcean