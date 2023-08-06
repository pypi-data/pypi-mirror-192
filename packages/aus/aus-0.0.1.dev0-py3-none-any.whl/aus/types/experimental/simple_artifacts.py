from aus.types import artifact


class Dataset(artifact.Artifact):
  TYPE_NAME = 'Dataset'


class File(artifact.Artifact):
  TYPE_NAME = 'File'


class Statistics(artifact.Artifact):
  TYPE_NAME = 'Statistics'


class Metrics(artifact.Artifact):
  TYPE_NAME = 'Metrics'