from FlaskdbServer import FlaskdbServercls
import os
# export HF_HOME=/home/grigoriev_adm/AI/dev/llm_aws/docker-db/cache
# os.environ['HF_HOME'] = '/your/custom/cache/directory'


os.environ["AWS_ACCESS_KEY_ID"] = ""
os.environ["AWS_SECRET_ACCESS_KEY"] = ""
os.environ["AWS_REGION_NAME"] = ""


if __name__=="__main__":
    flask_server=FlaskdbServercls("twi")
    flask_server.start()
