import whisper
from pyannote.audio import Pipeline
from src.config import PIPELINE_TOKEN

DEVICE_WHISPER = 'cpu'
MODEL_WHISPER  = 'large'


pipeline = Pipeline.from_pretrained(
    'pyannote/speaker-diarization@2.1',
    use_auth_token=PIPELINE_TOKEN
)

LANGUAGE: str = 'ru'; MIN_SPEAKERS: int = 1; MAX_SPEAKERS: int = 2; NUM_SPEAKERS: int = 2
out_file_path = "example.wav"
audio_file = f'wav/{out_file_path}'

diarization_result = pipeline(audio_file, num_speakers=NUM_SPEAKERS)
from pyannote.core import notebook
notebook.reset()
who_speaks_when = diarization_result.rename_labels({"SPEAKER_00": "Гоtesворящий 1", "SPEAKER_01": "Говорящий 2"})

model = whisper.load_model(
    name=MODEL_WHISPER, 
    device=DEVICE_WHISPER
)

from pyannote.audio import Audio
audio = Audio(sample_rate=16000, mono=True)

for segment, _, speaker in who_speaks_when.itertracks(yield_label=True):
    waveform, sample_rate = audio.crop(audio_file, segment)
    text = model.transcribe(waveform.squeeze().numpy(), language=LANGUAGE)["text"]
    time = f"{segment.start:.2f}:{segment.end:.2f}"
    print(f"{time} - {speaker}: {text}")

