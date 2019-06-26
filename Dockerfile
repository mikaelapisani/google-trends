FROM python:3
LABEL version="1.0"
LABEL description="GoogleTrends ETL"
LABEL maintainer="mikaela.p.leal@ttu.edu"

RUN git clone -b devel https://github.com/mikaelapisani/google-trends.git /root/google-trends

WORKDIR /root/google-trends

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
VOLUME /root/data
VOLUME /root/results

RUN sed -i 's/tickers_folder=.*$/tickers_folder=\/root\/data\//' config.properties
RUN sed -i 's/data_folder_monthly=.*$/data_folder_monthly=\/root\/data\/monthly\//' config.properties
RUN sed -i 's/data_folder_daily=.*$/data_folder_daily=\/root\/data\/daily\//' config.properties
RUN sed -i 's/result_folder=.*$/result_folder=\/root\/results\//' config.properties
