FROM python:3.9-alpine
RUN apk --update add gcc build-base
RUN pip install --no-cache-dir kopf kubernetes
ADD wordle_operator.py calculate_word.py wordlist.py /
CMD kopf run /wordle_operator.py