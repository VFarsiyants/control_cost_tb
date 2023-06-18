FROM python:3.11.2
RUN mkdir -p /usr/src/control_cost_bot
WORKDIR /usr/src/control_cost_bot
COPY . /usr/src/control_cost_bot/
RUN pip install --no-cache-dir -r requirements.txt
RUN sed -i 's/\r$//g' /usr/src/control_cost_bot/docker-entrypoint.sh
RUN chmod +x /usr/src/control_cost_bot/docker-entrypoint.sh
