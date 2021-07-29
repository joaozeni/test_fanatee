# Fanatee challenge
### Necesário para rodar
Para executar o projeto é necessário possuir o docker e docker-compose.

Link para instalação:
* Docker: https://docs.docker.com/install/linux/docker-ce/ubuntu/
* Docker-compose: https://docs.docker.com/compose/install/

Também é necessário possuir o click e o python-requests.
* Comando para instalar: pip3 install click requests

### Rodando o projeto
O docker monta o projeto e DB.

* Comando para rodar: docker-compose up

Assim que tudo for executado o projeto estará rodando e o banco criado.
Os testes também são executados logo antes de subir os endpoints.

### Executando o endpoint
Para executar o endpoint é possivel utilizar a documentação do swagger.
Para isso com o projeto rodando acesse: http://localhost:5000/apidocs/

### Executando o cli
Para executar pode-se utilizar o python, o cli possui um --help.
* Comando a executar: python3 paths_cli.py --help
Também é possível transformar o mesmo em executavel.
* Comando para transformar em executavel: chmod +x paths_cli.py
Assim será executando como uma linha comando tradicional
* Comando com executavel ./paths_cli.py --help
Feito isso você pode transferir para umas das pastas que esteja no seu path de sistema e se torná um comando
