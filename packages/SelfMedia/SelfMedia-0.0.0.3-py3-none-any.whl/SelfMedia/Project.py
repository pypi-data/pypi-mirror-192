from .__ import ____
from .__ import *

from ._AI import VAD, Whisper
from ._Audio import Audio
from ._Texture import Texture


class Project:
	__vad: VAD = None
	__whisp: Whisper = None

	__proxy: Audio = None
	__prim: Texture = None
	__draft: Texture = None
	__chop: Texture = None
	__regular: Texture = None
	__timeline: ET.ElementTree = None
	__proof: Texture = None

	_rawFiPa: Path = None
	_proxyFiPa: Path = None
	_primFiPa: Path = None
	_draftFiPa: Path = None
	_chopFiPa: Path = None
	_regularFiPa: Path = None
	_timelineFiPa: Path = None
	_previewFiPa: Path = None
	_proofFiPa: Path = None
	_dummyFiPa: Path = None

	def __init__(self, vad: VAD, whisp: Whisper, projDiPa: Path):
		self.__vad = vad
		self.__whisp = whisp

		title = projDiPa.name

		rawStem = title + ____.SEP + '0_Raw'
		self._rawFiPa = [_ for _ in projDiPa.iterdir() if _.stem == rawStem][0]
		self._proxyFiPa = projDiPa / (title + ____.SEP + '1_Proxy.aac')
		self._primFiPa = projDiPa / (title + ____.SEP + '2_Prim.srt')
		self._draftFiPa = projDiPa / (title + ____.SEP + '3_Draft.srt')
		self._chopFiPa = projDiPa / (title + ____.SEP + '4_Chop.srt')
		self._regularFiPa = projDiPa / (title + ____.SEP + '5_Regular.srt')
		self._timelineFiPa = projDiPa / (title + ____.SEP + '6_Timeline.xml')
		self._previewFiPa = projDiPa / (title + ____.SEP + '7_Preview.mp4')
		self._proofFiPa = projDiPa / (title + ____.SEP + '8_Proof.srt')
		self._dummyFiPa = projDiPa / (title + ____.SEP + 'Dummy.mp4')
		pass

	def dummy(self, ow: bool = False):
		print('<dummy>')
		if ow or not self._dummyFiPa.is_file():
			____.makeDummy(self._rawFiPa, self._dummyFiPa)
			pass
		pass

	def proxy(self, ow: bool = False, load: bool = True):
		print('<proxy>')
		if ow or not self._proxyFiPa.is_file():
			____.makeProxy(self._rawFiPa, self._proxyFiPa)
			pass
		if load and not self.__proxy:
			self.__proxy = Audio.load(self._proxyFiPa).normLufs(____.LUFS)
			pass
		pass

	def prim(self, ow: bool = False, load: bool = True):
		print('<prim>')
		if ow or not self._primFiPa.is_file():
			self.proxy()

			cont: Texture = self.__vad.probe(self.__proxy)
			cont = cont.aggrByGran()

			tex = self.__whisp.trans(self.__proxy, cont)
			tex.save(self._primFiPa.as_posix())
			pass
		if load and not self.__prim:
			self.__prim = Texture.load(self._primFiPa.as_posix())
			pass
		pass

	def draft(self, ow: bool = False, load: bool = True):
		print('<draft>')
		if ow or not self._draftFiPa.is_file():
			self.proxy()
			self.prim()
			tex = self.__prim.calib(self.__proxy, -30).extent([200, 100])
			tex.save(self._draftFiPa.as_posix())
			pass
		if load and not self.__draft:
			self.__draft = Texture.load(self._draftFiPa.as_posix())
			pass
		pass

	def chop(self):
		print('<chop>')
		if not self.__chop:
			self.__chop = Texture.load(self._chopFiPa.as_posix())
			pass
		pass

	def regular(self, ow: bool = False, load: bool = True):
		print('<regular>')
		if ow or not self._regularFiPa.is_file():
			self.chop()
			self.proxy()

			tex = self.__chop.calib(self.__proxy, -25).extent([200, 100])
			tex.save(self._regularFiPa.as_posix())
			pass
		if load and not self.__draft:
			self.__regular = Texture.load(self._regularFiPa.as_posix())
			pass
		pass

	def timeline(self, ow: bool = False, load: bool = False):
		print('<timeline>')
		if ow or not self._timelineFiPa.is_file():
			self.chop()
			self.proxy()
			self.regular()

			cont = self.__chop.calib(self.__proxy, -30).extent([500, 250])
			cont = cont.aggrByGap()

			refFiPa = self._dummyFiPa if self._dummyFiPa.is_file() else self._rawFiPa
			ske = cont.toSketch(refFiPa, 60)
			ske.write(self._timelineFiPa, encoding='utf-8')
			pass
		if load and not self.__timeline:
			self.__timeline = ET.parse(self._timelineFiPa)
			pass
		pass

	pass
