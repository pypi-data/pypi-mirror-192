from .__ import ____
from .__ import *

from ._Audio import Audio
from ._Stamp import Stamp


class Texture(SSAFile):

	def __init__(self, tex: Union[SSAFile, list[SSAEvent]] = None):
		super().__init__()
		if tex:
			self.extend([_.copy() for _ in tex])
		pass

	def aggrByGran(self, maxGran: int = ____.MAX_GRAN):
		if len(self) <= 1:
			___ = Texture(self)
			pass
		elif self[-1].end - self[0].start < maxGran:
			text = '\n'.join([_.text for _ in self])
			event = SSAEvent(self[0].start, self[-1].end, text)
			___ = Texture([event])
			pass
		else:
			key = lambda _: self[_].start - self[_ - 1].end
			theIdx = max(range(1, len(self)), key=key)

			_L = Texture(self[:theIdx])
			_L = _L.aggrByGran(maxGran)

			_R = Texture(self[theIdx:])
			_R = _R.aggrByGran(maxGran)

			___ = Texture(_L.events + _R.events)
			pass
		return ___

	def aggrByGap(self, minGap: int = ____.MIN_GAP):
		___ = Texture()
		lastEnd = -minGap - 1
		for event in self:
			if event.start - lastEnd > minGap:
				___.append(event.copy())
				pass
			else:
				___[-1].end = event.end
				___[-1].text = '\n'.join([___[-1].text, event.text])
				pass
			lastEnd = ___[-1].end
			pass
		return ___

	def calib(self, audio: Audio, db: float, step: int = ____.STEP):
		print('<calibrate>')
		DURA = audio.dura()
		___ = Texture(self)
		N = len(___)

		for i in range(N):
			cap = [
				0 if i == 0 else ___[i - 1].end,
				DURA if i == N - 1 else ___[i + 1].start,
			]
			lastDura = 0
			done = False
			while not done:
				stamp_1 = Stamp(
					max(cap[0], ___[i].start - step),
					min(cap[1], ___[i].end + step),
				)
				_, stamp_2 = audio[stamp_1].trim(db)
				stamp_2 = stamp_2.shift(stamp_1[0])

				dura = stamp_2[1] - stamp_2[0]
				done = (dura <= lastDura)
				if not done:
					___[i].start, ___[i].end = stamp_2
					lastDura = dura
					pass
				pass
			pass
		return ___

	def extent(self, ex: list[int]):
		print('<extent>')
		___ = Texture(self)
		N = len(___)

		___[0].start = max(___[0].start - ex[0], 0)
		___[N - 1].end = ___[N - 1].end + ex[1]

		for i in range(1, N):
			___[i].start = max(___[i].start - ex[0], ___[i - 1].end)
			___[i - 1].end = min(___[i - 1].end + ex[1], ___[i].start)
			pass
		return ___

	def withAccent(self, accent: str):
		print('<withAccent>')
		___ = Texture(self)
		for event in ___:
			event.text = zhconv.convert(event.text, accent)
			pass
		return ___

	def toSketch(self, refFiPa: Path, fps: int):
		meta = ____.getMediaMeta(refFiPa)

		elemRate = \
			____.elem('rate', children=[
				____.elem('timebase', text=fps)
			])

		elemFile = \
			____.elem('file', {'id': ____.REF_ID}, children=[
				____.elem('pathurl', text=refFiPa.name),
				____.elem('duration'),
				____.elem('media', children=[
					____.elem('video'),
					____.elem('audio', children=[
						____.elem('channelcount', text=2),
					]),
				])
			])

		formats = [_['codec_type'] for _ in meta['streams']]

		trackAttrs = {
			'video': None,
			'audio': {
				'currentExplodedTrackIndex': 0,
				'premiereTrackType': 'Stereo',
			},
		}
		elemTracks = {_: ____.elem('track', trackAttrs[_]) for _ in formats}

		__MS2F = lambda _: round(_ / 1000 * fps)
		__ID = lambda fmt, idx: '%s_%04d' % (fmt[0].upper(), idx + 1)

		for _idx, event in enumerate(self):
			idx = _idx + 1
			for fmt, elemTrack in elemTracks.items():
				clipAttrs = {
					'video': {'id': __ID(fmt, idx)},
					'audio': {'id': __ID(fmt, idx), 'premiereChannelType': 'stereo'}
				}

				elemClip = \
					____.elem('clipitem', clipAttrs[fmt], children=[
						____.elem('name', text=refFiPa.name),
						elemRate,
						elemFile,
						____.elem('start', text=__MS2F(event.start)),
						____.elem('end', text=__MS2F(event.end)),
						____.elem('in', text=__MS2F(event.start)),
						____.elem('out', text=__MS2F(event.end)),
					])

				for _ in formats:
					elemLink = \
						____.elem('link', children=[
							____.elem('linkclipref', text=__ID(_, idx)),
							____.elem('mediatype', text=_),
							____.elem('trackindex', text=1),
							____.elem('clipindex', text=idx),
						])
					elemClip.append(elemLink)
					pass

				elemTrack.append(elemClip)
				pass
			pass

		elemMedia = ____.elem('media')
		for fmt, elemTrack in elemTracks.items():
			if fmt == 'video':
				elemFormat = \
					____.elem('format', children=[
						____.elem('samplecharacteristics', children=[
							____.elem('pixelaspectratio', text='square'),
							____.elem('width', text=meta['streams'][0]['width']),
							____.elem('height', text=meta['streams'][0]['height']),
						])
					])
				el = ____.elem(fmt, children=[elemFormat, elemTracks[fmt]])
				pass
			else:
				el = ____.elem(fmt, children=[elemTracks[fmt]])
				pass
			elemMedia.append(el)
			pass

		___ = \
			____.elem('xmeml', {'version': 5}, children=[
				____.elem('sequence', children=[
					____.elem('name', text=refFiPa.stem),
					elemRate,
					elemMedia,
				]),
			])
		___ = ET.ElementTree(___)
		ET.indent(___, '\t')
		return ___

	pass
