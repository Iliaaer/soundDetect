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
options = whisper.DecodingOptions(language=LANGUAGE_WHISPER, fp16=False)

# diarization = pipeline("wav/" + FILE_NAME + ".wav", min_speakers=MIN_SPEAKERS, max_speakers=MAX_SPEAKERS)

# for turn, _, speaker in diarization.itertracks(yield_label=True):
#     print(f"start={turn.start*1000}s stop={turn.end*1000}s speaker_{speaker}")

result = model.transcribe(audio, **options.__dict__, verbose=False)
jsonResult = json.dumps(result)
with open('detect/audio_text_' + FILE_NAME + '.txt', 'w') as outfile:
    json.dump(jsonResult, outfile)

# with open("detect/audio_" + FILE_NAME + ".rttm", "w") as rttm:
#     diarization.write_rttm(rttm)