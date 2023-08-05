from    pydub               import AudioSegment
import  speech_recognition  as sr

class AudioConfig:
    def convertAudioMp3toWav(initialDir, finalDir, initialNameArchive, finalNameArchive):
        sound = AudioSegment.from_mp3(initialDir + "\\" + initialNameArchive + ".mp3")
        sound.export(finalDir + "\\" + finalNameArchive + ".wav", format="wav")

    def listenAudioWav(dirArchive, nameArchive):
        sample_audio = sr.AudioFile(dirArchive + "\\" + nameArchive + ".wav")

        microfone = sr.Recognizer()
        with sample_audio as source:
            audio = microfone.record(source)

        key = microfone.recognize_google(audio)

        return key