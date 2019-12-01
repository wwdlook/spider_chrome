# coding=utf-8

import os
import glob
import importlib
import copy
CUR_DIR = os.path.abspath('processors')


class ProcessorBase:
    def __init__(self, *args, **kwargs):
        if len(kwargs) > 0:
            self.params = copy.deepcopy(kwargs)
        else:
            self.params = None

    def set_params(self, **kwargs):
        if len(kwargs) > 0:
            self.params.update(
                kwargs
            )

    def process(self, *args, **kwargs):
        pass


def load_processors(names=None):
    """
    import all processor class whose name starts with 'processor' under app/processors/
    :return: dict({ClassName: ClassObject})
    """
    _processors = dict()
    if names is None:
        print(CUR_DIR)
        processors = glob.glob(CUR_DIR + '/processor_*.py')
    else:
        processors = []
        for name in names:
            processors.extend(glob.glob(CUR_DIR + '/'+name+'.py'))
    n = len(CUR_DIR)+1
    for p in processors:
        p = p[n:-3]
        module_name = 'processors.' + p
        class_name = ''.join([c.capitalize() for c in p.split('_')])
        print(module_name)
        module = importlib.import_module(module_name, __package__)
        processor_class = getattr(module, class_name)
        print(processor_class.__name__)
        _processors[processor_class.__name__] = processor_class
    return _processors


if __name__ == '__main__':
    load_processors()
    pass
