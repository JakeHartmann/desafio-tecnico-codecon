Minha tentativa de fazer [esse desafio](https://github.com/codecon-dev/desafio-1-1s-vs-3j) que surgiu desse [vídeo](https://youtu.be/AFtRYXJVO-4) do pessoal gente finissima da [Codecon](https://github.com/codecon-dev) antes mesmo de ver como os participantes resolveram.

Demorou definitivamente mais do que a 1 hora estipulada, já que foi meu maior contato com JSON até o momento e aprendi bastante sobre algumas peculiaridades do Flask. Acho que é um baita recurso pra ser implementado em outras linguagens e ver como elas funcionam, quem sabe tento fazer com um Gin ou um Ktor.

---

## Performance dos endpoints de acordo com a rota `GET "/evaluation"`
Tempo em ms da média aritmética de 5 requisições feitas utilizando o [Bruno](https://github.com/usebruno/bruno) na mesma máquina rodando o servidor local

`GET "/active-users-per-day"`: 46.53ms

`GET "/superusers"`: 99.84ms

`GET "/team-insights"`: 56.79ms

`GET "/top-countries"`: 12.39ms

Mesmo tendo feito em Python (com todo devido respeito), fiquei muito satisfeito com a performance, que atendeu tranquilamente o requisito técnico de tempo de resposta < 1s por endpoint.
