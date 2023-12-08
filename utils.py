import csv


async def get_keywords_and_channels():
    csv_file_path = 'example.csv'

    column_names = ['destination_channel_words',
                    'keywords_1_lemma',
                    'keywords_2_lemma',
                    'keywords_3_valid',
                    'keywords_4_minus_lemma',
                    'keywords_5_minus_valid']

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=column_names)

        # Пропускаем первую строку (названия колонок)
        next(reader)

        destination_channel_words = []
        keywords_1_lemma = []
        keywords_2_lemma = []
        keywords_3_valid = []
        keywords_4_minus_lemma = []
        keywords_5_minus_valid = []

        for row in reader:
            destination_channel_words.append(row['destination_channel_words'].strip())
            keywords_1_lemma.append(row['keywords_1_lemma'].strip())
            keywords_2_lemma.append(row['keywords_2_lemma'].strip())
            keywords_3_valid.append(row['keywords_3_valid'].strip())
            keywords_4_minus_lemma.append(row['keywords_4_minus_lemma'].strip())
            keywords_5_minus_valid.append(row['keywords_5_minus_valid'].strip())

        keywords = {
            'first_lemma': list(filter(None, keywords_1_lemma)),
            'second_lemma': list(filter(None, keywords_2_lemma)),
            'valid_word': list(filter(None, keywords_3_valid)),
            'minus_lemma': list(filter(None, keywords_4_minus_lemma)),
            'minus_valid_word': list(filter(None, keywords_5_minus_valid))
        }

        return list(filter(None, destination_channel_words)), keywords
