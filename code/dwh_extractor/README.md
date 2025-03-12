# Hinojosa DWH Extractor

## Build image

docker build -t europe-southwest1-docker.pkg.dev/pj-data-des/ar-pj-data-des/data_extractor:latest .

docker push europe-southwest1-docker.pkg.dev/pj-data-des/ar-pj-data-des/data_extractor:latest

docker build -t europe-southwest1-docker.pkg.dev/pj-data-pro/ar-pj-data-pro/data_extractor:latest .

docker push europe-southwest1-docker.pkg.dev/pj-data-pro/ar-pj-data-pro/data_extractor:latest

## Architecture diagram

[![](https://mermaid.ink/img/pako:eNp9lFFPszAYhf_K0mv1B-ziS9jAjQ3dRrkwXzGkg3cMhbYpxWiM_92u1VGRyRXnvM97ODRs7yjnBaApKiUVx0nip2yir7bbWyNkCuSB5tDawenyiLcNHyfX1_8mMzKjLXiiCl6VpLni8tHhDDInYGcZFVVWUEUdxCf-zCYFJsnfjwX5hrg9BzkhwIqUDTqfI5zOC4KPVILgFVNR1ar-MfY9enJJFpyXNfiyeoHLWOgE3lb1H-SKYCoG46Afr8lGT34FOERE8C7CIF9AjkNjh3BHK9ZH3JFG6xvxZvfuSfCQxN482cSZH-Ktl8yXQeyc-L3BFkNjOTTCobEaGuuhEV3ujPWL0RL6jQ1prXVuviWdqDktMsWzr5lTe2OYHdnT_LkTGa-LjO-fIFftLygmEk4BkH3DP8CxenPODlXZB2GSG-dU7vJWxMsSZL-VkNo4o1sz0y2xInDFwghsxdIVoStWrli7InLF1o3euSK2Al2hBqT-aAr93_B-GqVIHaGBFE31bUHlc4pS9qE52imO31iOpkp2cIUk78ojmh5o3WrVCf1rBb-i-jSab0RQ9p_z5gv6-AQVpU7M?type=png)](https://mermaid.live/edit#pako:eNp9lFFPszAYhf_K0mv1B-ziS9jAjQ3dRrkwXzGkg3cMhbYpxWiM_92u1VGRyRXnvM97ODRs7yjnBaApKiUVx0nip2yir7bbWyNkCuSB5tDawenyiLcNHyfX1_8mMzKjLXiiCl6VpLni8tHhDDInYGcZFVVWUEUdxCf-zCYFJsnfjwX5hrg9BzkhwIqUDTqfI5zOC4KPVILgFVNR1ar-MfY9enJJFpyXNfiyeoHLWOgE3lb1H-SKYCoG46Afr8lGT34FOERE8C7CIF9AjkNjh3BHK9ZH3JFG6xvxZvfuSfCQxN482cSZH-Ktl8yXQeyc-L3BFkNjOTTCobEaGuuhEV3ujPWL0RL6jQ1prXVuviWdqDktMsWzr5lTe2OYHdnT_LkTGa-LjO-fIFftLygmEk4BkH3DP8CxenPODlXZB2GSG-dU7vJWxMsSZL-VkNo4o1sz0y2xInDFwghsxdIVoStWrli7InLF1o3euSK2Al2hBqT-aAr93_B-GqVIHaGBFE31bUHlc4pS9qE52imO31iOpkp2cIUk78ojmh5o3WrVCf1rBb-i-jSab0RQ9p_z5gv6-AQVpU7M)


## Useful commands (old)

gcloud compute scp ../data_extractor/  javier_roger@vpn-conn-test:/home/javier_roger --project pj-data-des --zone europe-southwest1-a --recurse

docker run -v "$HOME/.config/gcloud/application_default_credentials.json":/gcp/creds.json:ro --env GOOGLE_APPLICATION_CREDENTIALS=/gcp/creds.json --env GOOGLE_CLOUD_PROJECT=pj-data-des --env ORIGIN=CIRCUTOR_PA_PS --env EXTRACTOR=SQL_SERVER --env TARGET=devices europe-southwest1-docker.pkg.dev/pj-data-des/ar-pj-data-des/data_extractor:latest

docker run -v "$HOME/.config/gcloud/application_default_credentials.json":/gcp/creds.json:ro --env GOOGLE_APPLICATION_CREDENTIALS=/gcp/creds.json --env GOOGLE_CLOUD_PROJECT=pj-data-des --env ORIGIN=SIMATIC_IT --env EXTRACTOR=SQL_SERVER --env TARGET=LogEnergia europe-southwest1-docker.pkg.dev/pj-data-des/ar-pj-data-des/data_extractor:latest
