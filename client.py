from pyannote.audio import Pipeline
import whisper

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
                                    use_auth_token="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")

# model = whisper.load_model("medium")
model = whisper.load_model("large")



FILE_NAME = "5"
MIN_SPEAKERS = 1
MAX_SPEAKERS = 2


diarization = pipeline("wav/" + FILE_NAME + ".wav", min_speakers=MIN_SPEAKERS, max_speakers=MAX_SPEAKERS)

for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"start={turn.start*1000}s stop={turn.end*1000}s speaker_{speaker}")
    
# print(diarization, type(diarization))

# with open("detect/audio_" + FILE_NAME + ".rttm", "w") as rttm:
#     diarization.write_rttm(rttm)