FROM python:3

WORKDIR /usr/src/app/examples

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

RUN ln -s /usr/src/app/cli.py /usr/local/bin/takathon
RUN chmod +x /usr/src/app/cli.py

CMD ["bash"]
