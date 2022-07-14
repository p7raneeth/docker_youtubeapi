FROM python:latest 

COPY ./ ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "youtube_comments-sentiment_analysis.py","BJ8hiBoDf6c"]