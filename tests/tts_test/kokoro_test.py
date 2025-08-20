from kokoro import KPipeline
import soundfile as sf
import torch
pipeline = KPipeline(lang_code='fr-fr')
text = '''
Le dromadaire resplendissant déambulait tranquillement dans les méandres en mastiquant de petites feuilles vernissées.
'''
generator = pipeline(text, voice='ff_siwis')
for i, (gs, ps, audio) in enumerate(generator):
    print(i, gs, ps)
    sf.write(f'../../tests/tts_test/{i}.wav', audio, 24000)

