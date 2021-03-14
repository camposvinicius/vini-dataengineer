# Terraform - Exercícios

Vamos implementar um exercício bastante próximo do dia a dia da Engenharia de Dados na A3. Utilizando o [Rony](https://github.com/a3data/rony), abra um novo projeto. Você precisará de um repositório no github para testar sua solução e também de uma conta AWS Free Tier.

Use o Rony para subir a seguinte estrutura:

- Um bucket S3 que será o *data lake*;
- Uma database no glue chamada *onboarding-a3-<meu-nome>*;
- Um glue crawler que vai ler tudo o que está nesse bucket, dentro de uma pasta chamada *consumer-zone* (a pasta não precisa existir e o crawler não vai precisar ser executado. Ele apenas deve ser configurado dessa maneira.)
- Uma função lambda que faz o download do dado que está no endereço **https://raw.githubusercontent.com/neylsoncrepalde/titanic_data_with_semicolon/main/titanic.csv** e deposita no S3 em uma pasta chamada **raw-data**;
- Um log group para armazenar logs de execução do lambda com período de expiração de 14 dias;
- Roles para o Lambda e o Glue Crawler
- Permissões para ler e escrever dados no bucket S3.

### Observações

- Pode consultar o A3Tech que fizemos sobre o Rony abordando uma construção parecida com a mencionada acima: https://drive.google.com/file/d/1hPT11a59kBWgPhNrr4eLAqTVqTmpI7oS/view 
- Para solicitar acesso, procure o [Arthur Assis](arthur.assis@a3data.com.br) 
- O repositório com esta implementação encontra-se aqui: https://github.com/a3data/exemplo_rony.

Após subir a estrutura, execute a função Lambda para que o arquivo do Titanic fique disponível no bucket S3. Após a conclusão do exercício, altere o arquivo **3-3-terraform-respostas.md** com o endereço do repositório criado para o projetinho e coloque prints das telas do ambiente AWS na pasta **3-terraform/img/**.

**Divirta-se!**

---

[> Voltar para o conteúdo anterior - 3-1-terraform-conteudo](3-1-terraform-conteudo.md)

[> Ir para o próximo conteúdo - 3-3-terraform-respostas](3-3-terraform-respostas.md)

[> Voltar para a HOME](../README.md)