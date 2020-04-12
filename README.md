## Tutorial *ldMusic*

*Versão: 0.1*

Tutorial básico para compartilhamento e nivelamento de conhecimento para o desenvolvimento da plataforma

#### **Git**

Facilitar a entrega de pequenas modificações e adições de recursos localmente(no PC de cada um) para o repositório remoto no [Github](https://github.com/marconifj/ldMusic), e também fazer o versionamento do Sistema.

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

Abra o CMD e digite:

```powershell
docker run hello-world
```

Depois veja se baixou a imagem de hello-world

```powershell
docker images
```

Agora vamos construir a nossa Imagem Base, que será criada através dos comandos contidos no arquivo Dockerfile
(Antes de executar esse comando, confirme que você está na pasta raiz do projeto ldMusic)
```powershell
docker build -t ldmusicpy:latest .
```
Pronto! Agora nossa imagem já está no nosso repositório local e já podemos subir nosso conteiner contendo a nossa aplicação rodando!

```powershell
docker run -d --name devldmusic -v "$(pwd)":/usr/src/app -p 5000:5000 ldmusicpy:latest
```

