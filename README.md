## Tutorial *ldMusic*

*Versão: 0.1*

Tutorial básico para compartilhamento e nivelamento de conhecimento para o desenvolvimento da plataforma

#### **Git**

Facilitar a entrega de pequenas modificações e adições de recursos localmente(no PC de cada um) para o repositório remoto no Github, e também fazer o versionamento do Sistema.

#### **Flask**

Agilizar e facilitar o processo de desenvolvimento  web com Python utilizando o Framework [Flask](https://flask-ptbr.readthedocs.io/en/latest/).

#### **Docker**

Ferramenta para compartilhar o mesmo ambiente de desenvolvimento através de Contêineres e Imagens de Docker (evitando aquela famosa frase "mas na minha máquina funciona")

Instalação no Windows: **Certifique-se de que esteja utilizando Windows 10 Pro** mais atual;
Baixe o instalador:

[Docker-For-Windows](https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe)

Abra o Instalador, aceite os termos e clique em Próximo/Next, e depois Finalizar/Finish!

Aperta o Menu Iniciar do Windows e digite "Docker"

Aparecerá o "Docker for Windows", abra esse aplicativo.

Assim que abrir aparecerá o seguinte icóne na sua barra de tarefas: 

![](https://blog.umbler.com/wp-content/uploads/2017/12/whale-taskbar-circle.png)

Pronto, o serviço Docker já foi inicializado e está pronto para subirmos nossos contêineres!

Bora fazer um teste?

Abra o PowerShell em **Modo de Administrador** e digite:

```powershell
docker run hello-world
```

Depois veja se baixou a imagem de hello-world

```powershell
docker images
```
Remover a imagem criada:

```powershell
docker rmi hello-world
```

Agora vamos construir a nossa Imagem Base, que será criada através dos comandos contidos no arquivo Dockerfile
(Antes de executar esse comando, confirme que você está na pasta raiz do projeto ldMusic)
```powershell
docker build -t ldmusicpy:latest .
```
Pronto! Agora nossa imagem já está no nosso repositório local e já podemos subir nosso contêiner contendo a nossa aplicação rodando!

```powershell
docker run -d --name devldmusic -v "$(pwd)":/usr/src/app -p 5000:5000 ldmusicpy:latest
```
Com o docker run -d iniciamos o nosso contêiner iniciar se desprender do nosso terminal, caso contrário ficariamos rodando o contêiner e ele pararia assim que cortássemos o processo, desse modo o contêiner fica rodando por "trás".

--name devldmusic damos nome para esse contêiner. 

-v "$(pwd)":/usr/src/app dizemos para espelhar a nossa pasta raiz do sistema na pasta do contêiner, assim toda mudança ou adição feita no diretório local será feita também dentro do contêiner, assim, persistiremos os dados alterados no contêiner.

-p 5000:5000 dizemos que a porta 5000 do contêiner se espelhará na porta 5000 do nosso localhost, assim ao acessar localhost:5000/cadastro poderemos acessar o nosso sistema que está rodando dentro do contêiner.

E finalmente com o ldmusicpy:latest dizemos qual é a imagem base que esse contêiner utilizará!

Acesse o http://localhost:5000/index e voílà!

Remova tudo criado pelos comandos anteriores com:

```powershell
docker system prune -all --force
```
Vamos facilitar!

##### Docker-compose.yml

Para facilitar o processo criei um docker-compose.yml, que é basicamente um arquivo onde expressamos quais são os contêineres que compõem nossa aplicação(web, banco, phpmyadmin, por exemplo). Através dele e do Dockerfile abstraímos a criação da nossa infraestrutura para o docker, podendo **focar apenas no código** do nosso sistema, sem muita complicação.

Dá uma olhadinha no garotão aqui: 

*docker-compose.yml*

Para iniciar a aplicação e todos os contêineres que ela necessita para funcionar basta apenas um simples comando:

``docker-compose up -d --build``

--build é usado pra reconstruir a imagem, caso ela tenha sido alterada (no caso da imagem web)
Obs: Omita o -d caso queira ver os logs da aplicação no terminal

E para encerrar a aplicação

``docker-compose down``
