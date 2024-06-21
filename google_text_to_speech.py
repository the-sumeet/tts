import os
from google.cloud import texttospeech
import os
from google.cloud import texttospeech_v1beta1 as tts
import json
from pathlib import Path
from google.cloud import texttospeech_v1beta1 as tts


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/sumeetmathpati/Projects/sumeet/tts/pro-micron-427112-r1-280f377c5068.json"



def go_ssml(basename: Path, ssml):
    client = tts.TextToSpeechClient()
    voice = tts.VoiceSelectionParams(
        language_code="en-AU",
        name="en-AU-Wavenet-B",
        ssml_gender=tts.SsmlVoiceGender.MALE,
    )

    response = client.synthesize_speech(
        request=tts.SynthesizeSpeechRequest(
            input=tts.SynthesisInput(ssml=ssml),
            voice=voice,
            audio_config=tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3),
            enable_time_pointing=[
                tts.SynthesizeSpeechRequest.TimepointType.SSML_MARK]
        )
    )

    # cheesy conversion of array of Timepoint proto.Message objects into plain-old data
    marks = [dict(sec=t.time_seconds, name=t.mark_name)
             for t in response.timepoints]

    name = basename.with_suffix('.json')
    with name.open('w') as out:
        json.dump(marks, out)
        print(f'Marks content written to file: {name}')

    name = basename.with_suffix('.mp3')
    with name.open('wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to file: {name}')


template = """
<speak>
<mark name="Go"/> Go <mark name="from"/> from <mark name="here,"/> here, <mark name="to"/> to <mark name="there"/> there!
</speak>
"""

word_marks = ""
text_file = open("txt", "r")
text = str(text_file.read())
words = text.split(" ")
for word in words:
    word_marks += f' <mark name="{word}"/> {word}'

go_ssml(Path.cwd() / 'demo', f"""
<speak>
{word_marks}
</speak>
    """.strip())

# go_ssml(Path.cwd() / 'demo', template)
