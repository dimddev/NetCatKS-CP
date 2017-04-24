__author__ = 'dimd'
from zope.component import createObject


def get_factory_objects(objects):

    storage = createObject('storageregister')

    objects.sort()

    temp = []

    for obj in objects:

        prefix = storage.components.get(obj, None)

        if prefix is None:
            continue

        temp.append(createObject(obj + prefix))

    return tuple(temp)
