from flask import Flask, request, render_template
from collections import Counter
import math

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    table_data = []
    if request.method == 'POST':
        uploaded_file = request.files.get('text_file')
        if uploaded_file:
            text = uploaded_file.read().decode('utf-8')
            # Обработка текста
            # Разделение на слова, приведение к нижнему регистру, удаление знаков препинания
            import re
            words = re.findall(r'\b\w+\b', text.lower())
            total_words = len(words)
            word_counts = Counter(words)
            # Вычисляем tf и idf
            # tf = частота слова
            # idf = log(1 + (общее количество слов / частота слова))
            # В данном случае для упрощения считаем, что document frequency = (частота слова / общее количество слов),
            # и для idf используем формулу log(1 + N / df)
            # Но поскольку у нас один документ, то "обратная частота документа" можно интерпретировать как log(1 + 1 / tf)
            # Однако, в оригинальной постановке, скорее, имеется в виду, что idf = log(N / df),
            # где N — число документов. Так как у нас один документ, то idf можно считать как log(1 + (общее число слов / tf))
            # Для примера, используем следующую формулу:

            N = total_words
            data = []
            for word, count in word_counts.items():
                tf = count
                idf = math.log(1 + N / tf)
                data.append((word, tf, idf))
            # Сортируем по убыванию idf
            data.sort(key=lambda x: x[2], reverse=True)
            # Берем только первые 50 слов
            table_data = data[:50]
    return render_template('index.html', table_data=table_data)

if __name__ == '__main__':
    app.run(debug=True)