from kws.engines import Porcupine
from kws.engines import snowboydetect

import os
from collections import namedtuple
from enum import Enum

import numpy as np

class Engine(object):
    def process(self, pcm):
        raise NotImplementedError()

    def release(self):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    @staticmethod
    def frame_length():
        return 512

    @staticmethod
    def sensitivity_info(engine_type):
        if engine_type is Engines.POCKET_SPHINX:
            return SensitivityInfo(-21, 15, 3)
        elif engine_type is Engines.PORCUPINE:
            return SensitivityInfo(0, 1, 0.1)
        elif engine_type is Engines.PORCUPINE_COMPRESSED:
            return SensitivityInfo(0, 1, 0.1)
        elif engine_type is Engines.SNOWBOY:
            return SensitivityInfo(0, 1, 0.05)
        else:
            raise ValueError("no sensitivity range for '%s'", engine_type.value)

    @staticmethod
    def create(engine, keyword, sensitivity):
        if engine is Engines.POCKET_SPHINX:
            return PocketSphinxEngine(keyword, sensitivity)
        elif engine is Engines.PORCUPINE:
            return PorcupineEngine(keyword, sensitivity)
        elif engine is Engines.PORCUPINE_COMPRESSED:
            return PorcupineCompressedEngine(keyword, sensitivity)
        elif engine is Engines.SNOWBOY:
            return SnowboyEngine(keyword, sensitivity)
        else:
            ValueError("cannot create engine of type '%s'", engine.value)



class SnowboyEngine(Engine):
    def __init__(self, keyword, sensitivity):
        keyword = keyword.lower()
        if keyword == 'alexa':
            model_relative_path = 'kws/engines/snowboy/resources/alexa/alexa-avs-sample-app/alexa.umdl'
        else:
            model_relative_path = 'kws/engines/snowboy/resources/models/%s.umdl' % keyword.replace(' ', '_')
        model_str = os.path.join(os.path.dirname(__file__), model_relative_path).encode()
        resource_filename = os.path.join(os.path.dirname(__file__), 'kws/engines/snowboy/resources/common.res').encode()
        self._snowboy = snowboydetect.SnowboyDetect(resource_filename=resource_filename, model_str=model_str)

        # https://github.com/Kitt-AI/snowboy#pretrained-universal-models

        if keyword == 'jarvis':
            self._snowboy.SetSensitivity(('%f,%f' % (sensitivity, sensitivity)).encode())
        else:
            self._snowboy.SetSensitivity(str(sensitivity).encode())

        if keyword in {'alexa', 'computer', 'jarvis', 'view glass'}:
            self._snowboy.ApplyFrontend(True)
        else:
            self._snowboy.ApplyFrontend(False)

    def process(self, pcm):
        assert pcm.dtype == np.int16

        return self._snowboy.RunDetection(pcm.tobytes()) == 1

    def release(self):
        pass

    def __str__(self):
        return 'Snowboy'

import os

class PorcupineEngineBase(Engine):
    def __init__(self, model_file_path, keyword_file_path, sensitivity):
        self._porcupine = Porcupine(
            library_path=os.path.join(self._repo_path, 'lib/linux/x86_64/libpv_porcupine.so'),
            model_file_path=model_file_path,
            keyword_file_path=keyword_file_path,
            sensitivity=sensitivity)

    def process(self, pcm):
        assert pcm.dtype == np.int16

        return self._porcupine.process(pcm)

    def release(self):
        self._porcupine.delete()

    def __str__(self):
        raise NotImplementedError()

    @property
    def _repo_path(self):
        return os.path.join(os.path.dirname(__file__), 'kws/engines/porcupine')


class PorcupineEngine(PorcupineEngineBase):
    def __init__(self, keyword, sensitivity):
        super().__init__(
            os.path.join(self._repo_path, 'lib/common/porcupine_params.pv'),
            os.path.join(self._repo_path, 'resources/keyword_files/linux/%s_linux.ppn' % keyword.lower()),
            sensitivity)

    def __str__(self):
        return 'Porcupine'


class PorcupineCompressedEngine(PorcupineEngineBase):
    def __init__(self, keyword, sensitivity):
        super().__init__(
            os.path.join(self._repo_path, 'lib/common/porcupine_compressed_params.pv'),
            os.path.join(self._repo_path, 'resources/keyword_files/linux/%s_linux_compressed.ppn' % keyword.lower()),
            sensitivity)

    def __str__(self):
        return 'Porcupine Compressed'

