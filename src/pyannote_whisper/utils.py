from pyannote.core import Segment, Annotation, Timeline


def get_text_with_timestamp(transcribe_res):
    """
    Функция get_text_with_timestamp принимает объект transcribe_res и возвращает список кортежей.
    Каждый кортеж содержит время начала и окончания каждого сегмента, а также текст, который был произнесен во время этого сегмента.
    
    :параметр transcribe_res: Передать ответ из функции transcribe_audio
    :return: Список кортежей
    """
    timestamp_texts = []
    for item in transcribe_res['segments']:
        start = item['start']
        end = item['end']
        text = item['text']
        timestamp_texts.append((Segment(start, end), text))
    return timestamp_texts


def add_speaker_info_to_text(timestamp_texts, ann):
    """
    Функция add_speaker_info_to_text принимает список кортежей, содержащих временную метку и текст для каждого сегмента,
    и добавляет информацию о динамике к каждому кортежу. Функция возвращает список кортежей, состоящий из трех элементов: 
    временная метка, идентификатор говорящего и текст.
    
    :параметр timestamp_texts: Передает список кортежей, содержащих временную метку и текст, подлежащий обработке
    :параметр ann: Обрезать сегмент
    :return: Список кортежей
    """
    spk_text = []
    for seg, text in timestamp_texts:
        spk = ann.crop(seg).argmax()
        spk_text.append((seg, spk, text))
    return spk_text


def merge_cache(text_cache):
    """
    Функция merge_cache принимает список кортежей, каждый из которых содержит следующее:
        - Объект сегмента (время начала и окончания)
        - Идентификатор динамика для этого сегмента
        - Текст, связанный с этим сегментом.
    
    :параметр text_cache: Сохраняет текстовые сегменты, которые в данный момент обрабатываются
    :return: Кортеж формы (сегмент, говорящий, предложение)
    """
    sentence = ''.join([item[-1] for item in text_cache])
    spk = text_cache[0][1]
    start = text_cache[0][0].start
    end = text_cache[-1][0].end
    return Segment(start, end), spk, sentence


PUNC_SENT_END = ['.', '?', '!']


def merge_sentence(spk_text):
    """
    Функция merge_sentence принимает список кортежей (seq, speak, text) и объединяет текст в предложения.
    Функция возвращает список кортежей (seg_start, seg_end, spk, предложение).
    
    :параметр spk_text: Сохраняет текст каждого выступающего
    :return: Список кортежей
    """
    merged_spk_text = []
    pre_spk = None
    text_cache = []
    for seg, spk, text in spk_text:
        if spk != pre_spk and pre_spk is not None and len(text_cache) > 0:
            merged_spk_text.append(merge_cache(text_cache))
            text_cache = [(seg, spk, text)]
        elif text[-1] in PUNC_SENT_END:
            text_cache.append((seg, spk, text))
            merged_spk_text.append(merge_cache(text_cache))
            text_cache = []
        else:
            text_cache.append((seg, spk, text))
        pre_spk = spk

    if len(text_cache) > 0:
        merged_spk_text.append(merge_cache(text_cache))
    return merged_spk_text


def diarize_text(transcribe_res, diarization_result):
    """
    Функция diarize_text принимает результаты задания на транскрипцию и
    ведение дневника и возвращает список строк, содержащих текст, произнесенный каждым говорящим.
    
    :параметр transcribe_res: Получить текст из результата транскрипции
    :параметр diarization_result: Получить информацию о динамике
    :return: Список кортежей
    """
    timestamp_texts = get_text_with_timestamp(transcribe_res)
    spk_text = add_speaker_info_to_text(timestamp_texts, diarization_result)
    return merge_sentence(spk_text)


def write_to_txt(spk_sent, file):
    """
    Функция write_to_txt принимает список кортежей, каждый из которых содержит время начала и окончания сегмента,
    имя говорящего и произнесенное предложение. Затем он записывает эту информацию в текстовый файл.
    
    :параметр spk_sent: Записать данные в текстовый файл
    :param file: Укажите имя файла, в который будет записываться
    :return: Файл, содержащий время начала и окончания каждого предложения,
    """
    with open(file, 'w') as fp:
        for seg, spk, sentence in spk_sent:
            line = f'{seg.start:.2f} {seg.end:.2f} {spk} {sentence}\n'
            fp.write(line)
