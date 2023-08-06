import json5
import numpy
import torch
import zhconv
import ffmpeg
import whisper
import librosa
import soundfile
import pyloudnorm
import subprocess

import re as regex

from pathlib import Path

from typing import Optional, Union
from pysubs2 import SSAFile, SSAEvent

import xml.etree.ElementTree as ET


class ____:
	SEP = '┆'

	FPS: int = 16000

	LUFS: float = -15
	TP: float = -0.5

	MAX_GRAN: int = 20000
	MIN_GAP: int = 200

	STEP = 10

	REF_ID = '________'

	@classmethod
	def makeProxy(
		cls,
		rawFiPa: Path, proxyFiPa: Path,
		fps: int = FPS, lufs: float = LUFS, tp: float = TP
	):
		pipe = ffmpeg.input(rawFiPa.as_posix())
		pipe = ffmpeg.filter(pipe, "loudnorm", I=lufs, TP=tp)
		pipe = ffmpeg.output(pipe, proxyFiPa.as_posix(), ar=fps, ac=1)
		ffmpeg.run(pipe, quiet=True, overwrite_output=True)
		pass

	@classmethod
	def makeDummy(cls, rawFiPa: Path, dummyFiPa: Path):
		cmd = ' '.join([
			'ffmpeg -y -v warning',
			'-f lavfi -i color=c=0x202020:s=1920x1080:r=10',
			'-i "%s"' % rawFiPa.as_posix(),
			'-c:a copy',
			'-shortest',
			'"%s"' % dummyFiPa.as_posix(),
		])
		# print(cmd)
		subprocess.run(cmd, encoding='UTF-8')
		pass

	@classmethod
	def getMediaMeta(cls, mediaFiPa: Path):
		cmd = ' '.join([
			'ffprobe -v warning',
			'-show_format',
			'-show_streams',
			'-print_format json',
			'"%s"' % mediaFiPa.as_posix()
		])
		# print(cmd)
		___ = subprocess.check_output(cmd).decode('utf-8')
		___ = json5.loads(___, encoding='utf-8')
		return ___

	@classmethod
	def elem(cls, tag: str, attr: dict = None, text=None, children: list = None):
		if attr:
			attr = {k: str(v) for k, v in attr.items()}
			pass
		___ = ET.Element(tag, attrib=attr) if attr else ET.Element(tag)
		if text:
			___.text = str(text)
			pass
		if children:
			[___.append(_) for _ in children]
			pass
		return ___

	pass
