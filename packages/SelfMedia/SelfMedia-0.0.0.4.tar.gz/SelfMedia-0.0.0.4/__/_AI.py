from .__ import *

from ._Stamp import Stamp
from ._Audio import Audio
from ._Texture import Texture


class VAD:
	_model = None
	_tools = None

	def probe(
		self,
		audio: Audio,
		thresh: float = 0.8,
		minGran: int = 150,
		minGap: int = 100,
		pad: int = 200,
	):
		if not (self._model and self._tools):
			print('[VAD]')
			self._model, self._tools = torch.hub.load(
				repo_or_dir='snakers4/silero-vad',
				model='silero_vad',
				verbose=False
			)
			pass

		print('<probe>')
		fStamps: list[dict] = self._tools[0](
			audio.sig,
			self._model,
			sampling_rate=audio.fps,
			threshold=thresh,
			min_speech_duration_ms=minGran,
			min_silence_duration_ms=minGap,
			speech_pad_ms=pad,
			window_size_samples=1024,
		)
		return Texture([SSAEvent(*Stamp(*_.values(), unit=audio.fps)) for _ in fStamps])

	pass


class Whisper:
	_size = None
	_model = None

	def __init__(self, size: str):
		self._size = size
		pass

	def trans(
		self,
		audio: Audio,
		cont: Texture,
		lang: str = 'Chinese',
		accent: str = 'zh-cn',
	):
		if not self._model:
			print('[Whisper]')
			self._model = whisper.load_model(self._size)
			pass

		print('<trans>')
		___ = Texture()
		prompt = None

		for contEvent in cont:
			clip = audio.pick(contEvent)
			res = self._model.transcribe(
				clip.sig,
				language=lang,
				prompt=prompt,
				no_speech_threshold=0.2,
				temperature=0,
			)

			prompt = ''
			for seg in res['segments']:
				msStamp = [round(seg[_] * 1000) for _ in ['start', 'end']]
				segEvent = SSAEvent(*msStamp, seg['text'])
				segEvent.shift(ms=contEvent.start)

				t = min(segEvent.end, contEvent.end)
				if segEvent.start < t:
					segEvent.end = t
					segEvent.text = regex.sub('[,?。，？]', ' ', segEvent.text)
					segEvent.text = segEvent.text.strip()
					if accent:
						segEvent.text = zhconv.convert(segEvent.text, accent)
						pass
					___.append(segEvent)
					prompt += segEvent.text
					pass
				pass

			prompt = prompt.replace(' ', '')
			pass
		return ___

	pass
