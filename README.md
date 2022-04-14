Flask restfull API test proj

including JWT/JWT extended (fresh/no fresh | refresh |blacklist/logout)

uwsgi emperor configuration

uwsgi metrics extended with influx + telegraph / grafana

(Also tested free heroku dyno node + CD/CI)

wrk also is used to test Resource API's performance

Suggestion for wrk after compile (openssl required):

./wrk -t{int:thread} -c{int:connections} -d{int:seconds}s -R1 {api/resource}

no tox, no coverage ( this project is intended just for test/stud purposes)
