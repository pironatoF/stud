Flask restfull API test proj

including JWT/JWT extended (fresh/no fresh | refresh |blacklist/logout)

uwsgi emperor configuration

uwsgi metrics extended with influx + telegraph / grafana

(Also tested free heroku dyno node + CD/CI)

wrk also is used to test Resource API's performance

Suggestion for wrk after compile (openssl required):

./wrk -t{int:thread} -c{int:connections} -d{int:seconds}s -R1 {api/resource}

no tox, no coverage ( this project is intended just for test/stud purposes)

![Schermata da 2022-04-14 06-11-38](https://user-images.githubusercontent.com/13415369/163312257-758b77ac-cdb6-48f4-abc5-fc1f2a2fd660.png)
