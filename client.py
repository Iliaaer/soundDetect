from pyannote.audio import Pipeline
import whisper

def millisec(timeStr):
    spl = timeStr.split(":")
    s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]) )* 1000)
    return s

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
                                    use_auth_token="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")

# model = whisper.load_model("medium")
model = whisper.load_model("large-v2")
print(model.is_multilingual)


FILE_NAME = "5"

diarization = pipeline("wav/" + FILE_NAME + ".wav")

for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"start={turn.start*1000}s stop={turn.end*1000}s speaker_{speaker}")
    
# print(diarization, type(diarization))

# with open("detect/audio_" + FILE_NAME + ".rttm", "w") as rttm:
#     diarization.write_rttm(rttm)