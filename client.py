from pyannote.audio import Pipeline
import whisper
import json

FILE_NAME = "5"
MIN_SPEAKERS = 1
MAX_SPEAKERS = 2
LANGUAGE_WHISPER = "ru"
MODEL_NAME = "large"

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
                                    use_auth_token="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")

# model = whisper.load_model("medium")
model = whisper.load_model(MODEL_NAME)
audio = whisper.load_audio("wav/" + FILE_NAME + ".wav")

diarization = pipeline("wav/" + FILE_NAME + ".wav", min_speakers=MIN_SPEAKERS, max_speakers=MAX_SPEAKERS)

for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"start={turn.start}s stop={turn.end}s speaker_{speaker}")

result = model.transcribe(audio, language=LANGUAGE_WHISPER, fp16=False, verbose=True)
# jsonResult = json.dumps(result, indent=4, ensure_ascii=False)
# with open('detect/audio_text_' + FILE_NAME + '.json', 'w') as outfile:
#     json.dump(jsonResult, outfile, indent=2)

# print(result["text"])

with open("detect/audio_" + FILE_NAME + ".rttm", "w") as rttm:
    diarization.write_rttm(rttm)

'''



'''