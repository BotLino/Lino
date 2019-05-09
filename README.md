
<p align="center">
  <img src="https://user-images.githubusercontent.com/18364727/46375175-19b5a300-c669-11e8-898e-00b4f5a1fed4.png">
</p>

<h1 align="center"> Lino - O bot da Universidade</h1>
<p align="center">
  <img width="15" src="https://user-images.githubusercontent.com/18364727/46375818-d2c8ad00-c66a-11e8-95a3-a4f80e984a35.png">
  <a href="https://www.facebook.com/Lino-303317230254781/?modal=admin_todo_tour" margin=50>Facebook</a>
  <img width="15" src="https://user-images.githubusercontent.com/18364727/46376121-9a759e80-c66b-11e8-8aa0-6c4cf887089e.png">
  <a href="https://web.telegram.org/#/im?p=@lino_o_bot">@lino_o_bot</a>
</p>
  <p align="center">
    <a href="https://botlino.github.io/docs/"><strong>Visite nossa página &raquo;</strong></a>
    <br>
    <br>
    <a href="https://github.com/BotLino/Lino-WebCrawler">Web Crawler</a>
    &middot;
    <a href="https://github.com/BotLino/Lino-Alerta">Alerta</a>
    &middot;
    <a href="https://github.com/BotLino/Lino-API-Mensageiros">API de Mensageiros</a>
  </p>
</p>

### Sobre o projeto

<p align="justify"> &emsp;&emsp;
  O projeto Lino é um bot que visa orientar, alertar e tirar dúvidas a respeito dos assuntos mais procurados na Universidade de Brasília - Campus FGA. Para apoio ao Bot, um painel de controle de métricas que acompanha sua eficiência durante seu uso em produção.</p>

<p align="justify"> &emsp;&emsp;
  Como principais funcionalidade, tem-se:
</p>


### Utilização

&emsp;&emsp; O Lino se encontra nas plataformas <a href="https://www.facebook.com/Lino-303317230254781/?modal=admin_todo_tour" margin=50>Facebook Mensseger</a> e <a href="https://web.telegram.org/#/im?p=@lino_o_bot">Telegram</a>

### Principais funcionalidades

* Alerta do cardápio (semanal, diário e por refeição);
* Alerta de emails enviados pelos dos funcionário do campus;
* Explicações das documentações mais procuradas.

### Guia de Contribuição

#### Políticas

As políticas de _branches_, _commits_, _pull requests_ e _issues_ se encontram [aqui](https://github.com/fga-eps-mds/2018.2-Lino/tree/master/docs/policies)

#### Desenvolvimento

&emsp;**Dependências**
* Docker
* Docker-compose
* Ngrok

##### Setup do Telegram

Para começar a desenvolver precisamos fazer algumas alterações no código para que funcione localmente.

1. Crie um bot para teste conversando com o @BotFather.

2. Agora altere os valores das seguintes variáveis de ambiente no **docker-compose**, com as credenciais do seu bot.
```
  # Para rodar no telegram altere as seguintes
  # variáveis nos serviços Lino e Actions
  - TELEGRAM_ACCESS_TOKEN=<TOKEN_GERADO_PELO_BOTFATHER>
  - VERIFY=<@USUÁRIO_DO_BOT_NO_TELEGRAM>
  - TELEGRAM_DB_URI=mongodb://mongo_lino:27010/lino_telegram

  # Ou utilize o banco que desejar
  - TELEGRAM_DB_URI=<BANCO_QUE_DESEJAR>
```
**OBS 1:** Altere as variáveis necessárias no serviço do cronjob.

3. Comente as linhas que dizem respeito à variáveis do serviço do **Messenger** em todos os serviços.
```
  # - FACEBOOK_DB_URI
  # - PSID
  # - FACEBOOK_ACCESS_TOKEN
  # - SECRET
```

4. Para conectar com o Telegram, você vai precisar gerar uma URL com certificado. Para isso, nós utilizamos o **Ngrok** (necessário instalá-lo).

5. Agora rode o seguinte comando para expor a porta e gerar o certificado para nosso webhook.

```
  # Gera a URL com certificado (https)
  ./ngrok http <PORTA_BOT>
```

6. Substitua o valor da variável no serviço Lino.
```
  # Altere o valor da variável seguinte
 - WEBHOOK_URL=<URL_HTTPS/webhooks/telegram/webhook
```

7. Rode o seguinte comando para finalizar e desfrutar do seu bot
```
  sudo docker-compose up
```

8. Agora está tudo certinho pra você começar a desenvolver e testar o seu bot :)

#### Setup para testar o Lino no terminal

Para testar as alterações feitas no Lino, execute os seguintes comandos no terminal:

1. Crie a imagem do Lino:
```
sudo docker build -t lino .
```

2. Inicialize o _container_:
```
sudo docker run --rm -it -p 5002:5002 -v $PWD:/2018.2-Lino lino
```

3. Agora basta testar as novas alterações pelo terminal.

### Licença

<p align="justify">&emsp;&emsp; Lino é distribuído sob a licença GPLv3. Consulte <a href="https://github.com/fga-eps-mds/2018.2-Lino/blob/master/LICENSE.md">LICENSE</a> para obter detalhes.</p>
